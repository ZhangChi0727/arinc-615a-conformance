"""Bounded Ethernet/IPv4/UDP decoding and fragment reconstruction."""

from __future__ import annotations

import ipaddress
import struct
from collections import OrderedDict
from dataclasses import dataclass, field

from .models import DatagramRecord, Ipv4Fragment, PacketRef, UdpDatagram


ETHERNET_LINKTYPE = 1
ETHERTYPE_IPV4 = 0x0800
VLAN_ETHERTYPES = {0x8100, 0x88A8, 0x9100}
UDP_PROTOCOL = 17


class PacketDecodeError(ValueError):
    """A per-packet decoding error with a stable code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def extract_ipv4(packet_ref: PacketRef, data: bytes) -> Ipv4Fragment | None:
    """Decode supported Ethernet/VLAN/IPv4 framing without guessing offsets."""
    if packet_ref.link_type != ETHERNET_LINKTYPE:
        raise PacketDecodeError(
            "UNSUPPORTED-LINKTYPE", f"linktype {packet_ref.link_type} is not supported"
        )
    if len(data) < 14:
        raise PacketDecodeError("TRUNCATED-ETHERNET", "ethernet header is truncated")
    cursor = 12
    ethertype = struct.unpack("!H", data[cursor:cursor + 2])[0]
    cursor += 2
    vlan_tags: list[int] = []
    while ethertype in VLAN_ETHERTYPES:
        if len(vlan_tags) >= 4:
            raise PacketDecodeError("VLAN-DEPTH-LIMIT", "more than four VLAN tags are unsupported")
        if len(data) < cursor + 4:
            raise PacketDecodeError("TRUNCATED-VLAN", "VLAN header is truncated")
        tci, ethertype = struct.unpack("!HH", data[cursor:cursor + 4])
        vlan_tags.append(tci & 0x0FFF)
        cursor += 4
    if ethertype != ETHERTYPE_IPV4:
        return None
    if len(data) < cursor + 20:
        raise PacketDecodeError("TRUNCATED-IPV4-HEADER", "IPv4 header is truncated")
    version_ihl = data[cursor]
    version = version_ihl >> 4
    ihl = (version_ihl & 0x0F) * 4
    if version != 4:
        raise PacketDecodeError("INVALID-IP-VERSION", "Ethernet payload is not IPv4")
    if ihl < 20:
        raise PacketDecodeError("INVALID-IPV4-IHL", "IPv4 IHL is below the minimum")
    if len(data) < cursor + ihl:
        raise PacketDecodeError("TRUNCATED-IPV4-HEADER", "IPv4 options are truncated")
    total_length = struct.unpack("!H", data[cursor + 2:cursor + 4])[0]
    if total_length < ihl:
        raise PacketDecodeError("INVALID-IPV4-TOTAL-LENGTH", "IPv4 total length is below IHL")
    if len(data) < cursor + total_length:
        raise PacketDecodeError(
            "TRUNCATED-IPV4-PAYLOAD", "captured IPv4 payload is shorter than total length"
        )
    identification = struct.unpack("!H", data[cursor + 4:cursor + 6])[0]
    flags_offset = struct.unpack("!H", data[cursor + 6:cursor + 8])[0]
    if flags_offset & 0x8000:
        raise PacketDecodeError("INVALID-IPV4-FLAGS", "IPv4 reserved flag is set")
    more_fragments = bool(flags_offset & 0x2000)
    fragment_offset = (flags_offset & 0x1FFF) * 8
    protocol = data[cursor + 9]
    source = str(ipaddress.IPv4Address(data[cursor + 12:cursor + 16]))
    destination = str(ipaddress.IPv4Address(data[cursor + 16:cursor + 20]))
    payload = data[cursor + ihl:cursor + total_length]
    if more_fragments and len(payload) % 8:
        raise PacketDecodeError(
            "INVALID-IPV4-FRAGMENT-LENGTH",
            "a non-final IPv4 fragment payload must be an eight-byte multiple",
        )
    return Ipv4Fragment(
        packet_ref=packet_ref,
        source=source,
        destination=destination,
        identification=identification,
        protocol=protocol,
        fragment_offset=fragment_offset,
        more_fragments=more_fragments,
        payload=payload,
        vlan_tags=tuple(vlan_tags),
    )


def decode_udp(datagram: DatagramRecord) -> UdpDatagram:
    """Decode UDP only from a complete IPv4 datagram with exact length bounds."""
    if datagram.payload is None:
        raise PacketDecodeError("UDP-WITHOUT-PAYLOAD", "datagram has no complete payload")
    if len(datagram.payload) < 8:
        raise PacketDecodeError("TRUNCATED-UDP-HEADER", "UDP header is truncated")
    source_port, destination_port, length, checksum = struct.unpack(
        "!HHHH", datagram.payload[:8]
    )
    if length < 8:
        raise PacketDecodeError("INVALID-UDP-LENGTH", "UDP length is below the header size")
    if length > len(datagram.payload):
        raise PacketDecodeError("TRUNCATED-UDP-PAYLOAD", "UDP length exceeds reconstructed payload")
    if length != len(datagram.payload):
        raise PacketDecodeError("UDP-LENGTH-MISMATCH", "UDP length leaves unexplained IPv4 bytes")
    return UdpDatagram(
        datagram=datagram,
        source_port=source_port,
        destination_port=destination_port,
        payload=datagram.payload[8:],
        checksum_present=checksum != 0,
    )


@dataclass
class _Accumulator:
    fragment: Ipv4Fragment
    bytes_by_offset: dict[int, int] = field(default_factory=dict)
    packet_refs: list[PacketRef] = field(default_factory=list)
    ranges: set[tuple[int, int]] = field(default_factory=set)
    terminal_end: int | None = None
    vlan_tags: tuple[int, ...] = ()
    fragment_count: int = 0

    @property
    def key(self) -> tuple[str, int, str, str, int, int]:
        return self.fragment.key

    @property
    def latest_end(self) -> int:
        return max((end for _start, end in self.ranges), default=0)


class Ipv4Reassembler:
    """Finite, byte-precise IPv4 reconstruction.

    Conflicting overlaps are terminal evidence for that datagram: no later
    fragment can overwrite the earlier bytes.  EOF or a resource eviction
    emits a GAPPED record instead of silently discarding its provenance.
    """

    def __init__(
        self,
        *,
        max_active_datagrams: int = 128,
        max_datagram_bytes: int = 65_535,
        max_fragments_per_datagram: int = 8_192,
    ) -> None:
        if (
            max_active_datagrams < 1
            or max_datagram_bytes < 1
            or max_fragments_per_datagram < 1
        ):
            raise ValueError("reassembly limits must be positive")
        self.max_active_datagrams = max_active_datagrams
        self.max_datagram_bytes = min(max_datagram_bytes, 65_535)
        self.max_fragments_per_datagram = max_fragments_per_datagram
        self._active: OrderedDict[tuple[str, int, str, str, int, int], _Accumulator] = OrderedDict()
        self._sequence = 0

    def add(self, fragment: Ipv4Fragment) -> list[DatagramRecord]:
        """Add a fragment and return any completed/terminated records."""
        results: list[DatagramRecord] = []
        key = fragment.key
        accumulator = self._active.get(key)
        # The overwhelmingly common IPv4 case is a complete, unfragmented
        # datagram.  It has no overlap or gap relation to resolve, so avoid a
        # byte-at-a-time accumulator while retaining exactly the same source
        # range and finite byte-bound semantics.  A pending fragment set with
        # the same key still follows the conservative accumulator path below.
        if accumulator is None and fragment.fragment_offset == 0 and not fragment.more_fragments:
            end = len(fragment.payload)
            standalone = _Accumulator(
                fragment=fragment,
                packet_refs=[fragment.packet_ref],
                ranges={(0, end)},
                terminal_end=end,
                vlan_tags=fragment.vlan_tags,
                fragment_count=1,
            )
            if end > self.max_datagram_bytes:
                return [self._gapped(standalone, "RESOURCE-DATAGRAM-BYTE-LIMIT")]
            return [self._record(standalone, "COMPLETE", None, payload=fragment.payload)]
        if accumulator is None:
            if len(self._active) >= self.max_active_datagrams:
                _old_key, old = self._active.popitem(last=False)
                results.append(self._gapped(old, "RESOURCE-ACTIVE-DATAGRAM-LIMIT"))
            accumulator = _Accumulator(fragment=fragment, vlan_tags=fragment.vlan_tags)
            self._active[key] = accumulator
        else:
            self._active.move_to_end(key)
        start = fragment.fragment_offset
        end = start + len(fragment.payload)
        accumulator.fragment_count += 1
        if accumulator.fragment_count > self.max_fragments_per_datagram:
            self._active.pop(key, None)
            accumulator.packet_refs.append(fragment.packet_ref)
            accumulator.ranges.add((start, end))
            results.append(self._gapped(accumulator, "RESOURCE-FRAGMENT-COUNT-LIMIT"))
            return results
        if end > self.max_datagram_bytes:
            self._active.pop(key, None)
            accumulator.packet_refs.append(fragment.packet_ref)
            accumulator.ranges.add((start, end))
            results.append(self._gapped(accumulator, "RESOURCE-DATAGRAM-BYTE-LIMIT"))
            return results
        if accumulator.terminal_end is not None and end > accumulator.terminal_end:
            self._active.pop(key, None)
            accumulator.packet_refs.append(fragment.packet_ref)
            accumulator.ranges.add((start, end))
            results.append(self._conflict(accumulator, [(accumulator.terminal_end, end)]))
            return results
        if not fragment.more_fragments:
            if accumulator.terminal_end is not None and accumulator.terminal_end != end:
                self._active.pop(key, None)
                accumulator.packet_refs.append(fragment.packet_ref)
                accumulator.ranges.add((start, end))
                results.append(self._conflict(
                    accumulator, [(min(accumulator.terminal_end, end), max(accumulator.terminal_end, end))]
                ))
                return results
            if accumulator.latest_end > end:
                self._active.pop(key, None)
                accumulator.packet_refs.append(fragment.packet_ref)
                accumulator.ranges.add((start, end))
                results.append(self._conflict(accumulator, [(end, accumulator.latest_end)]))
                return results
            accumulator.terminal_end = end
        conflict_offsets: list[int] = []
        for position, value in enumerate(fragment.payload, start):
            previous = accumulator.bytes_by_offset.get(position)
            if previous is not None and previous != value:
                conflict_offsets.append(position)
        accumulator.packet_refs.append(fragment.packet_ref)
        accumulator.ranges.add((start, end))
        if conflict_offsets:
            self._active.pop(key, None)
            results.append(self._conflict(accumulator, _ranges_from_positions(conflict_offsets)))
            return results
        for position, value in enumerate(fragment.payload, start):
            accumulator.bytes_by_offset.setdefault(position, value)
        if accumulator.terminal_end is not None and self._is_complete(accumulator):
            self._active.pop(key, None)
            results.append(self._complete_record(accumulator))
        return results

    def finish(self, reason: str = "INCOMPLETE-DATAGRAM") -> list[DatagramRecord]:
        """Flush EOF/age-limited accumulators as explicit GAPPED evidence."""
        results = [self._gapped(item, reason) for item in self._active.values()]
        self._active.clear()
        return results

    def _is_complete(self, accumulator: _Accumulator) -> bool:
        assert accumulator.terminal_end is not None
        return (
            accumulator.terminal_end > 0
            and len(accumulator.bytes_by_offset) == accumulator.terminal_end
            and 0 in accumulator.bytes_by_offset
        )

    def _record_id(self) -> str:
        self._sequence += 1
        return f"DG-{self._sequence:08d}"

    def _complete_record(self, accumulator: _Accumulator) -> DatagramRecord:
        assert accumulator.terminal_end is not None
        payload = bytes(accumulator.bytes_by_offset[index] for index in range(accumulator.terminal_end))
        return self._record(accumulator, "COMPLETE", None, payload=payload)

    def _gapped(self, accumulator: _Accumulator, reason: str) -> DatagramRecord:
        end = accumulator.terminal_end if accumulator.terminal_end is not None else accumulator.latest_end
        missing = _missing_ranges(accumulator.bytes_by_offset, end)
        return self._record(accumulator, "GAPPED", reason, missing_ranges=missing)

    def _conflict(self, accumulator: _Accumulator, ranges: list[tuple[int, int]]) -> DatagramRecord:
        return self._record(accumulator, "CONFLICT", "CONFLICTING-FRAGMENT-BYTES", conflict_ranges=ranges)

    def _record(
        self,
        accumulator: _Accumulator,
        status: str,
        failure_code: str | None,
        *,
        payload: bytes | None = None,
        missing_ranges: list[tuple[int, int]] | None = None,
        conflict_ranges: list[tuple[int, int]] | None = None,
    ) -> DatagramRecord:
        fragment = accumulator.fragment
        return DatagramRecord(
            datagram_id=self._record_id(),
            capture_id=fragment.packet_ref.capture_id,
            interface_id=fragment.packet_ref.interface_id,
            source=fragment.source,
            destination=fragment.destination,
            protocol=fragment.protocol,
            identification=fragment.identification,
            status=status,
            failure_code=failure_code,
            packet_refs=list(accumulator.packet_refs),
            fragment_ranges=sorted(accumulator.ranges),
            missing_ranges=missing_ranges or [],
            conflict_ranges=conflict_ranges or [],
            payload=payload,
            payload_length=None if payload is None else len(payload),
            vlan_tags=accumulator.vlan_tags,
        )


def _ranges_from_positions(positions: list[int]) -> list[tuple[int, int]]:
    if not positions:
        return []
    values = sorted(set(positions))
    result: list[tuple[int, int]] = []
    start = previous = values[0]
    for value in values[1:]:
        if value == previous + 1:
            previous = value
            continue
        result.append((start, previous + 1))
        start = previous = value
    result.append((start, previous + 1))
    return result


def _missing_ranges(values: dict[int, int], end: int) -> list[tuple[int, int]]:
    if end <= 0:
        return []
    missing: list[int] = [index for index in range(end) if index not in values]
    return _ranges_from_positions(missing)
