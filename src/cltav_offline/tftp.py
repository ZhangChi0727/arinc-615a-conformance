"""Strict, bounded TFTP decoding and passive session reconstruction."""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass, field
from typing import Iterable

from .models import Diagnostic, TftpMessage, TransferRecord, UdpDatagram


DEFAULT_BLOCK_SIZE = 512
MIN_NEGOTIATED_BLOCK_SIZE = 8
MAX_NEGOTIATED_BLOCK_SIZE = 65_464
REQUEST_KINDS = {"RRQ", "WRQ"}


class TftpDecodeError(ValueError):
    """A malformed TFTP layout with a stable diagnostic code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def parse_tftp(data: bytes) -> TftpMessage:
    """Strictly parse one TFTP message without treating strings as paths."""
    if len(data) < 2:
        raise TftpDecodeError("TRUNCATED-TFTP-OPCODE", "TFTP opcode is truncated")
    opcode = struct.unpack("!H", data[:2])[0]
    if opcode in (1, 2):
        fields = _request_fields(data[2:])
        return TftpMessage("RRQ" if opcode == 1 else "WRQ", fields)
    if opcode == 3:
        if len(data) < 4:
            raise TftpDecodeError("TRUNCATED-TFTP-DATA", "TFTP DATA header is truncated")
        return TftpMessage("DATA", {"block": struct.unpack("!H", data[2:4])[0], "data": data[4:]})
    if opcode == 4:
        if len(data) != 4:
            raise TftpDecodeError("INVALID-TFTP-ACK", "TFTP ACK must be exactly four bytes")
        return TftpMessage("ACK", {"block": struct.unpack("!H", data[2:4])[0]})
    if opcode == 5:
        if len(data) < 5 or not data.endswith(b"\x00"):
            raise TftpDecodeError(
                "INVALID-TFTP-ERROR", "TFTP ERROR needs code and a null-terminated message"
            )
        message = _ascii(data[4:-1], "ERROR message")
        return TftpMessage("ERROR", {"code": struct.unpack("!H", data[2:4])[0], "message": message})
    if opcode == 6:
        options = _option_pairs(data[2:], "OACK")
        if not options:
            raise TftpDecodeError("INVALID-TFTP-OACK", "TFTP OACK requires at least one option")
        return TftpMessage("OACK", {"options": options})
    raise TftpDecodeError("UNKNOWN-TFTP-OPCODE", f"unsupported TFTP opcode {opcode}")


def _request_fields(data: bytes) -> dict[str, object]:
    values = _nul_fields(data, "request")
    if len(values) < 2:
        raise TftpDecodeError("INVALID-TFTP-REQUEST", "TFTP request needs filename and mode")
    if len(values) % 2:
        raise TftpDecodeError("INVALID-TFTP-OPTIONS", "TFTP request options must be key/value pairs")
    filename = _ascii(values[0], "filename")
    mode = _ascii(values[1], "mode").lower()
    if not filename:
        raise TftpDecodeError("INVALID-TFTP-FILENAME", "TFTP filename must be nonempty")
    if mode not in {"octet", "netascii", "mail"}:
        raise TftpDecodeError("UNSUPPORTED-TFTP-MODE", f"TFTP mode {mode!r} is unsupported")
    options = _decode_option_values(values[2:], "request")
    return {"filename": filename, "mode": mode, "options": options}


def _option_pairs(data: bytes, label: str) -> dict[str, str]:
    return _decode_option_values(_nul_fields(data, label), label)


def _nul_fields(data: bytes, label: str) -> list[bytes]:
    if not data or not data.endswith(b"\x00"):
        raise TftpDecodeError(
            "INVALID-TFTP-TERMINATION", f"TFTP {label} fields must end in a null byte"
        )
    values = data[:-1].split(b"\x00")
    if any(value == b"" for value in values):
        raise TftpDecodeError("INVALID-TFTP-FIELD", f"TFTP {label} contains an empty field")
    return values


def _decode_option_values(values: list[bytes], label: str) -> dict[str, str]:
    if len(values) % 2:
        raise TftpDecodeError("INVALID-TFTP-OPTIONS", f"TFTP {label} options must be key/value pairs")
    options: dict[str, str] = {}
    for key_raw, value_raw in zip(values[0::2], values[1::2]):
        key = _ascii(key_raw, "option name").lower()
        value = _ascii(value_raw, "option value")
        if key in options:
            raise TftpDecodeError("DUPLICATE-TFTP-OPTION", f"TFTP option {key!r} is duplicated")
        options[key] = value
    return options


def _ascii(value: bytes, label: str) -> str:
    try:
        return value.decode("ascii")
    except UnicodeDecodeError as exc:
        raise TftpDecodeError("NONASCII-TFTP-STRING", f"TFTP {label} is not ASCII") from exc


@dataclass
class _Block:
    digest: bytes
    data: bytes


@dataclass
class _Session:
    record: TransferRecord
    request_options: dict[str, str]
    blocks: dict[int, _Block] = field(default_factory=dict)
    terminal_block: int | None = None
    received_payload_bytes: int = 0
    terminal_error: bool = False

    @property
    def client(self) -> tuple[str, int]:
        assert self.record.client_endpoint is not None
        return self.record.client_endpoint

    @property
    def server_host(self) -> str:
        assert self.record.server_endpoint is not None
        return self.record.server_endpoint[0]

    @property
    def server_tid(self) -> int | None:
        assert self.record.server_endpoint is not None
        return self.record.server_endpoint[1]

    def bind_server_tid(self, port: int) -> None:
        self.record.server_endpoint = (self.server_host, port)


class TftpReconstructor:
    """Passively associate TFTP sessions without assuming every packet uses port 69."""

    def __init__(
        self,
        *,
        capture_id: str,
        service_port: int = 69,
        max_active_transfers: int = 128,
        max_transfer_bytes: int = 16 * 1024 * 1024,
        max_transfer_records: int = 200_000,
    ) -> None:
        if not 1 <= service_port <= 65_535:
            raise ValueError("service_port must be in 1..65535")
        if max_active_transfers < 1 or max_transfer_bytes < 1 or max_transfer_records < 1:
            raise ValueError("transfer limits must be positive")
        self.capture_id = capture_id
        self.service_port = service_port
        self.max_active_transfers = max_active_transfers
        self.max_transfer_bytes = max_transfer_bytes
        self.max_transfer_records = max_transfer_records
        self._sessions: list[_Session] = []
        self._records: list[TransferRecord] = []
        self._sequence = 0
        self.diagnostics: list[Diagnostic] = []

    @property
    def records(self) -> list[TransferRecord]:
        return list(self._records)

    def could_be_tftp(self, udp: UdpDatagram) -> bool:
        return (
            udp.source_port == self.service_port
            or udp.destination_port == self.service_port
            or any(self._matches(session, udp)[0] for session in self._sessions)
        )

    def process(self, udp: UdpDatagram) -> None:
        """Decode and associate a packet when it lies in the TFTP candidate set."""
        try:
            message = parse_tftp(udp.payload)
        except TftpDecodeError as exc:
            self.diagnostics.append(Diagnostic(
                exc.code, "TFTP", str(exc), packet_ref_id=udp.datagram.packet_refs[-1].id,
                detail={"datagramId": udp.datagram.datagram_id},
            ))
            return
        if message.kind in REQUEST_KINDS and udp.destination_port == self.service_port:
            self._new_request(udp, message)
            return
        candidates = [(session, direction) for session in self._sessions
                      if (direction := self._matches(session, udp)[0]) is not None]
        if len(candidates) != 1:
            self.diagnostics.append(Diagnostic(
                "AMBIGUOUS-TFTP-ASSOCIATION" if candidates else "UNASSOCIATED-TFTP-PACKET",
                "TFTP",
                "TFTP packet could not be associated with exactly one observed request",
                severity="WARNING", packet_ref_id=udp.datagram.packet_refs[-1].id,
                detail={"datagramId": udp.datagram.datagram_id, "candidateCount": len(candidates)},
            ))
            return
        session, direction = candidates[0]
        self._accept(session, direction, udp, message)

    def finish(self) -> list[TransferRecord]:
        """Close every retained session without treating missing evidence as success."""
        for session in self._sessions:
            record = session.record
            if record.reconstruction_status in {"COMPLETE", "CONFLICT", "ERROR", "GAPPED"}:
                continue
            if session.terminal_error:
                record.reconstruction_status = "ERROR"
                continue
            if session.terminal_block is None:
                record.reconstruction_status = "GAPPED"
                _append_unique(record.diagnostics, "INCOMPLETE-TRANSFER")
                continue
            expected = range(1, session.terminal_block + 1)
            if any(number not in session.blocks for number in expected):
                record.reconstruction_status = "GAPPED"
                _append_unique(record.diagnostics, "MISSING-TFTP-DATA-BLOCK")
                continue
            record.reconstruction_status = "COMPLETE"
            record.terminal_block = session.terminal_block
            record.complete_payload = b"".join(session.blocks[number].data for number in expected)
            record.complete_payload_length = len(record.complete_payload)
        return self.records

    def _new_request(self, udp: UdpDatagram, message: TftpMessage) -> None:
        assert message.kind in REQUEST_KINDS
        if len(self._records) >= self.max_transfer_records:
            self.diagnostics.append(Diagnostic(
                "RESOURCE-TRANSFER-RECORD-LIMIT", "TFTP",
                "configured transfer-record limit reached; request was not reconstructed",
                packet_ref_id=udp.datagram.packet_refs[-1].id,
                detail={"limit": self.max_transfer_records},
            ))
            return
        endpoint = (udp.datagram.source, udp.source_port)
        server_host = udp.datagram.destination
        for existing in self._sessions:
            if (
                existing.record.reconstruction_status == "INCOMPLETE"
                and existing.client == endpoint and existing.server_host == server_host
                and existing.server_tid is None
            ):
                existing.record.reconstruction_status = "GAPPED"
                _append_unique(existing.record.diagnostics, "TFTP-SESSION-REUSED")
        if len(self._sessions) >= self.max_active_transfers:
            evicted = self._sessions.pop(0)
            if evicted.record.reconstruction_status == "INCOMPLETE":
                evicted.record.reconstruction_status = "GAPPED"
                _append_unique(evicted.record.diagnostics, "RESOURCE-ACTIVE-TRANSFER-LIMIT")
        self._sequence += 1
        options = dict(message.fields["options"])
        defaulted = "blksize" not in options
        record = TransferRecord(
            transfer_id=f"TR-{self._sequence:08d}",
            capture_id=self.capture_id,
            request_kind=message.kind,
            filename=str(message.fields["filename"]),
            mode=str(message.fields["mode"]),
            client_endpoint=endpoint,
            server_endpoint=(server_host, None),
            association_status="ASSOCIATED-REQUEST-OBSERVED",
            reconstruction_status="INCOMPLETE",
            option_status="DEFAULTED" if defaulted else "UNKNOWN",
            effective_block_size=DEFAULT_BLOCK_SIZE if defaulted else None,
        )
        _record_source(record, udp)
        session = _Session(record=record, request_options=options)
        self._sessions.append(session)
        self._records.append(record)

    def _matches(self, session: _Session, udp: UdpDatagram) -> tuple[str | None, bool]:
        """Return direction and whether a currently unbound server TID may bind."""
        client_host, client_port = session.client
        server_host, server_tid = session.record.server_endpoint or ("", None)
        if (
            udp.datagram.source == client_host
            and udp.source_port == client_port
            and udp.datagram.destination == server_host
            and (server_tid is None and udp.destination_port == self.service_port or server_tid == udp.destination_port)
        ):
            return "CLIENT-TO-SERVER", False
        if (
            udp.datagram.destination == client_host
            and udp.destination_port == client_port
            and udp.datagram.source == server_host
            and (server_tid is None or server_tid == udp.source_port)
        ):
            return "SERVER-TO-CLIENT", server_tid is None
        return None, False

    def _accept(self, session: _Session, direction: str, udp: UdpDatagram, message: TftpMessage) -> None:
        if session.server_tid is None and direction == "SERVER-TO-CLIENT":
            session.bind_server_tid(udp.source_port)
        _record_source(session.record, udp)
        if message.kind == "OACK":
            if direction != "SERVER-TO-CLIENT":
                self._conflict(session, "TFTP-OACK-WRONG-DIRECTION")
                return
            self._apply_oack(session, message)
            return
        if message.kind == "ACK":
            if session.record.request_kind == "WRQ" and direction == "SERVER-TO-CLIENT" and message.fields["block"] == 0:
                self._default_if_unaccepted(session)
            return
        if message.kind == "DATA":
            expected = "SERVER-TO-CLIENT" if session.record.request_kind == "RRQ" else "CLIENT-TO-SERVER"
            if direction != expected:
                self._conflict(session, "TFTP-DATA-WRONG-DIRECTION")
                return
            self._default_if_unaccepted(session)
            self._data(session, message)
            return
        if message.kind == "ERROR":
            session.terminal_error = True
            _append_unique(session.record.diagnostics, "TFTP-ERROR-PACKET")
            return
        self._conflict(session, f"UNEXPECTED-TFTP-{message.kind}")

    def _apply_oack(self, session: _Session, message: TftpMessage) -> None:
        options = dict(message.fields["options"])
        requested = session.request_options
        if any(name not in requested for name in options):
            self._conflict(session, "UNREQUESTED-TFTP-OACK-OPTION")
            return
        value = options.get("blksize")
        if value is None:
            self._default_if_unaccepted(session)
            return
        if "blksize" not in requested:
            self._conflict(session, "UNREQUESTED-TFTP-BLKSIZE")
            return
        try:
            block_size = int(value, 10)
        except ValueError:
            self._conflict(session, "INVALID-TFTP-BLKSIZE")
            return
        if not MIN_NEGOTIATED_BLOCK_SIZE <= block_size <= MAX_NEGOTIATED_BLOCK_SIZE:
            self._conflict(session, "INVALID-TFTP-BLKSIZE")
            return
        session.record.option_status = "ACCEPTED"
        session.record.effective_block_size = block_size

    def _default_if_unaccepted(self, session: _Session) -> None:
        if session.record.option_status == "UNKNOWN":
            session.record.option_status = "DEFAULTED"
            session.record.effective_block_size = DEFAULT_BLOCK_SIZE

    def _data(self, session: _Session, message: TftpMessage) -> None:
        block = int(message.fields["block"])
        data = bytes(message.fields["data"])
        if block == 0:
            self._conflict(session, "UNSUPPORTED-TFTP-BLOCK-ROLLOVER")
            return
        block_size = session.record.effective_block_size
        if block_size is None:
            self._conflict(session, "UNKNOWN-TFTP-BLOCK-SIZE")
            return
        if len(data) > block_size:
            self._conflict(session, "TFTP-DATA-EXCEEDS-BLOCK-SIZE")
            return
        digest = hashlib.sha256(data).digest()
        old = session.blocks.get(block)
        if old is not None:
            if old.digest != digest:
                self._conflict(session, "CONFLICTING-TFTP-DATA-BLOCK")
            return
        if session.received_payload_bytes + len(data) > self.max_transfer_bytes:
            session.record.reconstruction_status = "GAPPED"
            _append_unique(session.record.diagnostics, "RESOURCE-TRANSFER-BYTE-LIMIT")
            return
        session.blocks[block] = _Block(digest, data)
        session.received_payload_bytes += len(data)
        if len(data) < block_size:
            if session.terminal_block is not None and session.terminal_block != block:
                self._conflict(session, "CONFLICTING-TFTP-TERMINATOR")
                return
            session.terminal_block = block
            if all(number in session.blocks for number in range(1, block + 1)):
                session.record.reconstruction_status = "COMPLETE"
                session.record.terminal_block = block
                session.record.complete_payload = b"".join(
                    session.blocks[number].data for number in range(1, block + 1)
                )
                session.record.complete_payload_length = len(session.record.complete_payload)

    def _conflict(self, session: _Session, code: str) -> None:
        session.record.reconstruction_status = "CONFLICT"
        _append_unique(session.record.diagnostics, code)


def _record_source(record: TransferRecord, udp: UdpDatagram) -> None:
    for item in udp.datagram.packet_refs:
        if all(existing.id != item.id for existing in record.packet_refs):
            record.packet_refs.append(item)
    if udp.datagram.datagram_id not in record.datagram_ids:
        record.datagram_ids.append(udp.datagram.datagram_id)


def _append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)
