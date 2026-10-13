"""Strict, bounded TFTP decoding and passive session reconstruction.

The reconstructor is deliberately an evidence collector, not a TFTP client or
server. A terminal conflict, peer ERROR, or resource stop is never converted
back into a complete file merely because a later DATA packet appears.
"""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass, field

from .models import Diagnostic, TftpMessage, TransferRecord, UdpDatagram


DEFAULT_BLOCK_SIZE = 512
MIN_NEGOTIATED_BLOCK_SIZE = 8
MAX_NEGOTIATED_BLOCK_SIZE = 65_464
REQUEST_KINDS = {"RRQ", "WRQ"}
_TERMINAL_BAD = {"CONFLICT", "ERROR", "GAPPED"}


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
    return {"filename": filename, "mode": mode, "options": _decode_option_values(values[2:], "request")}


def _option_pairs(data: bytes, label: str) -> dict[str, str]:
    return _decode_option_values(_nul_fields(data, label), label)


def _nul_fields(data: bytes, label: str) -> list[bytes]:
    if not data or not data.endswith(b"\x00"):
        raise TftpDecodeError("INVALID-TFTP-TERMINATION", f"TFTP {label} fields must end in a null byte")
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
    context: tuple[str, int, int, str, tuple[int, ...]]
    blocks: dict[int, _Block] = field(default_factory=dict)
    terminal_block: int | None = None
    received_payload_bytes: int = 0
    oack_options: dict[str, str] | None = None
    data_seen: bool = False
    superseded: bool = False

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

    @property
    def is_bad_terminal(self) -> bool:
        return self.record.reconstruction_status in _TERMINAL_BAD

    @property
    def is_matchable(self) -> bool:
        # A complete session stays matchable only to detect a contradictory
        # later DATA; a new request epoch explicitly supersedes it.
        return not self.superseded and not self.is_bad_terminal

    def bind_server_tid(self, port: int) -> None:
        self.record.server_endpoint = (self.server_host, port)


