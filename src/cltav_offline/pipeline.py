"""One-way capture-to-evidence pipeline for the bounded offline intake slice."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import __version__
from .capture import CaptureFormatError, CaptureReader
from .events import first_slice_events
from .models import DatagramRecord, Diagnostic, PacketRef, ProtocolEvent, TransferRecord
from .network import Ipv4Reassembler, PacketDecodeError, UDP_PROTOCOL, decode_udp, extract_ipv4
from .tftp import TftpReconstructor


class IntakeError(ValueError):
    """A fatal invocation/input condition.  Fatal runs never publish output."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


SOURCE_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def validate_source_commit(value: object) -> str:
    """Require an immutable Git object ID for every published evidence item."""
    if not isinstance(value, str) or not SOURCE_COMMIT_RE.fullmatch(value):
        raise IntakeError(
            "INVALID-SOURCE-COMMIT",
            "source commit must be a lowercase 40-character Git object ID",
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
    max_transfer_records: int = 200_000
    max_transfer_bytes: int = 16 * 1024 * 1024
    max_evidence_records: int = 200_000
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
            "maxEvidenceRecords": self.max_evidence_records,
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
        ) or any(record.reconstruction_status != "COMPLETE" for record in self.transfers)

    def to_dict(self, *, source_commit: str) -> dict[str, Any]:
        source_commit = validate_source_commit(source_commit)
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
            "tool": {
                "name": "cltav-offline",
                "version": __version__,
                "sourceCommit": source_commit,
                "contractIds": ["CR-2026-016", "CR-2026-017", "DD-038", "DD-040", "DD-041"],
            },
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
            "diagnostics": [item.to_dict() for item in self.diagnostics],
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
        raise IntakeError("INPUT-READ-ERROR", str(exc)) from exc
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
        raise IntakeError("INPUT-IDENTITY-MISMATCH", "input does not match its declared identity")
    reader = CaptureReader(
        path, capture_id,
        max_packet_bytes=config.max_packet_bytes,
        max_block_bytes=config.max_container_block_bytes,
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
        max_transfer_records=config.max_transfer_records,
    )
    result = IntakeResult(
        capture_id=capture_id,
        byte_count=before[0],
        sha256=before[1],
        config=config,
        capture_metadata={},
    )
    stopped_for_limit = False

    def accept_datagram(record: DatagramRecord) -> None:
        nonlocal stopped_for_limit
        if len(result.datagrams) >= config.max_evidence_records:
            stopped_for_limit = True
            result.diagnostics.append(Diagnostic(
                "RESOURCE-EVIDENCE-RECORD-LIMIT", "PIPELINE",
                "configured evidence-record limit reached; remaining packets were not consumed",
                detail={"limit": config.max_evidence_records},
            ))
            return
        result.datagrams.append(record)
        _append_packet_refs(result.packet_refs, record.packet_refs)
        if record.status != "COMPLETE" or record.protocol != UDP_PROTOCOL:
            return
        try:
            udp = decode_udp(record)
        except PacketDecodeError as exc:
            result.diagnostics.append(Diagnostic(
                exc.code, "UDP", str(exc), packet_ref_id=record.packet_refs[-1].id,
                detail={"datagramId": record.datagram_id},
            ))
            return
        if transfers.could_be_tftp(udp):
            transfers.process(udp)

    try:
        for captured in reader:
            if stopped_for_limit:
                break
            try:
                fragment = extract_ipv4(captured.ref, captured.data)
            except PacketDecodeError as exc:
                result.diagnostics.append(Diagnostic(
                    exc.code, "NETWORK", str(exc), severity="WARNING",
                    packet_ref_id=captured.ref.id,
                ))
                continue
            if fragment is None:
                continue
            for record in reassembler.add(fragment):
                accept_datagram(record)
                if stopped_for_limit:
                    break
        if not stopped_for_limit:
            for record in reassembler.finish():
                accept_datagram(record)
    except CaptureFormatError as exc:
        raise IntakeError(exc.code, str(exc)) from exc
    finally:
        result.capture_metadata = reader.metadata.to_dict()
        result.container_packet_count = reader.metadata.packet_count
        result.diagnostics.extend(reader.metadata.diagnostics)
    if stopped_for_limit:
        # Active records are flushed even after a resource stop, preserving why
        # their reconstruction cannot be treated as complete.
        for record in reassembler.finish("RESOURCE-EVIDENCE-RECORD-LIMIT"):
            if len(result.datagrams) < config.max_evidence_records:
                result.datagrams.append(record)
                _append_packet_refs(result.packet_refs, record.packet_refs)
    result.diagnostics.extend(transfers.diagnostics)
    result.transfers = transfers.finish()
    result.events = first_slice_events(result.transfers)
    after = input_identity(path)
    if after != before:
        raise IntakeError(
            "INPUT-IDENTITY-CHANGED", "input identity changed during the read-only intake run"
        )
    return result


def _append_packet_refs(target: list[PacketRef], values: list[PacketRef]) -> None:
    known = {item.id for item in target}
    for item in values:
        if item.id not in known:
            target.append(item)
            known.add(item.id)


def _validate_config(config: IntakeConfig) -> None:
    for label, value in config.to_dict().items():
        if value < 1:
            raise IntakeError("INVALID-RUNTIME-LIMIT", f"{label} must be positive")
    if config.max_datagram_bytes > 65_535:
        raise IntakeError("INVALID-RUNTIME-LIMIT", "maxDatagramBytes cannot exceed IPv4 maximum")
    if config.tftp_service_port > 65_535:
        raise IntakeError("INVALID-RUNTIME-LIMIT", "tftpServicePort must not exceed 65535")
