"""Unit tests for TFTP transfer engine (loopback read/write, options, rollover)."""

import socket
import threading
import time
import pytest

from a615a_sim.tftp.core import (
    TransferError,
    read_file,
    serve_read,
    serve_write,
    write_file,
)


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


# ---------------------------------------------------------------------------
# Loopback READ (RRQ) transfer
# ---------------------------------------------------------------------------
class TestLoopbackRead:
    def test_basic_read(self):
        """Server has data; client reads it via RRQ."""
        port = _free_port()
        payload = b"Hello ARINC 615A" * 10  # 160 bytes
        server_data = {"firmware.bin": payload}

        def provider(filename: str) -> bytes:
            return server_data[filename]

        stop = threading.Event()
        srv = serve_read(provider, ("127.0.0.1", port), timeout=3.0, stop_event=stop)

        try:
            result = read_file(("127.0.0.1", port), "firmware.bin", timeout=3.0)
            assert result == payload
        finally:
            stop.set()
            srv.join(timeout=2)

    def test_read_with_blksize_option(self):
        """Negotiate blksize=128 and verify correct transfer."""
        port = _free_port()
        payload = b"A" * 500  # Not a multiple of 128
        stop = threading.Event()
        srv = serve_read(
            lambda fn: payload,
            ("127.0.0.1", port),
            options={"blksize": "128"},
            timeout=3.0,
            stop_event=stop,
        )

        try:
            result = read_file(
                ("127.0.0.1", port),
                "test.bin",
                options={"blksize": "128"},
                timeout=3.0,
            )
            assert result == payload
        finally:
            stop.set()
            srv.join(timeout=2)

    def test_read_empty_file(self):
        """Reading an empty file should return b''."""
        port = _free_port()
        stop = threading.Event()
        srv = serve_read(
            lambda fn: b"",
            ("127.0.0.1", port),
            timeout=3.0,
            stop_event=stop,
        )

        try:
            result = read_file(("127.0.0.1", port), "empty.bin", timeout=3.0)
            assert result == b""
        finally:
            stop.set()
            srv.join(timeout=2)

    def test_read_large_data(self):
        """Transfer data larger than one block (512 bytes default)."""
        port = _free_port()
        payload = bytes(range(256)) * 10  # 2560 bytes
        stop = threading.Event()
        srv = serve_read(
            lambda fn: payload,
            ("127.0.0.1", port),
            timeout=3.0,
            stop_event=stop,
        )

        try:
            result = read_file(("127.0.0.1", port), "large.bin", timeout=3.0)
            assert result == payload
        finally:
            stop.set()
            srv.join(timeout=2)


# ---------------------------------------------------------------------------
# Loopback WRITE (WRQ) transfer
# ---------------------------------------------------------------------------
class TestLoopbackWrite:
    def test_basic_write(self):
        """Client writes data; server receives it via WRQ."""
        port = _free_port()
        payload = b"Upload data " * 20
        received = {}

        def receiver(filename: str, data: bytes) -> None:
            received[filename] = data

        stop = threading.Event()
        srv = serve_write(receiver, ("127.0.0.1", port), timeout=3.0, stop_event=stop)

        try:
            write_file(("127.0.0.1", port), "upload.bin", payload, timeout=3.0)
            # Give server thread time to call receiver
            time.sleep(0.2)
            assert received["upload.bin"] == payload
        finally:
            stop.set()
            srv.join(timeout=2)

    def test_write_with_blksize(self):
        """Negotiate blksize and verify write completes."""
        port = _free_port()
        payload = b"B" * 300
        received = {}

        stop = threading.Event()
        srv = serve_write(
            lambda fn, data: received.update({fn: data}),
            ("127.0.0.1", port),
            options={"blksize": "64"},
            timeout=3.0,
            stop_event=stop,
        )

        try:
            write_file(
                ("127.0.0.1", port),
                "small_blk.bin",
                payload,
                options={"blksize": "64"},
                timeout=3.0,
            )
            time.sleep(0.2)
            assert received["small_blk.bin"] == payload
        finally:
            stop.set()
            srv.join(timeout=2)


# ---------------------------------------------------------------------------
# Block rollover (ARINC 615A: 65535 -> 1)
# ---------------------------------------------------------------------------
class TestBlockRollover:
    def test_rollover_with_small_blksize(self):
        """Force many blocks with tiny blksize to exercise block numbering.

        We can't practically send 65535 blocks in a unit test, but we verify
        the transfer works correctly across many blocks with a small blksize.
        """
        port = _free_port()
        blksize = 16
        # Send enough data for ~20 blocks
        payload = b"X" * (blksize * 20 + 5)
        stop = threading.Event()
        srv = serve_read(
            lambda fn: payload,
            ("127.0.0.1", port),
            options={"blksize": str(blksize)},
            timeout=5.0,
            stop_event=stop,
        )

        try:
            result = read_file(
                ("127.0.0.1", port),
                "rollover.bin",
                options={"blksize": str(blksize)},
                timeout=5.0,
            )
            assert result == payload
        finally:
            stop.set()
            srv.join(timeout=2)


