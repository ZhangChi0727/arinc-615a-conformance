"""Typed projection from bounded intake evidence to accepted development records.

The offline envelope remains the authoritative transport/report format for this
implementation slice.  This module is an explicit, versioned adapter for the
four accepted PR19 record shapes; it never fills unavailable values with zero
or guesses a role/TID/time merely to manufacture a contract instance.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from .identity import DEVELOPMENT_CONTRACT_PATH, DEVELOPMENT_CONTRACT_SHA256
from .models import DatagramRecord, PacketRef, ProtocolEvent, TransferRecord

if TYPE_CHECKING:  # pragma: no cover
    from .pipeline import IntakeResult


_CAPTURE_ID_RE = re.compile(r"^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2})$")


def project_development_records(result: "IntakeResult") -> dict[str, Any]:
    """Return validated-shape candidate records or explicit non-projectability.

    The caller/test suite validates every emitted ``payload`` with the public
    ``validate_record_instance`` entry point.  This adapter intentionally does
    not mutate the accepted contract or represent a non-projectable item as a
    fake compliant record.
    """
    projection = empty_contract_projection()
    records: list[dict[str, Any]] = projection["records"]
    unavailable: list[dict[str, str]] = projection["nonProjectable"]
    packet_ids: dict[str, str] = {}
    for packet in result.packet_refs:
        payload = _packet_payload(packet)
        if payload is None:
            unavailable.append({"sourceType": "PACKET-REF", "sourceId": packet.id, "reason": "TIMESTAMP-UNAVAILABLE"})
            continue
        packet_ids[packet.id] = _contract_packet_ref(packet)
        records.append({"recordType": "PACKET-REF", "sourceId": packet.id, "payload": payload})
    datagram_ids: dict[str, str] = {}
    for datagram in result.datagrams:
        payload = _datagram_payload(datagram, packet_ids)
        if payload is None:
            unavailable.append({"sourceType": "DATAGRAM-RECORD", "sourceId": datagram.datagram_id, "reason": "SOURCE-PACKET-NONPROJECTABLE"})
            continue
        datagram_ids[datagram.datagram_id] = f"dgram-{datagram.datagram_id}"
        records.append({"recordType": "DATAGRAM-RECORD", "sourceId": datagram.datagram_id, "payload": payload})
    transfer_event_ids: dict[str, str] = {}
    for transfer in result.transfers:
        request_event = _request_event_payload(transfer, packet_ids)
        if request_event is None:
            unavailable.append({"sourceType": "TRANSFER-RECORD", "sourceId": transfer.transfer_id, "reason": "REQUEST-OR-CONTEXT-NONPROJECTABLE"})
            continue
        request_id, request_payload = request_event
        records.append({"recordType": "PROTOCOL-EVENT", "sourceId": request_id, "payload": request_payload})
        transfer_event_ids[transfer.transfer_id] = request_id
        payload = _transfer_payload(transfer, packet_ids, request_id)
        if payload is None:
            unavailable.append({"sourceType": "TRANSFER-RECORD", "sourceId": transfer.transfer_id, "reason": "TID-OR-BLOCK-SOURCE-NONPROJECTABLE"})
            continue
        records.append({"recordType": "TRANSFER-RECORD", "sourceId": transfer.transfer_id, "payload": payload})
    for event in result.events:
        payload = _event_payload(event, packet_ids)
        if payload is None:
            unavailable.append({"sourceType": "PROTOCOL-EVENT", "sourceId": event.event_id, "reason": "RAW-SOURCE-NONPROJECTABLE"})
            continue
        records.append({"recordType": "PROTOCOL-EVENT", "sourceId": event.event_id, "payload": payload})
    return projection


def empty_contract_projection() -> dict[str, Any]:
    """Return the typed adapter envelope for a fatal pre-record failure."""
    return {
        "adapterVersion": "1.0",
        "contractIdentity": {
            "path": DEVELOPMENT_CONTRACT_PATH,
            "sha256": DEVELOPMENT_CONTRACT_SHA256,
            "version": "PR19-ACCEPTED-SNAPSHOT",
        },
        "records": [],
        "nonProjectable": [],
    }


def _packet_payload(packet: PacketRef) -> dict[str, Any] | None:
    if not _CAPTURE_ID_RE.fullmatch(packet.capture_id) or packet.timestamp is None:
        return None
    return {
        "captureId": packet.capture_id,
        "sectionId": packet.section_id,
        "interfaceId": packet.interface_id,
        "packetNumber": packet.packet_index,
        "rawTicks": packet.timestamp.ticks,
        "resolution": {"ticksPerSecond": packet.timestamp.ticks_per_second},
        "caplen": packet.captured_length,
        "origlen": packet.original_length,
        "decodeStatus": "FULL" if packet.captured_length == packet.original_length else "TRUNCATED",
    }


def _contract_packet_ref(packet: PacketRef) -> str:
    return f"{packet.capture_id}:{packet.section_id}:{packet.interface_id}:{packet.packet_index}"


def _datagram_payload(datagram: DatagramRecord, packet_ids: dict[str, str]) -> dict[str, Any] | None:
    references = [packet_ids.get(packet.id) for packet in datagram.packet_refs]
    coverage = [{"start": start, "endExclusive": end} for start, end in datagram.fragment_ranges if end > start]
    if any(reference is None for reference in references) or not coverage:
        return None
    return {
        "fragmentRefs": references,
        "coverage": coverage,
        "overlapStatus": "CONFLICT" if datagram.status == "CONFLICT" else "NONE",
        "reassemblyStatus": datagram.status,
    }


def _request_event_payload(transfer: TransferRecord, packet_ids: dict[str, str]) -> tuple[str, dict[str, Any]] | None:
    request_packet = transfer.request_packet_ref
    if (
        request_packet is None
        or request_packet.id not in packet_ids
        or transfer.request_kind not in {"RRQ", "WRQ"}
    ):
        return None
    event_id = f"event-request-{transfer.transfer_id}"
    return event_id, {
        "eventLayer": "WIRE",
        "role": "CLIENT",
        "payload": {"type": transfer.request_kind, "ref": f"payload-request-{transfer.transfer_id}"},
        "correlationKey": f"corr-{transfer.transfer_id}",
        "rawRefs": [packet_ids[request_packet.id]],
        "parseBoundary": "COMPLETE",
    }


def _transfer_payload(
    transfer: TransferRecord,
    packet_ids: dict[str, str],
    request_event_id: str,
) -> dict[str, Any] | None:
    if transfer.client_endpoint is None or transfer.server_endpoint is None:
        return None
    client_host, client_port = transfer.client_endpoint
    server_host, server_port = transfer.server_endpoint
    if server_port is None:
        return None
    block_map: dict[str, str] = {}
    for block, packet in sorted(transfer.block_packet_refs.items()):
        reference = packet_ids.get(packet.id)
        if reference is None:
            return None
        block_map[str(block)] = reference
    values = {} if transfer.option_status == "UNKNOWN" else {"blksize": transfer.effective_block_size}
    if transfer.option_status != "UNKNOWN" and transfer.effective_block_size is None:
        return None
    completion: list[str] = []
    if transfer.completion_packet_ref is not None:
        reference = packet_ids.get(transfer.completion_packet_ref.id)
        if reference is None:
            return None
        completion = [f"pkt-{reference}"]
    return {
        "direction": "SERVER-TO-CLIENT" if transfer.request_kind == "RRQ" else "CLIENT-TO-SERVER",
        "endpoints": {"client": client_host, "server": server_host},
        "tid": {"clientPort": client_port, "serverPort": server_port},
        "request": request_event_id,
        "optionState": {"mode": transfer.option_status, "values": values},
        "blockMap": block_map,
        "completionEvidence": completion,
    }


def _event_payload(event: ProtocolEvent, packet_ids: dict[str, str]) -> dict[str, Any] | None:
    raw_refs = [packet_ids.get(value) for value in event.source_packet_ref_ids]
    if not raw_refs or any(value is None for value in raw_refs):
        return None
    parse_status = event.fields.get("parseStatus") if isinstance(event.fields, dict) else None
    boundary = {
        "PARSED": "COMPLETE",
        "PARTIAL": "PARTIAL",
        "OPAQUE": "OPAQUE",
        "MALFORMED": "ERROR",
    }.get(parse_status, "COMPLETE" if event.layer == "WIRE" else "OPAQUE")
    return {
        "eventLayer": event.layer,
        "role": "CLIENT" if event.layer == "WIRE" else "UNKNOWN",
        "payload": {"type": event.event_type, "ref": f"payload-{event.event_id}"},
        "correlationKey": f"corr-{event.transfer_id}",
        "rawRefs": raw_refs,
        "parseBoundary": boundary,
    }
