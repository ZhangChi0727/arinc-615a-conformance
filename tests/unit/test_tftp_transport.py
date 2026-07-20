"""Unit tests for TFTP transport layer (timeout / retry logic)."""

import socket
import threading
import time
import pytest

from a615a_sim.tftp.packet import ACK, DATA, RRQ
from a615a_sim.tftp.transport import Transport, TransportError


def _free_port() -> int:
    """Return an available UDP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


# ---------------------------------------------------------------------------
# Basic send/recv
# ---------------------------------------------------------------------------
class TestBasicSendRecv:
    def test_send_and_recv_packet(self):
        port = _free_port()
        sender = Transport(timeout=2.0)
        receiver = Transport(timeout=2.0)
        receiver.bind(("127.0.0.1", port))

        try:
            pkt = ACK(42)
            sender.send_packet(("127.0.0.1", port), pkt)

            addr, decoded = receiver.recv_packet()
            assert isinstance(decoded, ACK)
            assert decoded.block_num == 42
            assert addr[0] == "127.0.0.1"
        finally:
            sender.close()
            receiver.close()


# ---------------------------------------------------------------------------
# Timeout
# ---------------------------------------------------------------------------
class TestTimeout:
    def test_recv_timeout_raises(self):
        tp = Transport(timeout=0.2)
        tp.bind(("127.0.0.1", 0))
        try:
            with pytest.raises(TransportError, match="timed out"):
                tp.recv_packet()
        finally:
            tp.close()


# ---------------------------------------------------------------------------
# Retry logic
# ---------------------------------------------------------------------------
class TestRetry:
    def test_send_with_retry_success(self):
        """Server responds with correct ACK on first attempt."""
        port = _free_port()
        client = Transport(timeout=2.0)
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_sock.settimeout(2.0)
        server_sock.bind(("127.0.0.1", port))

        def _respond():
            data, addr = server_sock.recvfrom(1024)
            # Send ACK(1) back
            server_sock.sendto(ACK(1).encode(), addr)

        t = threading.Thread(target=_respond, daemon=True)
        t.start()

        try:
            ack = client.send_with_retry(
                ("127.0.0.1", port), DATA(1, b"payload"), expected_block=1, max_retries=3
            )
            assert isinstance(ack, ACK)
            assert ack.block_num == 1
            t.join(timeout=3)
        finally:
            client.close()
            server_sock.close()

    def test_send_with_retry_exhausted(self):
        """No response at all — should raise after retries."""
        port = _free_port()
        client = Transport(timeout=0.2)
        # Bind a socket that never responds
        blackhole = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        blackhole.bind(("127.0.0.1", port))

        try:
            with pytest.raises(TransportError, match="No ACK"):
                client.send_with_retry(
                    ("127.0.0.1", port),
                    DATA(1, b"x"),
                    expected_block=1,
                    max_retries=1,
                    timeout=0.2,
                )
        finally:
            client.close()
            blackhole.close()

    def test_wrong_block_ignored(self):
        """ACK with wrong block number should not satisfy the wait."""
        port = _free_port()
        client = Transport(timeout=0.3)
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_sock.settimeout(0.5)
        server_sock.bind(("127.0.0.1", port))

        def _respond_wrong():
            data, addr = server_sock.recvfrom(1024)
            # Send ACK with WRONG block number
            server_sock.sendto(ACK(999).encode(), addr)

        t = threading.Thread(target=_respond_wrong, daemon=True)
        t.start()

        try:
            with pytest.raises(TransportError, match="No ACK"):
                client.send_with_retry(
                    ("127.0.0.1", port),
                    DATA(1, b"x"),
                    expected_block=1,
                    max_retries=0,
                    timeout=0.3,
                )
            t.join(timeout=2)
        finally:
            client.close()
            server_sock.close()
