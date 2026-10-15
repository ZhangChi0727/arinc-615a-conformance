"""One-way capture-to-evidence pipeline for the bounded offline intake slice."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import __version__
from .capture import CaptureFormatError, CaptureReader
from .contracts import ContractProjectionError, project_development_records
from .controlled_resources import ControlledResourceError
from .events import iter_first_slice_events
from .identity import tool_identity
from .models import DatagramRecord, Diagnostic, PacketRef, ProtocolEvent, TransferRecord
from .network import Ipv4Reassembler, PacketDecodeError, UDP_PROTOCOL, decode_udp, extract_ipv4
from .tftp import TftpReconstructor


class IntakeError(ValueError):
    """A fatal invocation/input condition.  Fatal runs never publish output."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        input_fault: bool = False,
        stage: str = "TOOL",
        container_offset: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.input_fault = input_fault
        self.stage = stage
        self.container_offset = container_offset


SOURCE_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def validate_source_commit(value: object) -> str:
    """Validate an optional caller claim without calling arbitrary CWD Git."""
    if value is None or value == "UNVERIFIED":
        return "UNVERIFIED"
    if not isinstance(value, str) or not SOURCE_COMMIT_RE.fullmatch(value):
        raise IntakeError(
            "INVALID-SOURCE-COMMIT",
            "source commit claim must be a lowercase 40-character Git object ID",
        )
    return value


@dataclass(frozen=True)
class IntakeConfig:
    """Implementation limits, explicitly separate from protocol constants."""

    max_packet_bytes: int = 2 * 1024 * 1024
    max_container_block_bytes: int = 4 * 1024 * 1024
    max_active_datagrams: int = 128
    max_datagram_bytes: int = 65_535
    max_fragments_per_datagram: int = 8_192
    max_active_transfers: int = 128
    max_transfer_records: int = 50_000
    max_transfer_bytes: int = 16 * 1024 * 1024
    max_active_transfer_bytes: int = 16 * 1024 * 1024
    max_completed_payload_bytes: int = 16 * 1024 * 1024
    max_evidence_records: int = 50_000
    max_packet_refs: int = 50_000
    max_diagnostics: int = 50_000
    max_events: int = 50_000
    max_interfaces: int = 1_024
    tftp_service_port: int = 69

    def to_dict(self) -> dict[str, int]:
        return {
            "maxPacketBytes": self.max_packet_bytes,
            "maxContainerBlockBytes": self.max_container_block_bytes,
            "maxActiveDatagrams": self.max_active_datagrams,
            "maxDatagramBytes": self.max_datagram_bytes,
            "maxFragmentsPerDatagram": self.max_fragments_per_datagram,
            "maxActiveTransfers": self.max_active_transfers,
            "maxTransferRecords": self.max_transfer_records,
            "maxTransferBytes": self.max_transfer_bytes,
            "maxActiveTransferBytes": self.max_active_transfer_bytes,
            "maxCompletedPayloadBytes": self.max_completed_payload_bytes,
            "maxEvidenceRecords": self.max_evidence_records,
            "maxPacketRefs": self.max_packet_refs,
            "maxDiagnostics": self.max_diagnostics,
            "maxEvents": self.max_events,
            "maxInterfaces": self.max_interfaces,
            "tftpServicePort": self.tftp_service_port,
        }


