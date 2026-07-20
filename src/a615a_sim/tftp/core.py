"""TFTP transfer engine — role-agnostic read/write operations.

Implements RFC 1350 transfer flows with RFC 2347 option negotiation and
ARINC 615A block-number rollover (65535 -> 1, not 0).
"""

from __future__ import annotations

import socket
import threading
from typing import Callable

from .packet import (
    ACK,
    DATA,
    ERROR,
    OACK,
    RRQ,
    WRQ,
    DecodeError,
    next_block,
)
from .transport import Address, Transport, TransportError

# Default block size per RFC 1350
DEFAULT_BLKSIZE = 512
DEFAULT_TIMEOUT = 5.0
DEFAULT_RETRIES = 3


# ---------------------------------------------------------------------------
# Client-side: read a file from a server (RRQ flow)
# ---------------------------------------------------------------------------
def read_file(
    server_addr: Address,
    filename: str,
    mode: str = "octet",
    options: dict[str, str] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    max_retries: int = DEFAULT_RETRIES,
) -> bytes:
    """Request *filename* from *server_addr* via RRQ and return its contents.

    Handles OACK negotiation if the server supports options.
    """
    opts = options or {}
    tp = Transport(timeout=timeout)
    try:
        # Bind to an ephemeral port
        tp.bind(("0.0.0.0", 0))
        tid = tp.socket.getsockname()

        rrq = RRQ(filename, mode, opts)
        tp.send_packet(server_addr, rrq)

        blksize = int(opts.get("blksize", DEFAULT_BLKSIZE))
        current_block = 0
        chunks: list[bytes] = []
        negotiated = True  # expecting OACK or first DATA

        while True:
            try:
                from_addr, pkt = tp.recv_packet()
            except TransportError:
                raise TransportError("Timed out waiting for server response")

            # Ignore packets from wrong TID
            if from_addr != server_addr:
                continue

            if isinstance(pkt, ERROR):
                raise TransferError(f"Server error {pkt.code}: {pkt.message}")

            if isinstance(pkt, OACK) and negotiated:
                # Accept negotiated options
                if "blksize" in pkt.options:
                    blksize = int(pkt.options["blksize"])
                ack = ACK(0)
                tp.send_packet(server_addr, ack)
                negotiated = False
                current_block = 0
                continue

            if isinstance(pkt, DATA):
                # First DATA after RRQ — if no OACK, use defaults
                if negotiated:
                    negotiated = False

                current_block = pkt.block_num
                chunks.append(pkt.data)

                ack = ACK(current_block)
                tp.send_packet(server_addr, ack)

                # Last block: data shorter than blksize
                if len(pkt.data) < blksize:
                    break
            else:
                raise TransferError(f"Unexpected packet type: {type(pkt).__name__}")

        return b"".join(chunks)
    finally:
        tp.close()


# ---------------------------------------------------------------------------
# Client-side: write a file to a server (WRQ flow)
# ---------------------------------------------------------------------------
def write_file(
    server_addr: Address,
    filename: str,
    data: bytes,
    mode: str = "octet",
    options: dict[str, str] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    max_retries: int = DEFAULT_RETRIES,
) -> None:
    """Send *data* to *server_addr* as *filename* via WRQ."""
    opts = options or {}
    tp = Transport(timeout=timeout)
    try:
        tp.bind(("0.0.0.0", 0))

        wrq = WRQ(filename, mode, opts)
        tp.send_packet(server_addr, wrq)

        blksize = int(opts.get("blksize", DEFAULT_BLKSIZE))
        expected_ack = 0
        negotiated = True

        # Wait for ACK(0) or OACK before sending data
        while True:
            try:
                from_addr, pkt = tp.recv_packet()
            except TransportError:
                raise TransportError("Timed out waiting for WRQ response")

            if from_addr != server_addr:
                continue

            if isinstance(pkt, ERROR):
                raise TransferError(f"Server error {pkt.code}: {pkt.message}")

            if isinstance(pkt, OACK) and negotiated:
                if "blksize" in pkt.options:
                    blksize = int(pkt.options["blksize"])
                negotiated = False
                break

            if isinstance(pkt, ACK) and pkt.block_num == 0:
                negotiated = False
                break

            raise TransferError(f"Unexpected response to WRQ: {type(pkt).__name__}")

        # Send data blocks
        offset = 0
        block_num = 0
        while offset < len(data) or block_num == 0:
            chunk = data[offset : offset + blksize]
            block_num = next_block(block_num) if block_num > 0 else 1
            data_pkt = DATA(block_num, chunk)
            tp.send_with_retry(server_addr, data_pkt, block_num, max_retries, timeout)
            offset += blksize
            if len(chunk) < blksize:
                break
    finally:
        tp.close()


