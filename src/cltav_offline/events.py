"""Bounded first-slice file-role parsing and evidence-event construction."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from .models import ProtocolEvent, TransferRecord


ROLE_SCOPE = {
    "LCI": "INFORMATION",
    "LCL": "INFORMATION",
    "LCS": "INFORMATION",
    "LUI": "UPLOAD",
    "LUR": "UPLOAD",
    "LUS": "UPLOAD",
}


def infer_file_role(filename: str | None) -> str | None:
    """Infer only a declared filename extension, never a host filesystem path."""
    if not filename or "." not in filename:
        return None
    extension = filename.rsplit(".", 1)[-1].upper()
    return extension if extension in ROLE_SCOPE else None


def first_slice_events(records: list[TransferRecord]) -> list[ProtocolEvent]:
    """Create WIRE/PARSE-RESULT/APPLICATION evidence without a verdict layer."""
    return list(iter_first_slice_events(records))


def iter_first_slice_events(records: list[TransferRecord]) -> Iterator[ProtocolEvent]:
    """Yield first-slice evidence one item at a time under a caller's budget.

    ``first_slice_events`` remains the convenient compatibility wrapper, while
    the pipeline consumes this iterator directly so an event cap does not first
    allocate a full, unpublished derived-event list.
    """
    sequence = 0
    for transfer in records:
        sequence += 1
        wire_id = f"EV-{sequence:08d}"
        yield ProtocolEvent(
            event_id=wire_id,
            event_type="TFTP-TRANSFER-OBSERVED",
            layer="WIRE",
            service_scope="UNRESOLVED",
            file_role=None,
            transfer_id=transfer.transfer_id,
            source_datagram_ids=tuple(transfer.datagram_ids),
            source_packet_ref_ids=tuple(item.id for item in transfer.packet_refs),
            fields={
                "requestKind": transfer.request_kind,
                "reconstructionStatus": transfer.reconstruction_status,
                "blockSizeStatus": transfer.option_status,
                "blockSize": transfer.effective_block_size,
            },
            evidence_status="OBSERVED",
        )
        role = infer_file_role(transfer.filename)
        if role is None:
            continue
        sequence += 1
        header = (
            decode_first_slice_header(role, transfer.complete_payload)
            if transfer.mode == "octet"
            else {
                "parseStatus": "OPAQUE",
                "decodedFields": {},
                "unparsedRemainderBytes": None,
                "codecScope": "BOUNDED-FIRST-SLICE-HEADER-ONLY",
                "reason": "TFTP-MODE-NOT-SUPPORTED-FOR-FILE-CODEC",
            }
        )
        parse_id = f"EV-{sequence:08d}"
        yield ProtocolEvent(
            event_id=parse_id,
            event_type="FIRST-SLICE-FILE-HEADER",
            layer="PARSE-RESULT",
            service_scope=ROLE_SCOPE[role],
            file_role=role,
            transfer_id=transfer.transfer_id,
            source_datagram_ids=tuple(transfer.datagram_ids),
            source_packet_ref_ids=tuple(item.id for item in transfer.packet_refs),
            fields=header,
            evidence_status=("PARSED" if header["parseStatus"] == "PARSED" else header["parseStatus"]),
        )
        if header["parseStatus"] != "PARSED":
            continue
        sequence += 1
        yield ProtocolEvent(
            event_id=f"EV-{sequence:08d}",
            event_type="FIRST-SLICE-FILE-EVIDENCE",
            layer="APPLICATION",
            service_scope=ROLE_SCOPE[role],
            file_role=role,
            transfer_id=transfer.transfer_id,
            source_datagram_ids=tuple(transfer.datagram_ids),
            source_packet_ref_ids=tuple(item.id for item in transfer.packet_refs),
            fields={
                "interpretation": "FILE-ROLE-AND-BOUNDED-HEADER-OBSERVED",
                "headerEventId": parse_id,
                "integrity": "NOT-EVALUATED",
                "acceptance": "NOT-EVALUATED",
            },
            evidence_status="PARSED-NOT-VERIFIED",
        )


def decode_first_slice_header(role: str, payload: bytes | None) -> dict[str, Any]:
    """Decode only source-bound leading fields; retain all other bytes as unknown.

    This is deliberately not a complete 615A file codec.  A malformed or
    short complete transfer remains a parser result and never becomes a product
    conformance conclusion.
    """
    result: dict[str, Any] = {
        "parseStatus": "NOT-AVAILABLE",
        "decodedFields": {},
        "unparsedRemainderBytes": None,
        "codecScope": "BOUNDED-FIRST-SLICE-HEADER-ONLY",
    }
    if payload is None:
        result["reason"] = "TRANSFER-NOT-COMPLETE"
        return result
    # Retain the available complete-payload fact before deciding whether the
    # bounded header codec can interpret the first bytes.  This lets the
    # publication gate distinguish a genuinely unsupported/short header from
    # an envelope edit that erases a known length contradiction.
    fields: dict[str, Any] = {"observedFileLength": len(payload)}
    if len(payload) >= 4:
        fields["declaredFileLength"] = int.from_bytes(payload[0:4], "big")
    result["decodedFields"] = fields
    if len(payload) < 6:
        result.update({"parseStatus": "MALFORMED", "reason": "HEADER-SHORTER-THAN-FILE-LENGTH-AND-VERSION"})
        return result
    version = _fixed_ascii(payload[4:6])
    if version is None:
        result.update({"parseStatus": "MALFORMED", "reason": "PROTOCOL-VERSION-NOT-ASCII"})
        return result
    fields["protocolVersion"] = version
    if version != "A1":
        result.update({"parseStatus": "OPAQUE", "reason": "PROTOCOL-VERSION-NOT-IN-BOUNDED-CODEC"})
        return result
    cursor = 6
    if role in {"LCI", "LUI"}:
        status = _u16(payload, cursor)
        description_length = _u8(payload, cursor + 2)
        if status is None or description_length is None:
            return _malformed(result, "STATUS-HEADER-TRUNCATED")
        fields["operationAcceptanceStatusCode"] = status
        description = _bounded_text(payload, cursor + 3, description_length)
        if description["status"] != "PARSED":
            return _partial(result, "STATUS-DESCRIPTION-TRUNCATED-OR-NONASCII", fields)
        fields["statusDescription"] = description
        cursor += 3 + description_length
    elif role == "LCL":
        count = _u16(payload, cursor)
        if count is None:
            return _malformed(result, "LCL-COUNT-TRUNCATED")
        fields["numberOfTargetHardware"] = count
        cursor += 2
    elif role == "LCS":
        counter, status, exception_timer, estimated_time, description_length = _fields_lcs(payload, cursor)
        if None in {counter, status, exception_timer, estimated_time, description_length}:
            return _malformed(result, "LCS-STATUS-HEADER-TRUNCATED")
        description = _bounded_text(payload, cursor + 9, description_length)
        if description["status"] != "PARSED":
            return _partial(result, "LCS-DESCRIPTION-TRUNCATED-OR-NONASCII", fields)
        fields.update({
            "counter": counter,
            "informationOperationStatusCode": status,
            "exceptionTimer": {
                "present": True,
                "value": exception_timer,
                "useCondition": "WHEN-STATUS-CODE-0002-OR-0004",
                "useConditionSatisfied": status in {2, 4},
            },
            "estimatedTime": _estimated_time(estimated_time),
            "statusDescription": description,
        })
        cursor += 9 + description_length
    elif role == "LUR":
        count = _u16(payload, cursor)
        if count is None:
            return _malformed(result, "LUR-COUNT-TRUNCATED")
        fields["numberOfHeaderFiles"] = count
        cursor += 2
    elif role == "LUS":
        status = _u16(payload, cursor)
        description_length = _u8(payload, cursor + 2)
        if status is None or description_length is None:
            return _malformed(result, "LUS-STATUS-HEADER-TRUNCATED")
        cursor += 3 + description_length
        counter = _u16(payload, cursor)
        exception_timer = _u16(payload, cursor + 2)
        estimated_time = _u16(payload, cursor + 4)
        ratio = payload[cursor + 6:cursor + 9]
        if None in {counter, exception_timer, estimated_time} or len(ratio) != 3:
            return _malformed(result, "LUS-CONTINUATION-HEADER-TRUNCATED")
        ratio_text = _fixed_ascii(ratio)
        if ratio_text is None:
            return _malformed(result, "LUS-RATIO-NOT-ASCII")
        description = _bounded_text(payload, 9, description_length)
        if description["status"] != "PARSED":
            return _partial(result, "LUS-DESCRIPTION-TRUNCATED-OR-NONASCII", fields)
        fields.update({
            "uploadOperationStatusCode": status,
            "statusDescription": description,
            "counter": counter,
            "exceptionTimer": {
                "present": True,
                "value": exception_timer,
                "useCondition": "WHEN-STATUS-CODE-0002-OR-0004",
                "useConditionSatisfied": status in {2, 4},
            },
            "estimatedTime": _estimated_time(estimated_time),
            "loadListRatio": {
                "rawAscii": ratio_text,
                "alignment": "RIGHT",
                "padding": "LEADING-SPACE",
            },
        })
        cursor += 9
    else:  # pragma: no cover - guarded by infer_file_role
        return _malformed(result, "UNSUPPORTED-FILE-ROLE")
    # The bounded codec does not interpret the entire role-specific body, but
    # once its supported A1 prefix is structurally valid it can still check
    # the header's file-length claim against the complete reconstructed byte
    # sequence.  Do not promote contradictory bytes into an APPLICATION
    # event: retain both values as a controlled malformed parse result.
    if fields["declaredFileLength"] != len(payload):
        result["decodedFields"] = fields
        result["parseStatus"] = "MALFORMED"
        result["reason"] = "DECLARED-FILE-LENGTH-MISMATCH"
        return result
    result["parseStatus"] = "PARSED"
    result["decodedFields"] = fields
    result["unparsedRemainderBytes"] = max(0, len(payload) - cursor)
    return result


def _u8(data: bytes, offset: int) -> int | None:
    return data[offset] if offset < len(data) else None


def _u16(data: bytes, offset: int) -> int | None:
    if offset + 2 > len(data):
        return None
    return int.from_bytes(data[offset:offset + 2], "big")


def _fixed_ascii(data: bytes) -> str | None:
    try:
        return data.decode("ascii")
    except UnicodeDecodeError:
        return None


def _bounded_text(data: bytes, offset: int, length: int) -> dict[str, Any]:
    end = offset + length
    if end > len(data):
        return {"status": "TRUNCATED", "declaredLength": length, "value": None}
    raw = data[offset:end]
    value = _fixed_ascii(raw.rstrip(b"\x00"))
    return {
        "status": "PARSED" if value is not None else "NONASCII",
        "declaredLength": length,
        "value": value,
    }


def _estimated_time(value: int) -> dict[str, Any]:
    return (
        {"status": "NOT-PROVIDED", "rawValue": "0xFFFF", "value": None}
        if value == 0xFFFF
        else {
            "status": "RAW-NOT-INTERPRETED",
            "rawValue": value,
            "value": None,
            "reason": "ESTIMATED-TIME-USABILITY-NOT-IMPLEMENTED",
        }
    )


def _fields_lcs(data: bytes, offset: int) -> tuple[int | None, int | None, int | None, int | None, int | None]:
    return (
        _u16(data, offset), _u16(data, offset + 2), _u16(data, offset + 4),
        _u16(data, offset + 6), _u8(data, offset + 8),
    )


def _malformed(result: dict[str, Any], reason: str) -> dict[str, Any]:
    result["parseStatus"] = "MALFORMED"
    result["reason"] = reason
    return result


def _partial(result: dict[str, Any], reason: str, fields: dict[str, Any]) -> dict[str, Any]:
    """Keep source-bound prefix fields without claiming a complete header parse."""
    result["parseStatus"] = "PARTIAL"
    result["reason"] = reason
    result["decodedFields"] = fields
    return result