class TftpReconstructor:
    """Passively associate capture-local TFTP sessions under explicit states."""

    def __init__(
        self,
        *,
        capture_id: str,
        service_port: int = 69,
        max_active_transfers: int = 128,
        max_transfer_bytes: int = 16 * 1024 * 1024,
        max_transfer_records: int = 200_000,
        max_diagnostics: int = 50_000,
    ) -> None:
        if not 1 <= service_port <= 65_535:
            raise ValueError("service_port must be in 1..65535")
        if min(max_active_transfers, max_transfer_bytes, max_transfer_records, max_diagnostics) < 1:
            raise ValueError("transfer limits must be positive")
        self.capture_id = capture_id
        self.service_port = service_port
        self.max_active_transfers = max_active_transfers
        self.max_transfer_bytes = max_transfer_bytes
        self.max_transfer_records = max_transfer_records
        self.max_diagnostics = max_diagnostics
        self._sessions: list[_Session] = []
        self._records: list[TransferRecord] = []
        self._sequence = 0
        self.diagnostics: list[Diagnostic] = []
        self._diagnostic_limit_reported = False

    @property
    def records(self) -> list[TransferRecord]:
        return list(self._records)

    def could_be_tftp(self, udp: UdpDatagram) -> bool:
        return (
            udp.source_port == self.service_port
            or udp.destination_port == self.service_port
            or any(self._matches(session, udp)[0] for session in self._sessions)
            # Keep a cross-domain packet in the candidate set so the public
            # evidence can say it was *not* associated rather than silently
            # disappearing.  ``_matches`` still rejects it for reconstruction.
            or any(_endpoint_shape_matches(session, udp) for session in self._sessions)
        )

    def process(self, udp: UdpDatagram) -> None:
        try:
            message = parse_tftp(udp.payload)
        except TftpDecodeError as exc:
            self._diagnose_packet(exc.code, str(exc), udp)
            return
        if message.kind in REQUEST_KINDS and udp.destination_port == self.service_port:
            self._new_request(udp, message)
            return
        candidates = [
            (session, direction)
            for session in self._sessions
            if (direction := self._matches(session, udp)[0]) is not None
        ]
        if len(candidates) != 1:
            self._diagnose_packet(
                "AMBIGUOUS-TFTP-ASSOCIATION" if candidates else "UNASSOCIATED-TFTP-PACKET",
                "TFTP packet could not be associated with exactly one observed request",
                udp,
                severity="WARNING",
                candidateCount=len(candidates),
            )
            return
        session, direction = candidates[0]
        self._accept(session, direction, udp, message)

    def finish(self) -> list[TransferRecord]:
        """Close remaining observations without turning missing evidence into success."""
        for session in self._sessions:
            record = session.record
            if record.reconstruction_status in _TERMINAL_BAD or record.reconstruction_status == "COMPLETE":
                continue
            if record.option_status == "UNKNOWN":
                self._terminate(session, "GAPPED", "MISSING-TFTP-BLOCKSIZE-CONFIRMATION")
            elif session.terminal_block is None:
                self._terminate(session, "GAPPED", "INCOMPLETE-TRANSFER")
            elif any(number not in session.blocks for number in range(1, session.terminal_block + 1)):
                self._terminate(session, "GAPPED", "MISSING-TFTP-DATA-BLOCK")
            else:
                self._complete(session)
        return self.records

    def _new_request(self, udp: UdpDatagram, message: TftpMessage) -> None:
        assert message.kind in REQUEST_KINDS
        endpoint = (udp.datagram.source, udp.source_port)
        server_host = udp.datagram.destination
        options = dict(message.fields["options"])
        context = udp.datagram.context_key
        request_key = (message.kind, str(message.fields["filename"]), str(message.fields["mode"]), tuple(sorted(options.items())))
        for existing in self._sessions:
            if (
                existing.is_matchable
                and existing.context == context
                and existing.client == endpoint
                and existing.server_host == server_host
                and _request_key(existing) == request_key
                and existing.record.reconstruction_status == "INCOMPLETE"
                and existing.server_tid is None
                and not existing.data_seen
            ):
                _record_source(existing.record, udp)
                return
        if len(self._records) >= self.max_transfer_records:
            self._diagnose_packet(
                "RESOURCE-TRANSFER-RECORD-LIMIT",
                "configured transfer-record limit reached; request was not reconstructed",
                udp,
                limit=self.max_transfer_records,
            )
            return
        for existing in self._sessions:
            if (
                existing.is_matchable
                and existing.context == context
                and existing.client == endpoint
                and existing.server_host == server_host
            ):
                if existing.record.reconstruction_status == "INCOMPLETE":
                    self._terminate(existing, "GAPPED", "TFTP-SESSION-REUSED")
                existing.superseded = True
        active = [session for session in self._sessions if session.is_matchable]
        if len(active) >= self.max_active_transfers:
            evicted = active[0]
            self._terminate(evicted, "GAPPED", "RESOURCE-ACTIVE-TRANSFER-LIMIT")
            evicted.superseded = True
        self._sequence += 1
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
            section_id=udp.datagram.section_id,
            interface_id=udp.datagram.interface_id,
            link_domain=udp.datagram.link_domain,
            vlan_tags=udp.datagram.vlan_tags,
        )
        _record_source(record, udp)
        record.request_packet_ref = udp.datagram.packet_refs[-1]
        self._sessions.append(_Session(record=record, request_options=options, context=context))
        self._records.append(record)

    def _matches(self, session: _Session, udp: UdpDatagram) -> tuple[str | None, bool]:
        """Return direction and whether a currently unbound server TID may bind."""
        if not session.is_matchable or session.context != udp.datagram.context_key:
            return None, False
        client_host, client_port = session.client
        server_host, server_tid = session.record.server_endpoint or ("", None)
        if (
            udp.datagram.source == client_host
            and udp.source_port == client_port
            and udp.datagram.destination == server_host
            and ((server_tid is None and udp.destination_port == self.service_port) or server_tid == udp.destination_port)
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
        if session.is_bad_terminal:
            self._diagnose_packet(
                "TFTP-PACKET-AFTER-TERMINAL",
                "packet follows a terminal TFTP reconstruction state",
                udp,
                severity="WARNING",
            )
            return
        if session.server_tid is None and direction == "SERVER-TO-CLIENT":
            session.bind_server_tid(udp.source_port)
        _record_source(session.record, udp)
        if message.kind == "OACK":
            if direction != "SERVER-TO-CLIENT":
                self._conflict(session, "TFTP-OACK-WRONG-DIRECTION")
            else:
                self._apply_oack(session, message)
            return
        if message.kind == "ACK":
            if session.record.request_kind == "WRQ" and direction == "SERVER-TO-CLIENT" and message.fields["block"] == 0:
                self._default_if_evidenced(session)
            return
        if message.kind == "DATA":
            expected = "SERVER-TO-CLIENT" if session.record.request_kind == "RRQ" else "CLIENT-TO-SERVER"
            if direction != expected:
                self._conflict(session, "TFTP-DATA-WRONG-DIRECTION")
                return
            block = int(message.fields["block"])
            if session.record.option_status == "UNKNOWN" and session.record.request_kind == "RRQ" and block == 1:
                self._default_if_evidenced(session)
            if session.record.option_status == "UNKNOWN":
                _append_unique(session.record.diagnostics, "MISSING-TFTP-BLOCKSIZE-CONFIRMATION")
                return
            self._data(session, message)
            return
        if message.kind == "ERROR":
            self._terminate(session, "ERROR", "TFTP-ERROR-PACKET")
            return
        self._conflict(session, f"UNEXPECTED-TFTP-{message.kind}")

    def _apply_oack(self, session: _Session, message: TftpMessage) -> None:
        options = dict(message.fields["options"])
        if session.data_seen:
            self._conflict(session, "TFTP-OACK-AFTER-DATA")
            return
        if session.oack_options is not None:
            if session.oack_options != options:
                self._conflict(session, "CONFLICTING-TFTP-OACK")
            return
        requested = session.request_options
        if any(name not in requested for name in options):
            self._conflict(session, "UNREQUESTED-TFTP-OACK-OPTION")
            return
        value = options.get("blksize")
        if value is None:
            self._default_if_evidenced(session)
            session.oack_options = options
            return
        requested_value = requested.get("blksize")
        if requested_value is None:
            self._conflict(session, "UNREQUESTED-TFTP-BLKSIZE")
            return
        try:
            requested_size = int(requested_value, 10)
            block_size = int(value, 10)
        except ValueError:
            self._conflict(session, "INVALID-TFTP-BLKSIZE")
            return
        if not (
            MIN_NEGOTIATED_BLOCK_SIZE <= requested_size <= MAX_NEGOTIATED_BLOCK_SIZE
            and MIN_NEGOTIATED_BLOCK_SIZE <= block_size <= MAX_NEGOTIATED_BLOCK_SIZE
            and block_size <= requested_size
        ):
            self._conflict(session, "INVALID-TFTP-BLKSIZE")
            return
        session.record.option_status = "ACCEPTED"
        session.record.effective_block_size = block_size
        session.oack_options = options

    def _default_if_evidenced(self, session: _Session) -> None:
        if session.record.option_status == "UNKNOWN":
            session.record.option_status = "DEFAULTED"
            session.record.effective_block_size = DEFAULT_BLOCK_SIZE

    def _data(self, session: _Session, message: TftpMessage) -> None:
        block = int(message.fields["block"])
        data = bytes(message.fields["data"])
        session.data_seen = True
        if block == 0:
            self._terminate(session, "GAPPED", "UNSUPPORTED-TFTP-BLOCK-ROLLOVER")
            return
        block_size = session.record.effective_block_size
        if block_size is None:
            self._terminate(session, "GAPPED", "UNKNOWN-TFTP-BLOCK-SIZE")
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
        if session.terminal_block is not None:
            self._conflict(session, "TFTP-DATA-AFTER-TERMINATOR")
            return
        if session.received_payload_bytes + len(data) > self.max_transfer_bytes:
            self._terminate(session, "GAPPED", "RESOURCE-TRANSFER-BYTE-LIMIT")
            return
        session.blocks[block] = _Block(digest, data)
        session.record.block_packet_refs[block] = session.record.packet_refs[-1]
        session.received_payload_bytes += len(data)
        if len(data) < block_size:
            session.terminal_block = block
            session.record.completion_packet_ref = session.record.packet_refs[-1]
            self._complete_if_contiguous(session)

    def _complete_if_contiguous(self, session: _Session) -> None:
        assert session.terminal_block is not None
        if all(number in session.blocks for number in range(1, session.terminal_block + 1)):
            self._complete(session)

    def _complete(self, session: _Session) -> None:
        if session.is_bad_terminal or session.terminal_block is None:
            return
        payload = b"".join(session.blocks[number].data for number in range(1, session.terminal_block + 1))
        session.record.reconstruction_status = "COMPLETE"
        session.record.terminal_block = session.terminal_block
        session.record.complete_payload = payload
        session.record.complete_payload_length = len(payload)

    def _terminate(self, session: _Session, status: str, code: str) -> None:
        assert status in _TERMINAL_BAD
        session.record.reconstruction_status = status
        _append_unique(session.record.diagnostics, code)
        session.record.terminal_block = None
        session.record.complete_payload = None
        session.record.complete_payload_length = None

    def _conflict(self, session: _Session, code: str) -> None:
        self._terminate(session, "CONFLICT", code)

    def _diagnose_packet(
        self,
        code: str,
        message: str,
        udp: UdpDatagram,
        *,
        severity: str = "ERROR",
        **detail: int | str,
    ) -> None:
        if len(self.diagnostics) >= self.max_diagnostics - 1:
            if self._diagnostic_limit_reported:
                return
            self._diagnostic_limit_reported = True
            self.diagnostics.append(Diagnostic(
                "RESOURCE-TFTP-DIAGNOSTIC-LIMIT",
                "TFTP",
                "TFTP diagnostics were bounded; later candidate packets were not retained",
                detail={"limit": self.max_diagnostics},
            ))
            return
        self.diagnostics.append(Diagnostic(
            code,
            "TFTP",
            message,
            severity=severity,
            packet_ref_id=udp.datagram.packet_refs[-1].id,
            container_offset=udp.datagram.packet_refs[-1].container_offset,
            detail={"datagramId": udp.datagram.datagram_id, **detail},
        ))


def _request_key(session: _Session) -> tuple[str | None, str | None, str | None, tuple[tuple[str, str], ...]]:
    return (
        session.record.request_kind,
        session.record.filename,
        session.record.mode,
        tuple(sorted(session.request_options.items())),
    )


def _endpoint_shape_matches(session: _Session, udp: UdpDatagram) -> bool:
    """Recognise a potential endpoint relation without authorising a merge."""
    client_host, client_port = session.client
    server_host, server_tid = session.record.server_endpoint or ("", None)
    return (
        (
            udp.datagram.source == client_host
            and udp.source_port == client_port
            and udp.datagram.destination == server_host
            and (server_tid is None or server_tid == udp.destination_port)
        )
        or (
            udp.datagram.destination == client_host
            and udp.destination_port == client_port
            and udp.datagram.source == server_host
            and (server_tid is None or server_tid == udp.source_port)
        )
    )


def _record_source(record: TransferRecord, udp: UdpDatagram) -> None:
    for item in udp.datagram.packet_refs:
        if all(existing.id != item.id for existing in record.packet_refs):
            record.packet_refs.append(item)
    if udp.datagram.datagram_id not in record.datagram_ids:
        record.datagram_ids.append(udp.datagram.datagram_id)


def _append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)