@dataclass
class IntakeResult:
    """Serialisable bounded evidence, not a conformance/evaluation result."""

    capture_id: str
    byte_count: int
    sha256: str
    config: IntakeConfig
    capture_metadata: dict[str, Any]
    packet_refs: list[PacketRef] = field(default_factory=list)
    datagrams: list[DatagramRecord] = field(default_factory=list)
    transfers: list[TransferRecord] = field(default_factory=list)
    events: list[ProtocolEvent] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    container_packet_count: int = 0

    @property
    def has_controlled_issue(self) -> bool:
        return bool(self.diagnostics) or any(
            record.status != "COMPLETE" for record in self.datagrams
        ) or any(record.reconstruction_status != "COMPLETE" for record in self.transfers) or (
            self.capture_metadata.get("scanStatus") not in {None, "COMPLETE"}
        ) or any(
            event.layer == "PARSE-RESULT"
            and isinstance(event.fields, dict)
            and event.fields.get("parseStatus") != "PARSED"
            for event in self.events
        )

    def to_dict(self, *, source_commit: str) -> dict[str, Any]:
        source_commit = validate_source_commit(source_commit)
        try:
            projection = project_development_records(self)
        except ContractProjectionError as exc:
            raise IntakeError("CONTRACT-PROJECTION-ERROR", str(exc)) from exc
        except ControlledResourceError as exc:
            raise IntakeError(exc.code, str(exc)) from exc
        return {
            "artifactType": "CLTAV-OFFLINE-INTAKE-EVIDENCE",
            "schemaVersion": "1.0",
            "evidenceBoundary": {
                "purpose": "EXPLORATORY-DEVELOPMENT-ONLY",
                "statement": (
                    "This is passive intake/reconstruction evidence. It is not a protocol "
                    "conformance verdict, product root-cause finding, independent validation "
                    "result, runtime-integrity result, or experimental truth."
                ),
                "conformanceVerdict": "NOT-EVALUATED",
                "integrity": "NOT-EVALUATED",
            },
            "tool": {"version": __version__, **tool_identity(source_commit)},
            "input": {
                "captureId": self.capture_id,
                "byteCount": self.byte_count,
                "sha256": self.sha256,
                "container": self.capture_metadata,
            },
            "runParameters": self.config.to_dict(),
            "executionStatus": (
                "COMPLETE" if not self.has_controlled_issue else "COMPLETE-WITH-CONTROLLED-ISSUES"
            ),
            "counts": {
                "containerPackets": self.container_packet_count,
                "evidencePacketRefs": len(self.packet_refs),
                "datagrams": len(self.datagrams),
                "transfers": len(self.transfers),
                "events": len(self.events),
                "diagnostics": len(self.diagnostics),
            },
            "packetRefs": [item.to_dict() for item in self.packet_refs],
            "datagrams": [item.to_dict() for item in self.datagrams],
            "transfers": [item.to_dict() for item in self.transfers],
            "events": [item.to_dict() for item in self.events],
            "diagnostics": [_diagnostic_dict(item, self.sha256) for item in self.diagnostics],
            "contractProjection": projection,
        }


def input_identity(path: Path) -> tuple[int, str]:
    """Stream an input identity without retaining its payload."""
    try:
        stat = path.stat()
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise IntakeError("INPUT-READ-ERROR", str(exc), input_fault=True, stage="INPUT") from exc
    return stat.st_size, digest.hexdigest()