# ---------------------------------------------------------------------------
# Timeout / failure
# ---------------------------------------------------------------------------
class TestTransferTimeout:
    def test_read_timeout_no_server(self):
        """Client should fail when no server is listening."""
        port = _free_port()
        # Bind a socket to prevent "connection refused" but never respond
        blackhole = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        blackhole.bind(("127.0.0.1", port))

        try:
            with pytest.raises(Exception):
                read_file(("127.0.0.1", port), "nope.bin", timeout=0.5)
        finally:
            blackhole.close()


# ---------------------------------------------------------------------------
# Edge cases: exact-multiple file size, duplicate DATA, wrong TID
# ---------------------------------------------------------------------------
class TestExactMultipleBlksize:
    """RFC 1350 §5: a final DATA packet shorter than blksize terminates the
    transfer. When the file size is an exact multiple of blksize, an extra
    zero-length DATA packet must be sent. Previously this case hung forever.
    """

    def test_read_exact_multiple_default_blksize(self):
        port = _free_port()
        payload = b"A" * (512 * 5)  # exact multiple of default blksize
        stop = threading.Event()
        srv = serve_read(lambda fn: payload, ("127.0.0.1", port), timeout=3.0, stop_event=stop)
        try:
            result = read_file(("127.0.0.1", port), "exact.bin", timeout=3.0)
            assert result == payload
        finally:
            stop.set()
            srv.join(timeout=2)

    def test_read_exact_multiple_small_blksize(self):
        port = _free_port()
        blksize = 32
        payload = b"B" * (blksize * 8)  # exact multiple
        stop = threading.Event()
        srv = serve_read(
            lambda fn: payload,
            ("127.0.0.1", port),
            options={"blksize": str(blksize)},
            timeout=3.0,
            stop_event=stop,
        )
        try:
            result = read_file(
                ("127.0.0.1", port),
                "exact_small.bin",
                options={"blksize": str(blksize)},
                timeout=3.0,
            )
            assert result == payload
        finally:
            stop.set()
            srv.join(timeout=2)

    def test_write_exact_multiple_default_blksize(self):
        port = _free_port()
        payload = b"C" * (512 * 4)  # exact multiple
        received = {}
        stop = threading.Event()
        srv = serve_write(
            lambda fn, data: received.update({fn: data}),
            ("127.0.0.1", port),
            timeout=3.0,
            stop_event=stop,
        )
        try:
            write_file(("127.0.0.1", port), "exact_w.bin", payload, timeout=3.0)
            time.sleep(0.2)
            assert received.get("exact_w.bin") == payload
        finally:
            stop.set()
            srv.join(timeout=2)

    def test_write_exact_multiple_small_blksize(self):
        port = _free_port()
        blksize = 16
        payload = b"D" * (blksize * 16)  # exact multiple
        received = {}
        stop = threading.Event()
        srv = serve_write(
            lambda fn, data: received.update({fn: data}),
            ("127.0.0.1", port),
            options={"blksize": str(blksize)},
            timeout=3.0,
            stop_event=stop,
        )
        try:
            write_file(
                ("127.0.0.1", port),
                "exact_w_small.bin",
                payload,
                options={"blksize": str(blksize)},
                timeout=3.0,
            )
            time.sleep(0.2)
            assert received.get("exact_w_small.bin") == payload
        finally:
            stop.set()
            srv.join(timeout=2)


class TestDuplicateData:
    """Server retransmits a DATA block when its ACK is lost. The client must
    re-ACK but must NOT append the duplicate (otherwise the file is corrupted).
    """

    def test_read_survives_duplicate_data(self):
        """Inject a duplicate DATA block on the server side and verify the
        client reassembles the file correctly."""
        import struct
        from a615a_sim.tftp.packet import DATA, OP_ACK

        port = _free_port()
        payload = b"X" * 200  # single block, < blksize
        stop = threading.Event()

        # Custom server: send DATA(1), then duplicate DATA(1), then wait for ACKs
        def _serve_dup():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("127.0.0.1", port))
            sock.settimeout(3.0)
            try:
                # Wait for RRQ
                data, client = sock.recvfrom(65535)
                # Send DATA(1) twice (simulating lost ACK)
                pkt1 = DATA(1, payload).encode()
                sock.sendto(pkt1, client)
                sock.sendto(pkt1, client)
                # Collect two ACKs
                acks = 0
                ack_prefix = struct.pack("!H", OP_ACK)
                while acks < 2:
                    try:
                        msg, _ = sock.recvfrom(65535)
                        if len(msg) == 4 and msg[:2] == ack_prefix:
                            acks += 1
                    except socket.timeout:
                        break
            finally:
                sock.close()

        srv = threading.Thread(target=_serve_dup, daemon=True)
        srv.start()
        try:
            result = read_file(("127.0.0.1", port), "dup.bin", timeout=3.0)
            assert result == payload  # not payload * 2
        finally:
            stop.set()
            srv.join(timeout=2)
