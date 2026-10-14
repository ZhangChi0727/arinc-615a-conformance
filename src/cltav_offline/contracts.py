"""Typed projection from bounded intake evidence to accepted development records.

The offline envelope remains the authoritative transport/report format for this
implementation slice.  This module is an explicit, versioned adapter for the
four accepted PR19 record shapes; it never fills unavailable values with zero
or guesses a role/TID/time merely to manufacture a contract instance.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from .controlled_resources import ControlledResourceError
from .development_contract import accepted_record_contracts, record_instance_errors
from .identity import DEVELOPMENT_CONTRACT_PATH, DEVELOPMENT_CONTRACT_SHA256
from .models import DatagramRecord, PacketRef, ProtocolEvent, TransferRecord

if TYPE_CHECKING:  # pragma: no cover
    from .pipeline import IntakeResult


_CAPTURE_ID_RE = re.compile(r"^(?:cap-[a-z0-9][a-z0-9-]*|HC-[0-9]{2})$")
_PROJECTED_TYPES = frozenset({"PACKET-REF", "DATAGRAM-RECORD", "TRANSFER-RECORD", "PROTOCOL-EVENT"})


class ContractProjectionError(ValueError):
    """The bounded adapter cannot make a valid controlled-contract claim."""

    def __init__(self, errors: list[str]) -> None:
        super().__init__("; ".join(errors))
        self.errors = errors


def project_development_records(result: "IntakeResult") -> dict[str, Any]:
    """Return validated-shape candidate records or explicit non-projectability.

    The caller/test suite validates every emitted ``payload`` with the public
    ``validate_record_instance`` entry point.  This adapter intentionally does
    not mutate the accepted contract or represent a non-projectable item as a
    fake compliant record.
    """
    # Load the exact bound snapshot before constructing any claim.  A missing,
    # changed, or schema-invalid packaged resource is a tool failure, not a
    # non-projectable capture observation.
    accepted_record_contracts()
    projection = empty_contract_projection()
    records: list[dict[str, Any]] = projection["records"]
    unavailable: list[dict[str, str]] = projection["nonProjectable"]
    packet_ids: dict[str, str] = {}
    for packet in result.packet_refs:
        payload = _packet_payload(packet)
        if payload is None:
            unavailable.append({
                "sourceType": "PACKET-REF", "sourceId": packet.id,
                "reason": _packet_nonprojectable_reason(packet),
            })
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
    errors = projection_errors(projection)
    if errors:
        raise ContractProjectionError(errors)
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
    if _packet_nonprojectable_reason(packet):
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


def _packet_nonprojectable_reason(packet: PacketRef) -> str:
    if not _CAPTURE_ID_RE.fullmatch(packet.capture_id):
        return "CAPTURE-IDENTITY-NONPROJECTABLE"
    if packet.timestamp is None:
        return "TIMESTAMP-UNAVAILABLE"
    if packet.timestamp.offset_seconds != 0:
        return "TIMESTAMP-OFFSET-NONPROJECTABLE"
    if packet.captured_length > packet.original_length:
        return "CAPLEN-EXCEEDS-ORIGLEN"
    return ""


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


def projection_errors(projection: object) -> list[str]:
    """Validate identity, types, and local uniqueness of a projection.

    Parentage and complete disposition need the surrounding evidence envelope,
    so ``evidence_projection_errors`` below performs that second pass.  This
    lightweight gate is intentionally called while a result is constructed so
    an adapter bug cannot be mistaken for a controlled input issue.
    """
    try:
        contracts = accepted_record_contracts()
    except ControlledResourceError as exc:
        return [f"{exc.code}: {exc}"]
    if not isinstance(projection, dict):
        return ["contract projection must be an object"]
    errors: list[str] = []
    identity = projection.get("contractIdentity")
    expected_identity = {
        "path": DEVELOPMENT_CONTRACT_PATH,
        "sha256": DEVELOPMENT_CONTRACT_SHA256,
        "version": "PR19-ACCEPTED-SNAPSHOT",
    }
    if identity != expected_identity:
        errors.append("contract projection identity does not match the accepted snapshot")
    if projection.get("adapterVersion") != "1.0":
        errors.append("contract projection adapterVersion is unsupported")
    records = projection.get("records")
    unavailable = projection.get("nonProjectable")
    if not isinstance(records, list) or not isinstance(unavailable, list):
        return [*errors, "contract projection records and nonProjectable must be arrays"]
    seen: set[tuple[str, str]] = set()
    for index, item in enumerate(records):
        if not isinstance(item, dict):
            errors.append(f"contract projection record {index} is not an object")
            continue
        record_type = item.get("recordType")
        source_id = item.get("sourceId")
        if record_type not in _PROJECTED_TYPES or record_type not in contracts:
            errors.append(f"contract projection record {index} has an unknown record type")
            continue
        if not isinstance(source_id, str) or not source_id:
            errors.append(f"contract projection record {index} has an invalid sourceId")
            continue
        key = (record_type, source_id)
        if key in seen:
            errors.append(f"contract projection repeats {record_type} source {source_id}")
        seen.add(key)
        violations = record_instance_errors(record_type, item.get("payload"))
        for constraint, path, detail in violations:
            rendered_path = ".".join(str(part) for part in path) or "$"
            errors.append(f"contract projection {record_type}/{source_id} violates {constraint} at {rendered_path}: {detail}")
    unavailable_seen: set[tuple[str, str]] = set()
    for index, item in enumerate(unavailable):
        if not isinstance(item, dict):
            errors.append(f"contract projection nonProjectable {index} is not an object")
            continue
        source_type = item.get("sourceType")
        source_id = item.get("sourceId")
        reason = item.get("reason")
        if source_type not in _PROJECTED_TYPES or not isinstance(source_id, str) or not source_id or not isinstance(reason, str) or not reason:
            errors.append(f"contract projection nonProjectable {index} is malformed")
            continue
        key = (source_type, source_id)
        if key in unavailable_seen:
            errors.append(f"contract projection repeats nonProjectable {source_type} source {source_id}")
        unavailable_seen.add(key)
        if key in seen:
            errors.append(f"contract projection both projects and rejects {source_type} source {source_id}")
    return errors


def evidence_projection_errors(evidence: object) -> list[str]:
    """Validate complete source disposition and parentage against evidence."""
    if not isinstance(evidence, dict) or not isinstance(evidence.get("contractProjection"), dict):
        return ["evidence contract projection is unavailable"]
    projection = evidence["contractProjection"]
    errors = projection_errors(projection)
    if errors:
        return errors
    packet_rows = _object_rows(evidence.get("packetRefs"), "packetRefId")
    datagram_rows = _object_rows(evidence.get("datagrams"), "datagramId")
    transfer_rows = _object_rows(evidence.get("transfers"), "transferId")
    event_rows = _object_rows(evidence.get("events"), "eventId")
    if any(rows is None for rows in (packet_rows, datagram_rows, transfer_rows, event_rows)):
        return ["evidence records needed for contract projection are malformed"]
    assert packet_rows is not None and datagram_rows is not None and transfer_rows is not None and event_rows is not None
    records = {
        (item["recordType"], item["sourceId"]): item["payload"]
        for item in projection["records"] if isinstance(item, dict)
    }
    unavailable = {
        (item["sourceType"], item["sourceId"]): item["reason"]
        for item in projection["nonProjectable"] if isinstance(item, dict)
    }
    packet_contract_refs: dict[str, str] = {}
    for source_id, packet in packet_rows.items():
        payload, reason = _packet_payload_from_evidence(packet)
        _check_expected_projection(
            errors, records, unavailable, "PACKET-REF", source_id, payload, reason,
        )
        if payload is not None:
            packet_contract_refs[source_id] = _packet_contract_ref_from_evidence(packet)
    for source_id, datagram in datagram_rows.items():
        payload, reason = _datagram_payload_from_evidence(datagram, packet_contract_refs)
        _check_expected_projection(
            errors, records, unavailable, "DATAGRAM-RECORD", source_id, payload, reason,
        )
    for source_id, event in event_rows.items():
        payload, reason = _event_payload_from_evidence(event, packet_contract_refs)
        _check_expected_projection(
            errors, records, unavailable, "PROTOCOL-EVENT", source_id, payload, reason,
        )
    for source_id, transfer in transfer_rows.items():
        _check_transfer_projection(
            errors, records, unavailable, source_id, transfer, packet_contract_refs,
        )
    expected_normal = {
        ("PACKET-REF", source_id) for source_id, packet in packet_rows.items()
        if _packet_payload_from_evidence(packet)[0] is not None
    }
    expected_normal.update(
        ("DATAGRAM-RECORD", source_id) for source_id, row in datagram_rows.items()
        if _datagram_payload_from_evidence(row, packet_contract_refs)[0] is not None
    )
    expected_normal.update(
        ("PROTOCOL-EVENT", source_id) for source_id, row in event_rows.items()
        if _event_payload_from_evidence(row, packet_contract_refs)[0] is not None
    )
    expected_unavailable = {
        ("PACKET-REF", source_id) for source_id, packet in packet_rows.items()
        if _packet_payload_from_evidence(packet)[0] is None
    }
    expected_unavailable.update(
        ("DATAGRAM-RECORD", source_id) for source_id, row in datagram_rows.items()
        if _datagram_payload_from_evidence(row, packet_contract_refs)[0] is None
    )
    expected_unavailable.update(
        ("PROTOCOL-EVENT", source_id) for source_id, row in event_rows.items()
        if _event_payload_from_evidence(row, packet_contract_refs)[0] is None
    )
    for source_id, transfer in transfer_rows.items():
        if _transfer_evidence_nonprojectable_reason(transfer, packet_contract_refs):
            expected_unavailable.add(("TRANSFER-RECORD", source_id))
        else:
            expected_normal.add(("TRANSFER-RECORD", source_id))
            expected_normal.add(("PROTOCOL-EVENT", f"event-request-{source_id}"))
    expected_sources = expected_normal | expected_unavailable
    for key in sorted(set(records) - expected_normal):
        errors.append(f"contract projection has an unparented record {key[0]}/{key[1]}")
    for key in sorted(set(unavailable) - expected_unavailable):
        errors.append(f"contract projection has an unparented nonProjectable item {key[0]}/{key[1]}")
    # Each original evidence source must be accounted for.  Transfers are
    # handled by the association check above because request pairing is
    # intentionally a derived adapter record rather than an evidence event.
    for source_type, source_id in sorted(expected_sources):
        if (source_type, source_id) not in records and (source_type, source_id) not in unavailable:
            errors.append(f"contract projection omits disposition for {source_type}/{source_id}")
    return errors


def _object_rows(value: object, key: str) -> dict[str, dict[str, Any]] | None:
    if not isinstance(value, list):
        return None
    rows: dict[str, dict[str, Any]] = {}
    for item in value:
        if not isinstance(item, dict) or not isinstance(item.get(key), str) or not item[key] or item[key] in rows:
            return None
        rows[item[key]] = item
    return rows


def _packet_payload_from_evidence(packet: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    timestamp = packet.get("timestamp")
    if not isinstance(packet.get("captureId"), str) or not _CAPTURE_ID_RE.fullmatch(packet["captureId"]):
        return None, "CAPTURE-IDENTITY-NONPROJECTABLE"
    if not isinstance(timestamp, dict):
        return None, "TIMESTAMP-UNAVAILABLE"
    if timestamp.get("offsetSeconds") != 0:
        return None, "TIMESTAMP-OFFSET-NONPROJECTABLE"
    caplen, origlen = packet.get("capturedLength"), packet.get("originalLength")
    if not isinstance(caplen, int) or not isinstance(origlen, int) or caplen > origlen:
        return None, "CAPLEN-EXCEEDS-ORIGLEN"
    try:
        return {
            "captureId": packet["captureId"],
            "sectionId": packet["sectionId"],
            "interfaceId": packet["interfaceId"],
            "packetNumber": packet["packetIndex"],
            "rawTicks": timestamp["ticks"],
            "resolution": {"ticksPerSecond": timestamp["ticksPerSecond"]},
            "caplen": caplen,
            "origlen": origlen,
            "decodeStatus": "FULL" if caplen == origlen else "TRUNCATED",
        }, ""
    except KeyError:
        return None, "TIMESTAMP-UNAVAILABLE"


def _packet_contract_ref_from_evidence(packet: dict[str, Any]) -> str:
    return f"{packet['captureId']}:{packet['sectionId']}:{packet['interfaceId']}:{packet['packetIndex']}"


def _datagram_payload_from_evidence(
    datagram: dict[str, Any], packet_contract_refs: dict[str, str],
) -> tuple[dict[str, Any] | None, str]:
    refs = datagram.get("packetRefIds")
    ranges = datagram.get("fragmentRanges")
    if not isinstance(refs, list) or not refs or any(not isinstance(value, str) or value not in packet_contract_refs for value in refs):
        return None, "SOURCE-PACKET-NONPROJECTABLE"
    coverage = [
        {"start": pair[0], "endExclusive": pair[1]}
        for pair in ranges if isinstance(pair, list) and len(pair) == 2 and isinstance(pair[0], int) and isinstance(pair[1], int) and pair[1] > pair[0]
    ] if isinstance(ranges, list) else []
    if not coverage:
        return None, "SOURCE-PACKET-NONPROJECTABLE"
    status = datagram.get("status")
    return {
        "fragmentRefs": [packet_contract_refs[value] for value in refs],
        "coverage": coverage,
        "overlapStatus": "CONFLICT" if status == "CONFLICT" else "NONE",
        "reassemblyStatus": status,
    }, ""


def _event_payload_from_evidence(
    event: dict[str, Any], packet_contract_refs: dict[str, str],
) -> tuple[dict[str, Any] | None, str]:
    refs = event.get("sourcePacketRefIds")
    if not isinstance(refs, list) or not refs or any(not isinstance(value, str) or value not in packet_contract_refs for value in refs):
        return None, "RAW-SOURCE-NONPROJECTABLE"
    fields = event.get("fields")
    parse_status = fields.get("parseStatus") if isinstance(fields, dict) else None
    boundary = {
        "PARSED": "COMPLETE", "PARTIAL": "PARTIAL", "OPAQUE": "OPAQUE", "MALFORMED": "ERROR",
    }.get(parse_status, "COMPLETE" if event.get("layer") == "WIRE" else "OPAQUE")
    source_id = event["eventId"]
    return {
        "eventLayer": event.get("layer"),
        "role": "CLIENT" if event.get("layer") == "WIRE" else "UNKNOWN",
        "payload": {"type": event.get("eventType"), "ref": f"payload-{source_id}"},
        "correlationKey": f"corr-{event.get('transferId')}",
        "rawRefs": [packet_contract_refs[value] for value in refs],
        "parseBoundary": boundary,
    }, ""


def _check_expected_projection(
    errors: list[str], records: dict[tuple[str, str], object], unavailable: dict[tuple[str, str], object],
    source_type: str, source_id: str, payload: dict[str, Any] | None, reason: str,
) -> None:
    key = (source_type, source_id)
    if payload is None:
        if unavailable.get(key) != reason:
            errors.append(f"contract projection must retain {source_type}/{source_id} as {reason}")
        return
    if records.get(key) != payload:
        errors.append(f"contract projection payload/parentage differs for {source_type}/{source_id}")


def _check_transfer_projection(
    errors: list[str], records: dict[tuple[str, str], object], unavailable: dict[tuple[str, str], object],
    source_id: str, transfer: dict[str, Any], packet_contract_refs: dict[str, str],
) -> None:
    key = ("TRANSFER-RECORD", source_id)
    packet_refs = transfer.get("packetRefIds")
    client, server = transfer.get("clientEndpoint"), transfer.get("serverEndpoint")
    request_kind = transfer.get("requestKind")
    reason = _transfer_evidence_nonprojectable_reason(transfer, packet_contract_refs)
    if reason:
        if unavailable.get(key) != reason:
            errors.append(f"contract projection must retain TRANSFER-RECORD/{source_id} as {reason}")
        return
    payload = records.get(key)
    request_key = ("PROTOCOL-EVENT", f"event-request-{source_id}")
    request_payload = records.get(request_key)
    if not isinstance(payload, dict) or not isinstance(request_payload, dict):
        errors.append(f"contract projection omits transfer/request parentage for {source_id}")
        return
    expected_refs = {packet_contract_refs[value] for value in packet_refs}
    if payload.get("direction") != ("SERVER-TO-CLIENT" if request_kind == "RRQ" else "CLIENT-TO-SERVER"):
        errors.append(f"contract projection transfer direction differs for {source_id}")
    if payload.get("endpoints") != {"client": client["address"], "server": server["address"]}:
        errors.append(f"contract projection endpoints differ for {source_id}")
    if payload.get("tid") != {"clientPort": client["port"], "serverPort": server["port"]}:
        errors.append(f"contract projection TID differs for {source_id}")
    if payload.get("request") != request_key[1]:
        errors.append(f"contract projection request parentage differs for {source_id}")
    if request_payload.get("payload", {}).get("type") != request_kind or not set(request_payload.get("rawRefs", [])).issubset(expected_refs):
        errors.append(f"contract projection request event is not parented by transfer {source_id}")
    if not set(payload.get("blockMap", {}).values() if isinstance(payload.get("blockMap"), dict) else ()).issubset(expected_refs):
        errors.append(f"contract projection block map is not parented by transfer {source_id}")
    completion = payload.get("completionEvidence")
    if not isinstance(completion, list) or any(
        not isinstance(item, str) or not item.startswith("pkt-") or item[4:] not in expected_refs for item in completion
    ):
        errors.append(f"contract projection completion evidence is not parented by transfer {source_id}")
    mode = transfer.get("blockSize", {})
    if not isinstance(mode, dict) or payload.get("optionState") != {
        "mode": mode.get("status"),
        "values": {} if mode.get("status") == "UNKNOWN" else {"blksize": mode.get("value")},
    }:
        errors.append(f"contract projection option state differs for {source_id}")


def _transfer_evidence_nonprojectable_reason(
    transfer: dict[str, Any], packet_contract_refs: dict[str, str],
) -> str:
    packet_refs = transfer.get("packetRefIds")
    client, server = transfer.get("clientEndpoint"), transfer.get("serverEndpoint")
    if (
        transfer.get("requestKind") not in {"RRQ", "WRQ"}
        or not isinstance(packet_refs, list)
        or not packet_refs
        or any(not isinstance(value, str) or value not in packet_contract_refs for value in packet_refs)
        or not isinstance(client, dict)
        or not isinstance(server, dict)
        or not isinstance(client.get("address"), str)
        or not isinstance(client.get("port"), int)
        or not isinstance(server.get("address"), str)
        or not isinstance(server.get("port"), int)
    ):
        return "REQUEST-OR-CONTEXT-NONPROJECTABLE"
    return ""