def run_capture(
    path: Path,
    *,
    capture_id: str,
    config: IntakeConfig | None = None,
    expected_identity: tuple[int, str] | None = None,
) -> IntakeResult:
    """Run the complete bounded intake pipeline on one immutable-looking input."""
    if not capture_id or not capture_id.strip():
        raise IntakeError("INVALID-CAPTURE-ID", "capture ID must be nonempty")
    config = config or IntakeConfig()
    _validate_config(config)
    before = input_identity(path)
    if expected_identity is not None and before != expected_identity:
        raise IntakeError(
            "INPUT-IDENTITY-MISMATCH", "input does not match its declared identity",
            input_fault=True, stage="INPUT",
        )
    reader = CaptureReader(
        path, capture_id,
        max_packet_bytes=config.max_packet_bytes,
        max_block_bytes=config.max_container_block_bytes,
        # Reserve one shared-evidence slot for an explicit stop witness.  Input
        # interface metadata is published evidence too; it cannot bypass the
        # same retention budget used by packets, reconstructions, and events.
        max_interfaces=config.max_interfaces,
        max_diagnostics=min(config.max_diagnostics, config.max_evidence_records),
    )
    reassembler = Ipv4Reassembler(
        max_active_datagrams=config.max_active_datagrams,
        max_datagram_bytes=config.max_datagram_bytes,
        max_fragments_per_datagram=config.max_fragments_per_datagram,
    )
    transfers = TftpReconstructor(
        capture_id=capture_id,
        service_port=config.tftp_service_port,
        max_active_transfers=config.max_active_transfers,
        max_transfer_bytes=config.max_transfer_bytes,
        max_active_transfer_bytes=config.max_active_transfer_bytes,
        max_completed_payload_bytes=config.max_completed_payload_bytes,
        max_transfer_records=config.max_transfer_records,
        max_diagnostics=min(config.max_diagnostics, config.max_evidence_records),
    )
    result = IntakeResult(
        capture_id=capture_id,
        byte_count=before[0],
        sha256=before[1],
        config=config,
        capture_metadata={},
    )
    stopped_for_limit = False
    packet_ref_ids: set[str] = set()
    live_transfer_ids: set[str] = set()
    diagnostic_limit_reported = False
    # A producer-local resource condition (for example, refusing one extra
    # transfer record) is not necessarily an input-stop boundary.  If it
    # cannot be retained without consuming the reserved final slot, remember
    # that fact and let the later, actual scan/derived-output boundary occupy
    # that slot.  The producer is allowed to continue because its controlled
    # record state remains serialised; only the duplicate detail diagnostic is
    # omitted.
    diagnostic_retention_pending = False
    last_consumed_packet: PacketRef | None = None
    post_scan_reclaimed_active: PacketRef | None = None

    def retained_count() -> int:
        return (
            len(reader.metadata.interfaces)
            + len(result.packet_refs)
            + len(result.datagrams)
            # Fragmented IPv4 datagrams have not reached the public result yet,
            # but their accumulators own packet provenance and payload bytes.
            + reassembler.active_count
            # Transfer records become public only after the capture scan, but
            # their internal sessions are still retained evidence state.  Count
            # them from admission onwards, not only after final serialisation.
            + max(len(result.transfers), len(live_transfer_ids))
            + len(result.events)
            + len(result.diagnostics)
        )

    def admit_transfer(record: TransferRecord) -> bool:
        """Reserve one shared evidence slot before TFTP stores a session."""
        if retained_count() >= config.max_evidence_records - 1:
            return False
        live_transfer_ids.add(record.transfer_id)
        return True

    def admit_interface(_interface: object) -> bool:
        """Reserve metadata evidence before a pcapng IDB is retained."""
        return retained_count() < config.max_evidence_records - 1

    def admit_reassembly(_fragment: object) -> bool:
        """Reserve a live slot before retaining a fragmented IPv4 accumulator."""
        # A reassembly accumulator may use the final slot only until it is
        # transferred into a terminal datagram at EOF.  If a later input
        # boundary arrives, its stop-witness path releases that private state
        # before retaining the witness.  The next item can be a pcapng IDB,
        # not only another packet.
        return retained_count() < config.max_evidence_records

    transfers.set_record_admission(admit_transfer)
    reader.set_interface_admission(admit_interface)
    reassembler.set_active_admission(admit_reassembly)

    def is_final_resource_boundary(diagnostic: Diagnostic) -> bool:
        """Return whether a diagnostic truthfully consumes the reserved slot.

        Resource *names* alone are not enough: several resource codes describe
        a local, controlled reconstruction outcome while capture scanning can
        continue.  Final-slot admission is restricted to explicit unread-input
        or post-scan-retention boundaries (plus the generic diagnostic-limit
        witness created below).
        """
        detail = diagnostic.detail
        return diagnostic.code == "RESOURCE-DIAGNOSTIC-LIMIT" or (
            isinstance(detail, dict)
            and ("unconsumedSuffix" in detail or "retentionBoundary" in detail)
        )

    def emit_diagnostic(diagnostic: Diagnostic, *, input_stop: bool = True) -> bool:
        """Retain a bounded diagnostic stream with one reserved stop witness."""
        nonlocal stopped_for_limit, diagnostic_limit_reported, diagnostic_retention_pending
        boundary_witness = is_final_resource_boundary(diagnostic)
        # An unfinished IPv4 reassembly is private retained state.  It may
        # borrow the final slot so that a capture ending at EOF can still
        # publish its gapped record.  Once an actual unread-input boundary is
        # known, however, that slot belongs to the truthful boundary witness.
        # Do this here, rather than only from retain_packet_ref(), because a
        # pcapng interface-description block can be the next input item.
        released = None
        if boundary_witness and input_stop:
            released = reassembler.discard_oldest_for_resource_stop()
            if released is not None:
                detail = dict(diagnostic.detail)
                detail.setdefault("discardedActivePacketRefId", released.id)
                diagnostic = Diagnostic(
                    diagnostic.code, diagnostic.stage, diagnostic.message,
                    severity=diagnostic.severity, packet_ref_id=diagnostic.packet_ref_id,
                    container_offset=diagnostic.container_offset, detail=detail,
                )
        if boundary_witness and last_consumed_packet is not None:
            detail = dict(diagnostic.detail)
            detail.setdefault("lastConsumedPacketRefId", last_consumed_packet.id)
            detail.setdefault("lastConsumedPacketIndex", last_consumed_packet.packet_index)
            detail.setdefault("lastConsumedContainerOffset", last_consumed_packet.container_offset)
            diagnostic = Diagnostic(
                diagnostic.code, diagnostic.stage, diagnostic.message,
                severity=diagnostic.severity, packet_ref_id=diagnostic.packet_ref_id,
                container_offset=diagnostic.container_offset, detail=detail,
            )
        diagnostic_limit = min(config.max_diagnostics, config.max_evidence_records)
        # A resource-boundary diagnostic is itself the final retained item.
        # It is allowed to consume the reserved slot whether it marks an
        # unread input suffix or a post-scan derived-retention boundary.
        if (
            len(result.diagnostics) < (diagnostic_limit if boundary_witness else diagnostic_limit - 1)
            and retained_count() < (
                config.max_evidence_records if boundary_witness else config.max_evidence_records - 1
            )
        ):
            result.diagnostics.append(diagnostic)
            return True
        if not boundary_witness:
            # Preserve the final slot for a later real boundary.  Returning
            # success keeps a local TFTP/capture limit from falsely stopping
            # the scan merely because its explanatory diagnostic could not be
            # retained.  The terminal record itself carries the controlled
            # outcome; at EOF we publish a generic boundary if no more
            # specific boundary supersedes it.
            diagnostic_retention_pending = True
            return True
        if not diagnostic_limit_reported and retained_count() < config.max_evidence_records:
            diagnostic_limit_reported = True
            detail: dict[str, Any] = {"limit": diagnostic_limit}
            if input_stop:
                detail["unconsumedSuffix"] = "NOT-CONSUMED"
            else:
                detail["retentionBoundary"] = "POST-SCAN-DIAGNOSTICS-TRUNCATED"
            if last_consumed_packet is not None:
                detail.update({
                    "lastConsumedPacketRefId": last_consumed_packet.id,
                    "lastConsumedPacketIndex": last_consumed_packet.packet_index,
                    "lastConsumedContainerOffset": last_consumed_packet.container_offset,
                })
            result.diagnostics.append(Diagnostic(
                "RESOURCE-DIAGNOSTIC-LIMIT",
                "PIPELINE",
                (
                    "diagnostic retention limit reached; input suffix was not consumed"
                    if input_stop else
                    "diagnostic retention limit reached after input consumption"
                ),
                detail=detail,
            ))
        if input_stop:
            stopped_for_limit = True
        return False

    # Capture and TFTP diagnostics are evidence too.  Admit them while their
    # producers are reading input rather than letting either private queue grow
    # beyond the result's single retention boundary and truncating afterwards.
    reader.set_diagnostic_admission(lambda diagnostic: emit_diagnostic(diagnostic))
    transfers.set_diagnostic_admission(lambda diagnostic: emit_diagnostic(diagnostic))

    def retain_packet_ref(reference: PacketRef) -> bool:
        nonlocal stopped_for_limit
        if reference.id in packet_ref_ids:
            return True
        packet_limit = min(config.max_packet_refs, config.max_evidence_records)
        if len(result.packet_refs) >= packet_limit or retained_count() >= config.max_evidence_records - 1:
            detail: dict[str, Any] = {"limit": packet_limit, "unconsumedSuffix": "NOT-CONSUMED"}
            # emit_diagnostic owns the one-time release of a private active
            # reassembly for every real unread-input boundary.  Keeping that
            # responsibility there covers packet and IDB boundaries uniformly
            # and prevents a packet path from silently discarding two active
            # accumulators for one retained stop witness.
            emit_diagnostic(Diagnostic(
                "RESOURCE-PACKET-REF-LIMIT",
                "PIPELINE",
                "packet-reference retention limit reached; input suffix was not consumed",
                detail=detail,
            ))
            stopped_for_limit = True
            return False
        result.packet_refs.append(reference)
        packet_ref_ids.add(reference.id)
        return True

    def accept_datagram(record: DatagramRecord, *, input_stop: bool = True) -> None:
        nonlocal stopped_for_limit
        # A terminal incomplete reassembly cannot generate a derived protocol
        # event.  At EOF it may therefore occupy the final slot without
        # inventing an unread-input stop witness.
        retention_limit = (
            config.max_evidence_records
            if not input_stop and record.status != "COMPLETE"
            else config.max_evidence_records - 1
        )
        if len(result.datagrams) >= config.max_evidence_records or retained_count() >= retention_limit:
            detail: dict[str, Any] = {"limit": config.max_evidence_records}
            if input_stop:
                detail["unconsumedSuffix"] = "NOT-CONSUMED"
            else:
                detail["retentionBoundary"] = "POST-SCAN-DATAGRAMS-TRUNCATED"
            emit_diagnostic(Diagnostic(
                "RESOURCE-DATAGRAM-RECORD-LIMIT", "PIPELINE",
                (
                    "configured evidence-record limit reached; remaining packets were not consumed"
                    if input_stop else
                    "configured evidence-record limit reached after input consumption"
                ),
                detail=detail,
            ), input_stop=input_stop)
            if input_stop:
                stopped_for_limit = True
            return
        if any(item.id not in packet_ref_ids for item in record.packet_refs):
            detail = {"limit": config.max_packet_refs}
            if input_stop:
                detail["unconsumedSuffix"] = "NOT-CONSUMED"
            else:
                detail["retentionBoundary"] = "POST-SCAN-SOURCES-UNAVAILABLE"
            emit_diagnostic(Diagnostic(
                "RESOURCE-PACKET-REF-LIMIT", "PIPELINE",
                "datagram source references could not be retained",
                detail=detail,
            ), input_stop=input_stop)
            if input_stop:
                stopped_for_limit = True
            record.payload = None
            return
        result.datagrams.append(record)
        if record.status != "COMPLETE" or record.protocol != UDP_PROTOCOL:
            record.payload = None
            return
        try:
            udp = decode_udp(record)
        except PacketDecodeError as exc:
            emit_diagnostic(Diagnostic(
                exc.code, "UDP", str(exc), packet_ref_id=record.packet_refs[-1].id,
                container_offset=record.packet_refs[-1].container_offset,
                detail={"datagramId": record.datagram_id},
            ))
        else:
            if transfers.could_be_tftp(udp):
                transfers.process(udp)
                if transfers.retention_limit_reached:
                    reference = transfers.resource_stop_packet_ref or record.packet_refs[-1]
                    if transfers.resource_limit_kind == "TRANSFER":
                        emit_diagnostic(Diagnostic(
                            "RESOURCE-TRANSFER-EVIDENCE-LIMIT",
                            "TFTP",
                            "shared evidence retention limit reached; later input was not consumed",
                            packet_ref_id=reference.id,
                            container_offset=reference.container_offset,
                            detail={
                                "limit": config.max_evidence_records,
                                "unconsumedSuffix": "NOT-CONSUMED",
                            },
                        ))
                    # A diagnostic-admission rejection has already retained its
                    # own RESOURCE-DIAGNOSTIC-LIMIT witness through the callback.
                    stopped_for_limit = True
        finally:
            record.payload = None

    try:
        for captured in reader:
            last_consumed_packet = captured.ref
            if stopped_for_limit:
                break
            if not retain_packet_ref(captured.ref):
                break
            try:
                fragment = extract_ipv4(captured.ref, captured.data)
            except PacketDecodeError as exc:
                emit_diagnostic(Diagnostic(
                    exc.code, "NETWORK", str(exc), severity="WARNING",
                    packet_ref_id=captured.ref.id, container_offset=captured.ref.container_offset,
                ))
                if stopped_for_limit:
                    break
                continue
            if fragment is None:
                emit_diagnostic(Diagnostic(
                    "UNSUPPORTED-NETWORK-PAYLOAD",
                    "NETWORK",
                    "captured packet is outside the bounded Ethernet/IPv4 intake scope",
                    severity="WARNING",
                    packet_ref_id=captured.ref.id,
                    container_offset=captured.ref.container_offset,
                ))
                if stopped_for_limit:
                    break
                continue
            for record in reassembler.add(fragment):
                accept_datagram(record)
                if stopped_for_limit:
                    break
            if reassembler.retention_limit_reached:
                reference = reassembler.resource_stop_packet_ref or captured.ref
                emit_diagnostic(Diagnostic(
                    "RESOURCE-REASSEMBLY-EVIDENCE-LIMIT",
                    "NETWORK",
                    "shared evidence retention limit reached before retaining fragmented IPv4 state",
                    packet_ref_id=reference.id,
                    container_offset=reference.container_offset,
                    detail={"limit": config.max_evidence_records, "unconsumedSuffix": "NOT-CONSUMED"},
                ))
                stopped_for_limit = True
            if stopped_for_limit:
                break
        if reader.resource_limit_reached and reader.resource_limit_kind == "INTERFACE":
            emit_diagnostic(Diagnostic(
                "RESOURCE-INTERFACE-EVIDENCE-LIMIT",
                "CAPTURE",
                "shared evidence retention limit reached while retaining a pcapng interface",
                container_offset=reader.resource_stop_offset,
                detail={
                    "limit": config.max_evidence_records,
                    "unconsumedSuffix": "NOT-CONSUMED",
                },
            ))
            stopped_for_limit = True
        elif reader.resource_limit_reached:
            # The shared diagnostic callback has already retained a precise
            # RESOURCE-DIAGNOSTIC-LIMIT witness before CaptureReader stopped.
            stopped_for_limit = True
        if not stopped_for_limit:
            # A normal EOF may turn a borrowed active fragment set into one
            # GAPPED datagram.  If an earlier ordinary diagnostic could not be
            # retained, that final slot instead belongs to the explicit
            # post-scan retention boundary.  Otherwise a valid unknown pcapng
            # block can disappear entirely when the EOF conversion consumes
            # the slot after the diagnostic was deferred.
            if diagnostic_retention_pending and retained_count() >= config.max_evidence_records:
                post_scan_reclaimed_active = reassembler.discard_oldest_for_resource_stop()
            for record in reassembler.finish():
                accept_datagram(record, input_stop=False)
    except CaptureFormatError as exc:
        raise IntakeError(
            exc.code, str(exc), input_fault=True, stage="CAPTURE", container_offset=exc.offset,
        ) from exc
    finally:
        result.capture_metadata = reader.metadata.to_dict()
        result.container_packet_count = reader.metadata.packet_count
        for diagnostic in reader.metadata.diagnostics:
            if diagnostic.packet_ref_id is not None and diagnostic.packet_ref_id not in packet_ref_ids:
                detail = dict(diagnostic.detail)
                detail["packetRefUnavailable"] = diagnostic.packet_ref_id
                diagnostic = Diagnostic(
                    diagnostic.code, diagnostic.stage, diagnostic.message,
                    severity=diagnostic.severity, container_offset=diagnostic.container_offset, detail=detail,
                )
            emit_diagnostic(diagnostic, input_stop=False)
    if stopped_for_limit:
        # Active records are flushed even after a resource stop, preserving why
        # their reconstruction cannot be treated as complete.
        for record in reassembler.finish("RESOURCE-EVIDENCE-RECORD-LIMIT"):
            if (
                len(result.datagrams) < config.max_evidence_records
                and retained_count() < config.max_evidence_records - 1
                and all(item.id in packet_ref_ids for item in record.packet_refs)
            ):
                result.datagrams.append(record)
    for diagnostic in transfers.diagnostics:
        emit_diagnostic(diagnostic, input_stop=False)
    # Every transfer was admitted before TFTP stored its internal session, so
    # publishing the finished list cannot silently exceed the shared bound.
    result.transfers = transfers.finish()
    events_truncated = False
    for event in iter_first_slice_events(result.transfers):
        if len(result.events) >= config.max_events or retained_count() >= config.max_evidence_records - 1:
            events_truncated = True
            break
        result.events.append(event)
    if events_truncated:
        # This is post-EOF derivation retention, not an unread input suffix.
        # Keep the scan result truthful while preserving an explicit boundary.
        event_limit_detail: dict[str, Any] = {
            "limit": min(config.max_events, config.max_evidence_records),
            "retentionBoundary": "DERIVED-EVENTS-TRUNCATED",
            "scanStatus": "COMPLETE" if not stopped_for_limit else "STOPPED-RESOURCE-LIMIT",
        }
        if diagnostic_retention_pending:
            event_limit_detail["earlierDiagnosticRetention"] = "NOT-RETAINED"
        emit_diagnostic(Diagnostic(
            "RESOURCE-EVENT-LIMIT",
            "EVENT",
            "event retention limit reached; later derived events were not retained",
            detail=event_limit_detail,
        ), input_stop=False)
    elif diagnostic_retention_pending and not stopped_for_limit:
        # An ordinary producer diagnostic was deliberately kept out of the
        # final slot, and no later event boundary consumed it.  State that
        # post-scan fact explicitly instead of silently dropping it.
        detail: dict[str, Any] = {
            "limit": min(config.max_diagnostics, config.max_evidence_records),
            "retentionBoundary": "POST-SCAN-DIAGNOSTICS-TRUNCATED",
        }
        if post_scan_reclaimed_active is not None:
            detail["discardedActivePacketRefId"] = post_scan_reclaimed_active.id
        emit_diagnostic(Diagnostic(
            "RESOURCE-DIAGNOSTIC-LIMIT",
            "PIPELINE",
            "diagnostic retention limit reached after input consumption",
            detail=detail,
        ), input_stop=False)

    # A quality diagnostic is emitted before its packet can be admitted.  If a
    # resource boundary stops the reader at exactly that point, detach the
    # unavailable packet reference rather than serialising dangling provenance.
    for index, diagnostic in enumerate(result.diagnostics):
        if diagnostic.packet_ref_id is not None and diagnostic.packet_ref_id not in packet_ref_ids:
            detail = dict(diagnostic.detail)
            detail["packetRefUnavailable"] = diagnostic.packet_ref_id
            result.diagnostics[index] = Diagnostic(
                diagnostic.code, diagnostic.stage, diagnostic.message,
                severity=diagnostic.severity, container_offset=diagnostic.container_offset,
                detail=detail,
            )
    if stopped_for_limit:
        result.capture_metadata["scanStatus"] = "STOPPED-RESOURCE-LIMIT"
        result.capture_metadata["unconsumedSuffix"] = "NOT-CONSUMED"
    else:
        result.capture_metadata["scanStatus"] = "COMPLETE"
    # Payload bytes are only an in-process parse input.  The serialised record
    # retains their length and source chain, never the payload itself.
    for transfer in result.transfers:
        transfer.complete_payload = None
    after = input_identity(path)
    if after != before:
        raise IntakeError(
            "INPUT-IDENTITY-CHANGED", "input identity changed during the read-only intake run",
            input_fault=True, stage="INPUT",
        )
    return result


