"""Typed, payload-minimising records for offline intake evidence.

Internal packet bytes are intentionally absent from the serialised records.
They are used only while reconstructing a bounded capture and are never
published in the evidence index.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Timestamp:
    """An exact capture timestamp, without a floating-point conversion."""

    ticks: int
    ticks_per_second: int
    offset_seconds: int = 0
    clock_domain: str = "CAPTURE-INTERFACE-UNASSESSED"

    def to_dict(self) -> dict[str, Any]:
        return {
            "ticks": self.ticks,
            "ticksPerSecond": self.ticks_per_second,
            "offsetSeconds": self.offset_seconds,
            "clockDomain": self.clock_domain,
            "accuracy": "UNKNOWN",
        }


@dataclass(frozen=True)
class PacketRef:
    """A source reference for one container packet record."""

    capture_id: str
    packet_index: int
    container_offset: int
    interface_id: int
    link_type: int
    captured_length: int
    original_length: int
    timestamp: Timestamp | None

    @property
    def id(self) -> str:
        return f"{self.capture_id}:P{self.packet_index:08d}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "packetRefId": self.id,
            "captureId": self.capture_id,
            "packetIndex": self.packet_index,
            "containerOffset": self.container_offset,
            "interfaceId": self.interface_id,
            "linkType": self.link_type,
            "capturedLength": self.captured_length,
            "originalLength": self.original_length,
            "timestamp": None if self.timestamp is None else self.timestamp.to_dict(),
        }


@dataclass(frozen=True)
class CapturedPacket:
    """A packet record whose bytes are kept only for the current pipeline run."""

    ref: PacketRef
    data: bytes


@dataclass(frozen=True)
class Diagnostic:
    """A stable, evidence-scoped parser/reconstruction diagnostic."""

    code: str
    stage: str
    message: str
    severity: str = "ERROR"
    packet_ref_id: str | None = None
    container_offset: int | None = None
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "code": self.code,
            "stage": self.stage,
            "severity": self.severity,
            "message": self.message,
        }
        if self.packet_ref_id is not None:
            result["packetRefId"] = self.packet_ref_id
        if self.container_offset is not None:
            result["containerOffset"] = self.container_offset
        if self.detail:
            result["detail"] = self.detail
        return result


@dataclass(frozen=True)
class Ipv4Fragment:
    """A validated IPv4 fragment, after link-layer parsing."""

    packet_ref: PacketRef
    source: str
    destination: str
    identification: int
    protocol: int
    fragment_offset: int
    more_fragments: bool
    payload: bytes
    vlan_tags: tuple[int, ...] = ()

    @property
    def key(self) -> tuple[str, int, str, str, int, int]:
        """Include capture/interface/direction context; never key by IP ID alone."""
        return (
            self.packet_ref.capture_id,
            self.packet_ref.interface_id,
            self.source,
            self.destination,
            self.protocol,
            self.identification,
        )


@dataclass
class DatagramRecord:
    """A finite IPv4 reconstruction record.

    ``payload`` is retained internally only long enough for UDP/TFTP decoding;
    serialisation exposes length and provenance, not payload bytes.
    """

    datagram_id: str
    capture_id: str
    interface_id: int
    source: str
    destination: str
    protocol: int
    identification: int
    status: str
    failure_code: str | None
    packet_refs: list[PacketRef]
    fragment_ranges: list[tuple[int, int]]
    missing_ranges: list[tuple[int, int]] = field(default_factory=list)
    conflict_ranges: list[tuple[int, int]] = field(default_factory=list)
    payload: bytes | None = None
    payload_length: int | None = None
    vlan_tags: tuple[int, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "datagramId": self.datagram_id,
            "captureId": self.capture_id,
            "interfaceId": self.interface_id,
            "source": self.source,
            "destination": self.destination,
            "protocol": self.protocol,
            "ipv4Identification": self.identification,
            "status": self.status,
            "failureCode": self.failure_code,
            "payloadLength": (
                self.payload_length
                if self.payload_length is not None
                else None if self.payload is None else len(self.payload)
            ),
            "packetRefIds": [item.id for item in self.packet_refs],
            "fragmentRanges": [list(item) for item in self.fragment_ranges],
            "missingRanges": [list(item) for item in self.missing_ranges],
            "conflictRanges": [list(item) for item in self.conflict_ranges],
            "vlanTags": list(self.vlan_tags),
        }


@dataclass(frozen=True)
class UdpDatagram:
    """A strictly bounded UDP payload derived from a complete IPv4 datagram."""

    datagram: DatagramRecord
    source_port: int
    destination_port: int
    payload: bytes
    checksum_present: bool


@dataclass(frozen=True)
class TftpMessage:
    """A parsed TFTP message.  Payload stays internal to session reconstruction."""

    kind: str
    fields: dict[str, Any]


@dataclass
class TransferRecord:
    """A bounded TFTP-session evidence record."""

    transfer_id: str
    capture_id: str
    request_kind: str | None
    filename: str | None
    mode: str | None
    client_endpoint: tuple[str, int] | None
    server_endpoint: tuple[str, int | None] | None
    association_status: str
    reconstruction_status: str
    option_status: str
    effective_block_size: int | None
    packet_refs: list[PacketRef] = field(default_factory=list)
    datagram_ids: list[str] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)
    terminal_block: int | None = None
    complete_payload: bytes | None = None
    complete_payload_length: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "transferId": self.transfer_id,
            "captureId": self.capture_id,
            "requestKind": self.request_kind,
            "filename": self.filename,
            "mode": self.mode,
            "clientEndpoint": None if self.client_endpoint is None else {
                "address": self.client_endpoint[0], "port": self.client_endpoint[1],
            },
            "serverEndpoint": None if self.server_endpoint is None else {
                "address": self.server_endpoint[0], "port": self.server_endpoint[1],
            },
            "associationStatus": self.association_status,
            "reconstructionStatus": self.reconstruction_status,
            "blockSize": {
                "status": self.option_status,
                "value": self.effective_block_size,
            },
            "terminalBlock": self.terminal_block,
            "packetRefIds": [item.id for item in self.packet_refs],
            "datagramIds": list(self.datagram_ids),
            "diagnosticCodes": list(self.diagnostics),
            "completePayloadLength": (
                self.complete_payload_length
                if self.complete_payload_length is not None
                else None if self.complete_payload is None else len(self.complete_payload)
            ),
            "integrity": "NOT-EVALUATED",
        }


@dataclass(frozen=True)
class ProtocolEvent:
    """A bounded, observed event; never a conformance verdict."""

    event_id: str
    event_type: str
    layer: str
    service_scope: str
    file_role: str | None
    transfer_id: str
    source_datagram_ids: tuple[str, ...]
    source_packet_ref_ids: tuple[str, ...]
    fields: dict[str, Any]
    evidence_status: str = "OBSERVED-OR-PARSED"

    def to_dict(self) -> dict[str, Any]:
        return {
            "eventId": self.event_id,
            "eventType": self.event_type,
            "layer": self.layer,
            "serviceScope": self.service_scope,
            "fileRole": self.file_role,
            "transferId": self.transfer_id,
            "sourceDatagramIds": list(self.source_datagram_ids),
            "sourcePacketRefIds": list(self.source_packet_ref_ids),
            "fields": self.fields,
            "evidenceStatus": self.evidence_status,
            "conformanceVerdict": "NOT-EVALUATED",
        }
