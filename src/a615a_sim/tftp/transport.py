"""UDP transport wrapper with timeout and retransmission logic."""

from __future__ import annotations

import socket
import time
from typing import Tuple

from .packet import ACK, Packet, decode

Address = Tuple[str, int]


class TransportError(Exception):
    """Raised for transport-level failures (timeout, network errors)."""


class Transport:
    """Thin UDP socket wrapper providing send/recv with timeout."""

    def __init__(self, sock: socket.socket | None = None, timeout: float = 5.0):
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        self._sock = sock
        self._timeout = timeout

    @property
    def socket(self) -> socket.socket:
        return self._sock

    @property
    def timeout(self) -> float:
        return self._timeout

    @timeout.setter
    def timeout(self, value: float) -> None:
        self._timeout = value
        self._sock.settimeout(value)

    def bind(self, addr: Address) -> None:
        self._sock.bind(addr)

    def send_packet(self, addr: Address, packet: Packet) -> None:
        """Encode and send a packet to *addr*."""
        self._sock.sendto(packet.encode(), addr)

    def recv_packet(self) -> Tuple[Address, Packet]:
        """Receive a datagram and decode it.

        Raises TransportError on timeout.
        """
        try:
            data, addr = self._sock.recvfrom(65535)
        except socket.timeout:
            raise TransportError("Receive timed out")
        return addr, decode(data)

    def send_with_retry(
        self,
        addr: Address,
        packet: Packet,
        expected_block: int,
        max_retries: int = 3,
        timeout: float | None = None,
    ) -> ACK:
        """Send *packet* and wait for an ACK with the expected block number.

        Retransmits up to *max_retries* times.  Returns the ACK on success,
        raises TransportError if all retries are exhausted.
        """
        t = timeout if timeout is not None else self._timeout
        self._sock.settimeout(t)
        for attempt in range(max_retries + 1):
            self.send_packet(addr, packet)
            deadline = time.monotonic() + t
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                self._sock.settimeout(remaining)
                try:
                    data, from_addr = self._sock.recvfrom(65535)
                except socket.timeout:
                    break
                # Ignore packets from unexpected TIDs
                if from_addr != addr:
                    continue
                pkt = decode(data)
                if isinstance(pkt, ACK) and pkt.block_num == expected_block:
                    self._sock.settimeout(self._timeout)
                    return pkt
            # Retransmit
        self._sock.settimeout(self._timeout)
        raise TransportError(
            f"No ACK(block={expected_block}) after {max_retries + 1} attempts"
        )

    def close(self) -> None:
        self._sock.close()
