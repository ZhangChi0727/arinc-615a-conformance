"""Load controlled runtime resources from a wheel or a source checkout.

The installed tool never relies on the current working directory.  A source
checkout may fall back to its single authoritative ``configs/engineering``
files, while a wheel consumes the build-populated package resources.
"""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any


_RESOURCE_NAMES = {
    "development-contract": "cltav_development_contracts.json",
    "development-contract-schema": "cltav_development_contracts.schema.json",
    "evidence-schema": "cltav_offline_intake_evidence.schema.json",
}


class ControlledResourceError(RuntimeError):
    """A package/resource failure that must fail closed before publication."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _source_authority_path(filename: str) -> Path:
    return Path(__file__).resolve().parents[2] / "configs" / "engineering" / filename


def _filename(resource_id: str) -> str:
    try:
        return _RESOURCE_NAMES[resource_id]
    except KeyError as exc:
        raise ControlledResourceError("CONTROLLED-RESOURCE-UNKNOWN", f"unknown controlled resource {resource_id!r}") from exc


@lru_cache(maxsize=None)
def controlled_resource_bytes(resource_id: str) -> bytes:
    """Read a named controlled resource without depending on CWD or Git."""
    filename = _filename(resource_id)
    try:
        candidate = resources.files("cltav_offline.resources").joinpath(filename)
        return candidate.read_bytes()
    except (FileNotFoundError, ModuleNotFoundError, OSError):
        # Editable/source runs have no checked-in duplicate under ``src``.  The
        # fallback is intentionally exact and only succeeds beside the source
        # package; arbitrary CWD paths are never consulted.
        source = _source_authority_path(filename)
        try:
            return source.read_bytes()
        except OSError as exc:
            raise ControlledResourceError(
                "CONTROLLED-RESOURCE-UNAVAILABLE",
                f"controlled resource {filename} is unavailable",
            ) from exc


@lru_cache(maxsize=None)
def controlled_resource_json(resource_id: str) -> dict[str, Any]:
    """Read a controlled JSON object with a named, publish-blocking failure."""
    filename = _filename(resource_id)
    try:
        value = json.loads(controlled_resource_bytes(resource_id).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ControlledResourceError(
            "CONTROLLED-RESOURCE-INVALID", f"controlled resource {filename} is not valid JSON"
        ) from exc
    if not isinstance(value, dict):
        raise ControlledResourceError(
            "CONTROLLED-RESOURCE-INVALID", f"controlled resource {filename} must contain a JSON object"
        )
    return value


def controlled_resource_sha256(resource_id: str) -> str:
    return hashlib.sha256(controlled_resource_bytes(resource_id)).hexdigest()


def source_authority_bytes(resource_id: str) -> bytes | None:
    """Expose exact source bytes for build/tests when that authority exists."""
    source = _source_authority_path(_filename(resource_id))
    try:
        return source.read_bytes()
    except OSError:
        return None

