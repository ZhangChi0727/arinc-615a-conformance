"""Streaming pcap/pcapng container intake with explicit metadata uncertainty."""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import BinaryIO, Iterator

from .models import CapturedPacket, Diagnostic, PacketRef, Timestamp


PCAPNG_SECTION_HEADER = 0x0A0D0D0A
PCAPNG_INTERFACE_DESCRIPTION = 0x00000001
PCAPNG_SIMPLE_PACKET = 0x00000003
PCAPNG_ENHANCED_PACKET = 0x00000006
PCAPNG_KNOWN_NON_PACKET_BLOCKS = {
    0x00000004,  # Name Resolution Block
    0x00000005,  # Interface Statistics Block
    0x0000000A,  # Decryption Secrets Block
    0x0000000B,  # Custom Block
    0x40000BAD,  # Custom Block (copyable)
}


class CaptureFormatError(ValueError):
    """A fatal capture/container condition that cannot yield a reliable index."""

    def __init__(self, code: str, message: str, offset: int | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.offset = offset


@dataclass(frozen=True)
class InterfaceMetadata:
    section_id: int
    interface_id: int
    link_type: int
    snap_length: int
    ticks_per_second: int
    offset_seconds: int
    clock_domain: str

    def to_dict(self) -> dict[str, object]:
        return {
            "sectionId": self.section_id,
            "interfaceId": self.interface_id,
            "linkType": self.link_type,
            "snapLength": self.snap_length,
            "ticksPerSecond": self.ticks_per_second,
            "offsetSeconds": self.offset_seconds,
            "clockDomain": self.clock_domain,
            "clockAccuracy": "UNKNOWN",
        }


@dataclass
class CaptureMetadata:
    """Metadata collected while streaming one input file."""

    container_format: str = "UNKNOWN"
    byte_order: str = "UNKNOWN"
    interfaces: dict[int, InterfaceMetadata] = field(default_factory=dict)
    packet_count: int = 0
    diagnostics: list[Diagnostic] = field(default_factory=list)

    @property
    def has_controlled_issue(self) -> bool:
        return bool(self.diagnostics)

    def to_dict(self) -> dict[str, object]:
        return {
            "containerFormat": self.container_format,
            "byteOrder": self.byte_order,
            "interfaces": [
                item.to_dict() for _, item in sorted(self.interfaces.items())
            ],
            "containerPacketCount": self.packet_count,
        }


class CaptureReader:
    """Lazily read one pcap/pcapng file under explicit resource bounds."""

    def __init__(
        self,
        path: Path,
        capture_id: str,
        *,
        max_packet_bytes: int = 2 * 1024 * 1024,
        max_block_bytes: int = 4 * 1024 * 1024,
        max_interfaces: int = 1_024,
        max_diagnostics: int = 50_000,
    ) -> None:
        self.path = path
        self.capture_id = capture_id
        self.max_packet_bytes = max_packet_bytes
        self.max_block_bytes = max_block_bytes
        self.max_interfaces = max_interfaces
        self.max_diagnostics = max_diagnostics
        self.metadata = CaptureMetadata()
        self._metadata_diagnostic_limit_reported = False

    def __iter__(self) -> Iterator[CapturedPacket]:
        try:
            with self.path.open("rb") as stream:
                magic = stream.read(4)
                stream.seek(0)
                if magic == PCAPNG_SECTION_HEADER.to_bytes(4, "big"):
                    yield from self._pcapng_packets(stream)
                elif magic in {
                    b"\xd4\xc3\xb2\xa1", b"\xa1\xb2\xc3\xd4",
                    b"\x4d\x3c\xb2\xa1", b"\xa1\xb2\x3c\x4d",
                }:
                    yield from self._pcap_packets(stream)
                else:
                    raise CaptureFormatError(
                        "UNSUPPORTED-CAPTURE-CONTAINER",
                        "input is neither a supported pcap nor pcapng container",
                        0,
                    )
        except OSError as exc:
            raise CaptureFormatError("CAPTURE-READ-ERROR", str(exc)) from exc

    def _pcap_packets(self, stream: BinaryIO) -> Iterator[CapturedPacket]:
        offset = 0
        header = _read_exact(stream, 24, "TRUNCATED-PCAP-GLOBAL-HEADER", offset)
        magic = header[:4]
        if magic == b"\xd4\xc3\xb2\xa1":
            endian, resolution = "<", 1_000_000
        elif magic == b"\xa1\xb2\xc3\xd4":
            endian, resolution = ">", 1_000_000
        elif magic == b"\x4d\x3c\xb2\xa1":
            endian, resolution = "<", 1_000_000_000
        elif magic == b"\xa1\xb2\x3c\x4d":
            endian, resolution = ">", 1_000_000_000
        else:  # pragma: no cover - dispatched before this method
            raise CaptureFormatError("UNSUPPORTED-PCAP-MAGIC", "unsupported pcap magic", 0)
        _major, _minor, _zone, _sigfigs, snaplen, link_type = struct.unpack(
            f"{endian}HHIIII", header[4:]
        )
        if snaplen <= 0:
            raise CaptureFormatError("INVALID-PCAP-SNAPLEN", "pcap snaplen must be positive", 16)
        self.metadata = CaptureMetadata(
            container_format="PCAP",
            byte_order="LITTLE" if endian == "<" else "BIG",
            interfaces={0: InterfaceMetadata(
                section_id=0, interface_id=0,
                link_type=link_type,
                snap_length=snaplen,
                ticks_per_second=resolution,
                offset_seconds=0,
                clock_domain="PCAP-GLOBAL-CLOCK-UNASSESSED",
            )},
        )
        offset = 24
        packet_index = 0
        while True:
            record_start = offset
            record_header = stream.read(16)
            if not record_header:
                break
            if len(record_header) != 16:
                raise CaptureFormatError(
                    "TRUNCATED-PCAP-PACKET-HEADER", "pcap packet header is truncated", record_start
                )
            ts_sec, ts_fraction, included_length, original_length = struct.unpack(
                f"{endian}IIII", record_header
            )
            if ts_fraction >= resolution:
                raise CaptureFormatError(
                    "INVALID-PCAP-TIMESTAMP-FRACTION",
                    "pcap timestamp fraction exceeds its declared resolution",
                    record_start,
                )
            offset += 16
            if included_length > self.max_packet_bytes:
                self._add_metadata_diagnostic(Diagnostic(
                    "PACKET-RESOURCE-LIMIT", "CAPTURE",
                    "pcap packet exceeds configured capture-byte limit",
                    packet_ref_id=f"{self.capture_id}:P{packet_index + 1:08d}",
                    container_offset=record_start,
                    detail={"includedLength": included_length, "limit": self.max_packet_bytes},
                ))
                _skip_exact(stream, included_length, "TRUNCATED-PCAP-PACKET", offset)
                offset += included_length
                packet_index += 1
                self.metadata.packet_count += 1
                continue
            data = _read_exact(stream, included_length, "TRUNCATED-PCAP-PACKET", offset)
            offset += included_length
            packet_index += 1
            self.metadata.packet_count += 1
            timestamp = Timestamp(
                ticks=ts_sec * resolution + ts_fraction,
                ticks_per_second=resolution,
                clock_domain="PCAP-GLOBAL-CLOCK-UNASSESSED",
            )
            yield CapturedPacket(
                PacketRef(
                    self.capture_id, packet_index, record_start, 0, link_type,
                    included_length, original_length, timestamp,
                    section_id=0, link_domain="PCAP-SECTION-0-INTERFACE-0",
                ),
                data,
            )

    def _pcapng_packets(self, stream: BinaryIO) -> Iterator[CapturedPacket]:
        offset = 0
        endian: str | None = None
        interface_sequence = 0
        global_interface_id = 0
        section_index = -1
        local_interfaces: dict[int, InterfaceMetadata] = {}
        packet_index = 0
        self.metadata = CaptureMetadata(container_format="PCAPNG")
        while True:
            block_start = offset
            header = stream.read(8)
            if not header:
                break
            if len(header) != 8:
                raise CaptureFormatError(
                    "TRUNCATED-PCAPNG-BLOCK-HEADER", "pcapng block header is truncated", block_start
                )
            raw_type = header[:4]
            if raw_type == PCAPNG_SECTION_HEADER.to_bytes(4, "big"):
                bom = _read_exact(stream, 4, "TRUNCATED-PCAPNG-SHB", block_start + 8)
                if int.from_bytes(bom, "little") == 0x1A2B3C4D:
                    endian = "<"
                elif int.from_bytes(bom, "big") == 0x1A2B3C4D:
                    endian = ">"
                else:
                    raise CaptureFormatError(
                        "INVALID-PCAPNG-BYTE-ORDER", "pcapng section has no valid byte-order magic", block_start
                    )
                total_length = struct.unpack(f"{endian}I", header[4:])[0]
                _validate_block_length(total_length, self.max_block_bytes, block_start)
                if total_length < 28:
                    raise CaptureFormatError(
                        "INVALID-PCAPNG-SHB",
                        "pcapng section header is shorter than its fixed fields",
                        block_start,
                    )
                remaining = _read_exact(
                    stream, total_length - 12, "TRUNCATED-PCAPNG-SHB", block_start + 12
                )
                if struct.unpack(f"{endian}I", remaining[-4:])[0] != total_length:
                    raise CaptureFormatError(
                        "PCAPNG-BLOCK-LENGTH-MISMATCH", "pcapng section block length disagrees", block_start
                    )
                offset += total_length
                self.metadata.byte_order = "LITTLE" if endian == "<" else "BIG"
                section_index += 1
                local_interfaces = {}
                interface_sequence = 0
                continue
            if endian is None:
                raise CaptureFormatError(
                    "PCAPNG-MISSING-SECTION-HEADER", "pcapng packet appears before a section header", block_start
                )
            block_type, total_length = struct.unpack(f"{endian}II", header)
            _validate_block_length(total_length, self.max_block_bytes, block_start)
            remainder = _read_exact(
                stream, total_length - 8, "TRUNCATED-PCAPNG-BLOCK", block_start + 8
            )
            if struct.unpack(f"{endian}I", remainder[-4:])[0] != total_length:
                raise CaptureFormatError(
                    "PCAPNG-BLOCK-LENGTH-MISMATCH", "pcapng block length disagrees", block_start
                )
            body = remainder[:-4]
            offset += total_length
            if block_type == PCAPNG_INTERFACE_DESCRIPTION:
                if len(self.metadata.interfaces) >= self.max_interfaces:
                    raise CaptureFormatError(
                        "RESOURCE-INTERFACE-LIMIT",
                        "pcapng interface count exceeds configured bound",
                        block_start,
                    )
                interface = _parse_interface_description(
                    body, endian, section_index, global_interface_id, block_start,
                    clock_domain=f"PCAPNG-SECTION-{section_index}-INTERFACE-{interface_sequence}-UNASSESSED",
                )
                self.metadata.interfaces[global_interface_id] = interface
                local_interfaces[interface_sequence] = interface
                interface_sequence += 1
                global_interface_id += 1
                continue
            if block_type == PCAPNG_ENHANCED_PACKET:
                if len(body) < 20:
                    raise CaptureFormatError(
                        "INVALID-PCAPNG-ENHANCED-PACKET", "enhanced packet block is too short", block_start
                    )
                interface_id, high, low, captured_length, original_length = struct.unpack(
                    f"{endian}IIIII", body[:20]
                )
                interface = local_interfaces.get(interface_id)
                if interface is None:
                    raise CaptureFormatError(
                        "PCAPNG-UNKNOWN-INTERFACE", "enhanced packet references an unknown interface", block_start
                    )
                padded = _padded_length(captured_length)
                if len(body) < 20 + padded:
                    raise CaptureFormatError(
                        "INVALID-PCAPNG-ENHANCED-LENGTH", "enhanced packet length is inconsistent", block_start
                    )
                _parse_options(body[20 + padded:], endian, block_start + 28 + padded)
                packet_index += 1
                self.metadata.packet_count += 1
                if captured_length > self.max_packet_bytes:
                    self._add_metadata_diagnostic(Diagnostic(
                        "PACKET-RESOURCE-LIMIT", "CAPTURE",
                        "pcapng packet exceeds configured capture-byte limit",
                        packet_ref_id=f"{self.capture_id}:P{packet_index:08d}",
                        container_offset=block_start,
                        detail={"capturedLength": captured_length, "limit": self.max_packet_bytes},
                    ))
                    continue
                timestamp = Timestamp(
                    ticks=(high << 32) | low,
                    ticks_per_second=interface.ticks_per_second,
                    offset_seconds=interface.offset_seconds,
                    clock_domain=interface.clock_domain,
                )
                yield CapturedPacket(
                    PacketRef(
                        self.capture_id, packet_index, block_start, interface.interface_id,
                        interface.link_type, captured_length, original_length, timestamp,
                        section_id=interface.section_id, link_domain=interface.clock_domain,
                    ),
                    body[20:20 + captured_length],
                )
                continue
            if block_type == PCAPNG_SIMPLE_PACKET:
                if len(body) < 4:
                    raise CaptureFormatError(
                        "INVALID-PCAPNG-SIMPLE-PACKET", "simple packet block is too short", block_start
                    )
                interface = local_interfaces.get(0)
                if interface is None:
                    raise CaptureFormatError(
                        "PCAPNG-UNKNOWN-INTERFACE", "simple packet has no interface zero", block_start
                    )
                original_length = struct.unpack(f"{endian}I", body[:4])[0]
                payload = body[4:]
                captured_length = min(original_length, len(payload))
                packet_index += 1
                self.metadata.packet_count += 1
                if captured_length > self.max_packet_bytes:
                    self._add_metadata_diagnostic(Diagnostic(
                        "PACKET-RESOURCE-LIMIT", "CAPTURE",
                        "simple packet exceeds configured capture-byte limit",
                        packet_ref_id=f"{self.capture_id}:P{packet_index:08d}",
                        container_offset=block_start,
                        detail={"capturedLength": captured_length, "limit": self.max_packet_bytes},
                    ))
                    continue
                self._add_metadata_diagnostic(Diagnostic(
                    "PACKET-TIMESTAMP-UNKNOWN", "CAPTURE",
                    "pcapng simple packet has no timestamp", severity="WARNING",
                    packet_ref_id=f"{self.capture_id}:P{packet_index:08d}", container_offset=block_start,
                ))
                yield CapturedPacket(
                    PacketRef(
                        self.capture_id, packet_index, block_start, interface.interface_id, interface.link_type,
                        captured_length, original_length, None,
                        section_id=interface.section_id, link_domain=interface.clock_domain,
                    ),
                    payload[:captured_length],
                )
                continue
            if block_type not in PCAPNG_KNOWN_NON_PACKET_BLOCKS:
                self._add_metadata_diagnostic(Diagnostic(
                    "UNSUPPORTED-PCAPNG-BLOCK", "CAPTURE",
                    "pcapng contains a block type not interpreted by this bounded intake",
                    severity="WARNING", container_offset=block_start,
                    detail={"blockType": f"0x{block_type:08X}"},
                ))

    def _add_metadata_diagnostic(self, diagnostic: Diagnostic) -> None:
        """Bound retained container diagnostics, reserving a truncation witness."""
        if len(self.metadata.diagnostics) < self.max_diagnostics - 1:
            self.metadata.diagnostics.append(diagnostic)
            return
        if not self._metadata_diagnostic_limit_reported:
            self._metadata_diagnostic_limit_reported = True
            self.metadata.diagnostics.append(Diagnostic(
                "RESOURCE-CAPTURE-DIAGNOSTIC-LIMIT",
                "CAPTURE",
                "capture diagnostics were bounded; later container issues were not retained",
                detail={"limit": self.max_diagnostics},
            ))


def _read_exact(stream: BinaryIO, size: int, code: str, offset: int) -> bytes:
    data = stream.read(size)
    if len(data) != size:
        raise CaptureFormatError(code, "capture ended before declared record length", offset)
    return data


def _skip_exact(stream: BinaryIO, size: int, code: str, offset: int) -> None:
    remaining = size
    while remaining:
        chunk = stream.read(min(remaining, 1024 * 1024))
        if not chunk:
            raise CaptureFormatError(code, "capture ended before declared record length", offset)
        remaining -= len(chunk)


def _validate_block_length(total_length: int, max_block_bytes: int, offset: int) -> None:
    if total_length < 12 or total_length % 4:
        raise CaptureFormatError(
            "INVALID-PCAPNG-BLOCK-LENGTH", "pcapng block length is invalid", offset
        )
    if total_length > max_block_bytes:
        raise CaptureFormatError(
            "PCAPNG-BLOCK-RESOURCE-LIMIT", "pcapng block exceeds configured bound", offset
        )


def _padded_length(length: int) -> int:
    return length + (-length % 4)


def _parse_options(data: bytes, endian: str, offset: int) -> None:
    """Validate and intentionally discard legal pcapng option payloads.

    Comments and other options may contain local/sensitive content.  The
    bounded intake preserves only structural validity, never their text.
    """
    cursor = 0
    while cursor < len(data):
        if cursor + 4 > len(data):
            raise CaptureFormatError(
                "INVALID-PCAPNG-OPTION", "pcapng option header is truncated", offset + cursor
            )
        code, length = struct.unpack(f"{endian}HH", data[cursor:cursor + 4])
        cursor += 4
        if code == 0:
            if length != 0 or cursor != len(data):
                raise CaptureFormatError(
                    "INVALID-PCAPNG-OPTION", "pcapng option end marker is invalid", offset + cursor - 4
                )
            return
        padded = _padded_length(length)
        if cursor + padded > len(data):
            raise CaptureFormatError(
                "INVALID-PCAPNG-OPTION", "pcapng option payload is truncated", offset + cursor
            )
        cursor += padded


def _parse_interface_description(
    body: bytes, endian: str, section_id: int, interface_id: int, offset: int, *, clock_domain: str,
) -> InterfaceMetadata:
    if len(body) < 8:
        raise CaptureFormatError(
            "INVALID-PCAPNG-INTERFACE", "interface description is too short", offset
        )
    link_type, _reserved, snap_length = struct.unpack(f"{endian}HHI", body[:8])
    if snap_length < 0:  # unsigned field; retain an explicit defensive boundary.
        raise CaptureFormatError(
            "INVALID-PCAPNG-SNAPLEN", "interface snap length is invalid", offset
        )
    ticks_per_second = 1_000_000
    offset_seconds = 0
    cursor = 8
    while cursor < len(body):
        if cursor + 4 > len(body):
            raise CaptureFormatError(
                "INVALID-PCAPNG-OPTION", "pcapng option header is truncated", offset + cursor
            )
        code, length = struct.unpack(f"{endian}HH", body[cursor:cursor + 4])
        cursor += 4
        if code == 0:
            if length != 0:
                raise CaptureFormatError(
                    "INVALID-PCAPNG-OPTION", "pcapng option end marker has a value", offset + cursor - 4
                )
            break
        padded = _padded_length(length)
        if cursor + padded > len(body):
            raise CaptureFormatError(
                "INVALID-PCAPNG-OPTION", "pcapng option payload is truncated", offset + cursor
            )
        value = body[cursor:cursor + length]
        cursor += padded
        if code == 9:  # if_tsresol
            if length != 1:
                raise CaptureFormatError(
                    "INVALID-PCAPNG-TSRESOL", "if_tsresol must have one byte", offset
                )
            exponent = value[0]
            if exponent & 0x80:
                ticks_per_second = 2 ** (exponent & 0x7F)
            else:
                # Enormous decimal exponents are neither usable nor faithfully
                # serialisable in this bounded tool.
                if exponent > 18:
                    raise CaptureFormatError(
                        "UNSUPPORTED-PCAPNG-TSRESOL", "if_tsresol exponent exceeds supported bound", offset
                    )
                ticks_per_second = 10 ** exponent
        elif code == 14:  # if_tsoffset
            if length != 8:
                raise CaptureFormatError(
                    "INVALID-PCAPNG-TSOFFSET", "if_tsoffset must have eight bytes", offset
                )
            offset_seconds = struct.unpack(f"{endian}q", value)[0]
    return InterfaceMetadata(
        section_id=section_id, interface_id=interface_id,
        link_type=link_type,
        snap_length=snap_length,
        ticks_per_second=ticks_per_second,
        offset_seconds=offset_seconds,
        clock_domain=clock_domain,
    )
