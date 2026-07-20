"""Unit tests for TFTP packet encode/decode (RFC 1350 + options)."""

import struct
import pytest

from a615a_sim.tftp.packet import (
    ACK,
    DATA,
    ERROR,
    OACK,
    RRQ,
    WRQ,
    OP_ACK,
    OP_DATA,
    OP_ERROR,
    OP_OACK,
    OP_RRQ,
    OP_WRQ,
    DecodeError,
    decode,
    next_block,
)


# ---------------------------------------------------------------------------
# RRQ
# ---------------------------------------------------------------------------
class TestRRQ:
    def test_encode_decode_basic(self):
        pkt = RRQ("firmware.bin", "octet")
        raw = pkt.encode()
        result = decode(raw)
        assert isinstance(result, RRQ)
        assert result.filename == "firmware.bin"
        assert result.mode == "octet"
        assert result.options == {}

    def test_encode_decode_with_options(self):
        opts = {"blksize": "1024", "tsize": "4096"}
        pkt = RRQ("data.lod", "octet", opts)
        result = decode(pkt.encode())
        assert isinstance(result, RRQ)
        assert result.options == opts

    def test_raw_format(self):
        pkt = RRQ("test", "octet")
        raw = pkt.encode()
        assert raw[:2] == struct.pack("!H", OP_RRQ)
        assert b"test\x00" in raw
        assert b"octet\x00" in raw


# ---------------------------------------------------------------------------
# WRQ
# ---------------------------------------------------------------------------
class TestWRQ:
    def test_encode_decode_basic(self):
        pkt = WRQ("upload.bin", "octet")
        result = decode(pkt.encode())
        assert isinstance(result, WRQ)
        assert result.filename == "upload.bin"
        assert result.mode == "octet"

    def test_encode_decode_with_options(self):
        opts = {"blksize": "512", "timeout": "3"}
        pkt = WRQ("file.dat", "octet", opts)
        result = decode(pkt.encode())
        assert isinstance(result, WRQ)
        assert result.options == opts


# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------
class TestDATA:
    def test_encode_decode(self):
        payload = b"hello world"
        pkt = DATA(1, payload)
        result = decode(pkt.encode())
        assert isinstance(result, DATA)
        assert result.block_num == 1
        assert result.data == payload

    def test_empty_data(self):
        pkt = DATA(5, b"")
        result = decode(pkt.encode())
        assert isinstance(result, DATA)
        assert result.block_num == 5
        assert result.data == b""

    def test_block_num_boundaries(self):
        for bn in (0, 1, 32768, 65535):
            pkt = DATA(bn, b"x")
            result = decode(pkt.encode())
            assert isinstance(result, DATA)
            assert result.block_num == bn

    def test_raw_format(self):
        pkt = DATA(42, b"AB")
        raw = pkt.encode()
        assert raw == struct.pack("!HH", OP_DATA, 42) + b"AB"


# ---------------------------------------------------------------------------
# ACK
# ---------------------------------------------------------------------------
class TestACK:
    def test_encode_decode(self):
        pkt = ACK(7)
        result = decode(pkt.encode())
        assert isinstance(result, ACK)
        assert result.block_num == 7

    def test_ack_zero(self):
        result = decode(ACK(0).encode())
        assert isinstance(result, ACK)
        assert result.block_num == 0

    def test_ack_65535(self):
        result = decode(ACK(65535).encode())
        assert isinstance(result, ACK)
        assert result.block_num == 65535

    def test_raw_length(self):
        assert len(ACK(1).encode()) == 4


# ---------------------------------------------------------------------------
# ERROR
# ---------------------------------------------------------------------------
class TestERROR:
    def test_encode_decode(self):
        pkt = ERROR(1, "File not found")
        result = decode(pkt.encode())
        assert isinstance(result, ERROR)
        assert result.code == 1
        assert result.message == "File not found"

    def test_all_error_codes(self):
        for code in range(8):
            pkt = ERROR(code, f"err{code}")
            result = decode(pkt.encode())
            assert isinstance(result, ERROR)
            assert result.code == code

    def test_empty_message(self):
        result = decode(ERROR(0, "").encode())
        assert isinstance(result, ERROR)
        assert result.message == ""


# ---------------------------------------------------------------------------
# OACK
# ---------------------------------------------------------------------------
class TestOACK:
    def test_encode_decode(self):
        opts = {"blksize": "1024", "timeout": "5", "tsize": "2048"}
        pkt = OACK(opts)
        result = decode(pkt.encode())
        assert isinstance(result, OACK)
        assert result.options == opts

    def test_single_option(self):
        pkt = OACK({"blksize": "256"})
        result = decode(pkt.encode())
        assert isinstance(result, OACK)
        assert result.options["blksize"] == "256"

    def test_raw_starts_with_opcode(self):
        raw = OACK({"blksize": "512"}).encode()
        assert raw[:2] == struct.pack("!H", OP_OACK)


# ---------------------------------------------------------------------------
# Decode errors
# ---------------------------------------------------------------------------
class TestDecodeErrors:
    def test_too_short(self):
        with pytest.raises(DecodeError):
            decode(b"\x00")

    def test_empty(self):
        with pytest.raises(DecodeError):
            decode(b"")

    def test_unknown_opcode(self):
        with pytest.raises(DecodeError):
            decode(struct.pack("!H", 99))

    def test_data_too_short(self):
        with pytest.raises(DecodeError):
            decode(struct.pack("!H", OP_DATA) + b"\x00")

    def test_ack_wrong_length(self):
        with pytest.raises(DecodeError):
            decode(struct.pack("!HHH", OP_ACK, 1, 2))

    def test_missing_null_terminator(self):
        # RRQ without null terminator after filename
        with pytest.raises(DecodeError):
            decode(struct.pack("!H", OP_RRQ) + b"no_null")


# ---------------------------------------------------------------------------
# ARINC 615A block rollover
# ---------------------------------------------------------------------------
class TestNextBlock:
    def test_normal_increment(self):
        assert next_block(1) == 2
        assert next_block(100) == 101
        assert next_block(65534) == 65535

    def test_rollover_to_one(self):
        """ARINC 615A: after 65535, next block is 1 (not 0)."""
        assert next_block(65535) == 1

    def test_zero_goeses_to_one(self):
        assert next_block(0) == 1
