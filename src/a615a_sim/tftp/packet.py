"""TFTP packet definitions per RFC 1350, RFC 2347/2348/2349.

Includes ARINC 615A block-number rollover rule: after block 65535 the next
block is 1 (not 0).
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from typing import Union

# ---------------------------------------------------------------------------
# Opcodes
# ---------------------------------------------------------------------------
OP_RRQ = 1
OP_WRQ = 2
OP_DATA = 3
OP_ACK = 4
OP_ERROR = 5
OP_OACK = 6

# ---------------------------------------------------------------------------
# Error codes (RFC 1350 §8)
# ---------------------------------------------------------------------------
ERR_NOT_DEFINED = 0
ERR_FILE_NOT_FOUND = 1
ERR_ACCESS_VIOLATION = 2
ERR_DISK_FULL = 3
ERR_ILLEGAL_OP = 4
ERR_UNKNOWN_TID = 5
ERR_FILE_EXISTS = 6
ERR_NO_SUCH_USER = 7


# ---------------------------------------------------------------------------
# Packet dataclasses
# ---------------------------------------------------------------------------
@dataclass
class RRQ:
    filename: str
    mode: str = "octet"
    options: dict[str, str] = field(default_factory=dict)

    def encode(self) -> bytes:
        buf = struct.pack("!H", OP_RRQ)
        buf += self.filename.encode("ascii") + b"\x00"
        buf += self.mode.encode("ascii") + b"\x00"
        for k, v in self.options.items():
            buf += k.encode("ascii") + b"\x00"
            buf += v.encode("ascii") + b"\x00"
        return buf


@dataclass
class WRQ:
    filename: str
    mode: str = "octet"
    options: dict[str, str] = field(default_factory=dict)

    def encode(self) -> bytes:
        buf = struct.pack("!H", OP_WRQ)
        buf += self.filename.encode("ascii") + b"\x00"
        buf += self.mode.encode("ascii") + b"\x00"
        for k, v in self.options.items():
            buf += k.encode("ascii") + b"\x00"
            buf += v.encode("ascii") + b"\x00"
        return buf


@dataclass
class DATA:
    block_num: int  # 1..65535
    data: bytes = b""

    def encode(self) -> bytes:
        return struct.pack("!HH", OP_DATA, self.block_num & 0xFFFF) + self.data


@dataclass
class ACK:
    block_num: int  # 0..65535

    def encode(self) -> bytes:
        return struct.pack("!HH", OP_ACK, self.block_num & 0xFFFF)


@dataclass
class ERROR:
    code: int  # 0-7
    message: str = ""

    def encode(self) -> bytes:
        buf = struct.pack("!HH", OP_ERROR, self.code)
        buf += self.message.encode("ascii") + b"\x00"
        return buf


@dataclass
class OACK:
    options: dict[str, str] = field(default_factory=dict)

    def encode(self) -> bytes:
        buf = struct.pack("!H", OP_OACK)
        for k, v in self.options.items():
            buf += k.encode("ascii") + b"\x00"
            buf += v.encode("ascii") + b"\x00"
        return buf


# ---------------------------------------------------------------------------
# Union type alias
# ---------------------------------------------------------------------------
Packet = Union[RRQ, WRQ, DATA, ACK, ERROR, OACK]


# ---------------------------------------------------------------------------
# Decoder
# ---------------------------------------------------------------------------
class DecodeError(Exception):
    """Raised when a raw datagram cannot be parsed as a valid TFTP packet."""


def _read_null_terminated(data: bytes, offset: int) -> tuple[str, int]:
    """Read a null-terminated ASCII string starting at *offset*."""
    end = data.find(b"\x00", offset)
    if end == -1:
        raise DecodeError("Missing null terminator")
    return data[offset:end].decode("ascii"), end + 1


def decode(data: bytes) -> Packet:
    """Decode raw bytes into a Packet instance.

    Raises DecodeError for malformed or unrecognised packets.
    """
    if len(data) < 2:
        raise DecodeError("Packet too short")

    opcode = struct.unpack("!H", data[:2])[0]

    if opcode == OP_RRQ:
        filename, off = _read_null_terminated(data, 2)
        mode, off = _read_null_terminated(data, off)
        options = _parse_options(data, off)
        return RRQ(filename, mode, options)

    if opcode == OP_WRQ:
        filename, off = _read_null_terminated(data, 2)
        mode, off = _read_null_terminated(data, off)
        options = _parse_options(data, off)
        return WRQ(filename, mode, options)

    if opcode == OP_DATA:
        if len(data) < 4:
            raise DecodeError("DATA packet too short")
        block_num = struct.unpack("!H", data[2:4])[0]
        return DATA(block_num, data[4:])

    if opcode == OP_ACK:
        if len(data) != 4:
            raise DecodeError("ACK packet must be exactly 4 bytes")
        block_num = struct.unpack("!H", data[2:4])[0]
        return ACK(block_num)

    if opcode == OP_ERROR:
        if len(data) < 4:
            raise DecodeError("ERROR packet too short")
        code = struct.unpack("!H", data[2:4])[0]
        msg, _ = _read_null_terminated(data, 4)
        return ERROR(code, msg)

    if opcode == OP_OACK:
        options = _parse_options(data, 2)
        return OACK(options)

    raise DecodeError(f"Unknown opcode {opcode}")


def _parse_options(data: bytes, offset: int) -> dict[str, str]:
    """Parse key-value option pairs from *offset* to end of *data*."""
    opts: dict[str, str] = {}
    while offset < len(data):
        key, offset = _read_null_terminated(data, offset)
        if offset >= len(data):
            break  # value missing — ignore partial
        val, offset = _read_null_terminated(data, offset)
        opts[key] = val
    return opts


# ---------------------------------------------------------------------------
# ARINC 615A block-number helpers
# ---------------------------------------------------------------------------
def next_block(block_num: int) -> int:
    """Return the next block number with ARINC 615A rollover (65535 -> 1)."""
    if block_num >= 65535:
        return 1
    return block_num + 1
