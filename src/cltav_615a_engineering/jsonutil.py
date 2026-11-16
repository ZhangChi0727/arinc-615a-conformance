"""Canonical JSON helpers for D-stage evidence.  Independent of G3 evidence."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Any


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(value: bytes) -> str:
    return sha256(value).hexdigest()


def load_json_mapping(raw: bytes, *, code: str) -> dict[str, Any]:
    from .errors import EngineeringError

    try:
        decoded = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EngineeringError(code, "JSON mapping cannot be decoded") from exc
    if not isinstance(decoded, dict):
        raise EngineeringError(code, "JSON mapping required")
    return decoded