# ---------------------------------------------------------------------------
# Server-side: serve a read request (responds to RRQ)
# ---------------------------------------------------------------------------
def serve_read(
    data_provider: Callable[[str], bytes],
    listen_addr: Address = ("0.0.0.0", 0),
    options: dict[str, str] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    max_retries: int = DEFAULT_RETRIES,
    stop_event: threading.Event | None = None,
) -> threading.Thread:
    """Start a background thread that serves one RRQ request.

    *data_provider* is called with the requested filename and must return bytes.
    Returns the server thread (already started).
    """
    opts = options or {}
    stop = stop_event or threading.Event()

    def _serve() -> None:
        tp = Transport(timeout=timeout)
        try:
            tp.bind(listen_addr)
            server_addr = tp.socket.getsockname()

            # Wait for RRQ
            while not stop.is_set():
                try:
                    client_addr, pkt = tp.recv_packet()
                    break
                except TransportError:
                    continue
            else:
                return

            if not isinstance(pkt, RRQ):
                return

            file_data = data_provider(pkt.filename)
            blksize = DEFAULT_BLKSIZE

            # Negotiate options if client requested any
            if pkt.options:
                negotiated = {}
                for k in pkt.options:
                    if k in opts:
                        negotiated[k] = opts[k]
                    elif k == "blksize":
                        negotiated["blksize"] = opts.get("blksize", str(DEFAULT_BLKSIZE))
                    elif k == "tsize":
                        negotiated["tsize"] = str(len(file_data))
                if negotiated:
                    if "blksize" in negotiated:
                        blksize = int(negotiated["blksize"])
                    oack = OACK(negotiated)
                    tp.send_packet(client_addr, oack)
                    # Wait for ACK(0)
                    try:
                        _, ack_pkt = tp.recv_packet()
                        if not isinstance(ack_pkt, ACK) or ack_pkt.block_num != 0:
                            return
                    except TransportError:
                        return

            # Send data blocks
            offset = 0
            block_num = 0
            while offset < len(file_data) or block_num == 0:
                chunk = file_data[offset : offset + blksize]
                block_num = next_block(block_num) if block_num > 0 else 1
                data_pkt = DATA(block_num, chunk)
                try:
                    tp.send_with_retry(client_addr, data_pkt, block_num, max_retries, timeout)
                except TransportError:
                    return
                offset += blksize
                if len(chunk) < blksize:
                    break
        finally:
            tp.close()

    t = threading.Thread(target=_serve, daemon=True)
    t.start()
    return t


# ---------------------------------------------------------------------------
# Server-side: serve a write request (responds to WRQ)
# ---------------------------------------------------------------------------
def serve_write(
    data_receiver: Callable[[str, bytes], None],
    listen_addr: Address = ("0.0.0.0", 0),
    options: dict[str, str] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    stop_event: threading.Event | None = None,
) -> threading.Thread:
    """Start a background thread that serves one WRQ request.

    *data_receiver* is called with (filename, received_bytes) when complete.
    Returns the server thread (already started).
    """
    opts = options or {}
    stop = stop_event or threading.Event()

    def _serve() -> None:
        tp = Transport(timeout=timeout)
        try:
            tp.bind(listen_addr)

            # Wait for WRQ
            while not stop.is_set():
                try:
                    client_addr, pkt = tp.recv_packet()
                    break
                except TransportError:
                    continue
            else:
                return

            if not isinstance(pkt, WRQ):
                return

            blksize = DEFAULT_BLKSIZE

            # Send ACK(0) or OACK
            if pkt.options:
                negotiated = {}
                for k in pkt.options:
                    if k in opts:
                        negotiated[k] = opts[k]
                    elif k == "blksize":
                        negotiated["blksize"] = opts.get("blksize", str(DEFAULT_BLKSIZE))
                if negotiated:
                    if "blksize" in negotiated:
                        blksize = int(negotiated["blksize"])
                    oack = OACK(negotiated)
                    tp.send_packet(client_addr, oack)
                else:
                    tp.send_packet(client_addr, ACK(0))
            else:
                tp.send_packet(client_addr, ACK(0))

            # Receive data blocks
            chunks: list[bytes] = []
            expected_block = 1
            while True:
                try:
                    from_addr, dpkt = tp.recv_packet()
                except TransportError:
                    return

                if from_addr != client_addr:
                    continue

                if isinstance(dpkt, ERROR):
                    return

                if not isinstance(dpkt, DATA):
                    continue

                if dpkt.block_num != expected_block:
                    # Send error for wrong block
                    tp.send_packet(client_addr, ERROR(0, "Block sequence error"))
                    return

                chunks.append(dpkt.data)
                tp.send_packet(client_addr, ACK(expected_block))

                if len(dpkt.data) < blksize:
                    break
                expected_block = next_block(expected_block)

            data_receiver(pkt.filename, b"".join(chunks))
        finally:
            tp.close()

    t = threading.Thread(target=_serve, daemon=True)
    t.start()
    return t


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------
class TransferError(Exception):
    """Raised when a TFTP transfer fails at the protocol level."""