def _append_packet_refs(
    target: list[PacketRef], values: list[PacketRef], known: set[str] | None = None,
) -> None:
    """Append source references once without a repeated whole-result scan."""
    if known is None:
        known = {item.id for item in target}
    for item in values:
        if item.id not in known:
            target.append(item)
            known.add(item.id)


def _diagnostic_dict(diagnostic: Diagnostic, input_sha256: str) -> dict[str, Any]:
    """Attach the immutable input identity to each retained diagnostic."""
    rendered = diagnostic.to_dict()
    detail = dict(rendered.get("detail", {}))
    detail["inputSha256"] = input_sha256
    rendered["detail"] = detail
    return rendered


def _validate_config(config: IntakeConfig) -> None:
    for label, value in config.to_dict().items():
        if value < 1:
            raise IntakeError("INVALID-RUNTIME-LIMIT", f"{label} must be positive")
    if config.max_datagram_bytes > 65_535:
        raise IntakeError("INVALID-RUNTIME-LIMIT", "maxDatagramBytes cannot exceed IPv4 maximum")
    if config.max_evidence_records < 2:
        raise IntakeError(
            "INVALID-RUNTIME-LIMIT",
            "maxEvidenceRecords must reserve one item for an explicit resource-stop witness",
        )
    if config.tftp_service_port > 65_535:
        raise IntakeError("INVALID-RUNTIME-LIMIT", "tftpServicePort must not exceed 65535")
