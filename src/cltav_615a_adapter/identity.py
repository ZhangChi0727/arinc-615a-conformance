"""Loaded-source identity for the independent C-stage adapter package.

The C adapter is intentionally not included in the accepted B object source
manifest.  This small sibling manifest therefore proves exactly which adapter
modules were loaded, without redefining the B object identity.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import sys


SCHEME = "CLTAV-615A-C-ADAPTER-LOADED-SOURCE-SHA256-LF-V1"
MODULE_FILES = {
    "cltav_615a_adapter": "__init__.py",
    "cltav_615a_adapter.identity": "identity.py",
    "cltav_615a_adapter.contract": "contract.py",
    "cltav_615a_adapter.session": "session.py",
}


class AdapterSourceIdentityError(ValueError):
    """Raised before an adapter can run when its source binding is invalid."""


@dataclass(frozen=True)
class AdapterSourceFileIdentity:
    """One normalized adapter source-file identity."""

    path: str
    sha256: str
    byte_size: int


@dataclass(frozen=True)
class AdapterSourceIdentity:
    """Complete loaded-source identity for the C adapter only."""

    scheme: str
    digest: str
    files: tuple[AdapterSourceFileIdentity, ...]

    @property
    def identifier(self) -> str:
        return f"{self.scheme}:{self.digest}"


_PACKAGE_ROOT = Path(__file__).resolve().parent
_LOADED: dict[str, tuple[Path, bytes]] = {}


def _source_bytes(path: Path) -> bytes:
    try:
        if path.is_symlink() or not path.is_file() or path.resolve().parent != _PACKAGE_ROOT:
            raise AdapterSourceIdentityError("C-ADAPTER-SOURCE-UNSAFE-OR-MISSING-FILE")
        raw = path.read_bytes()
        raw.decode("utf-8")
        return raw
    except (OSError, UnicodeError) as exc:
        raise AdapterSourceIdentityError("C-ADAPTER-SOURCE-UNREADABLE-FILE") from exc


def register_loaded_module(module_name: str, source_file: str) -> None:
    """Capture only source whose code object is executing this module."""

    expected = MODULE_FILES.get(module_name)
    path = Path(source_file)
    if expected is None or path.name != expected:
        raise AdapterSourceIdentityError("C-ADAPTER-SOURCE-UNEXPECTED-MODULE")
    raw = _source_bytes(path)
    frame = sys._getframe(1)
    if frame.f_globals.get("__name__") != module_name or frame.f_code.co_name != "<module>":
        raise AdapterSourceIdentityError("C-ADAPTER-SOURCE-NOT-MODULE-EXECUTION")
    if any(Path(value).resolve() != path.resolve() for value in (
        frame.f_globals.get("__file__", ""), frame.f_code.co_filename,
    )):
        raise AdapterSourceIdentityError("C-ADAPTER-SOURCE-MODULE-PATH-MISMATCH")
    try:
        compiled = compile(raw, frame.f_code.co_filename, "exec", dont_inherit=True, optimize=sys.flags.optimize)
    except (SyntaxError, ValueError) as exc:
        raise AdapterSourceIdentityError("C-ADAPTER-SOURCE-INVALID") from exc
    if compiled != frame.f_code:
        raise AdapterSourceIdentityError("C-ADAPTER-SOURCE-LOADED-CODE-MISMATCH")
    normalized = raw.decode("utf-8").replace("\r\n", "\n").encode("utf-8")
    existing = _LOADED.get(module_name)
    if existing is not None and existing != (path.resolve(), normalized):
        raise AdapterSourceIdentityError("C-ADAPTER-SOURCE-RELOAD-MISMATCH")
    _LOADED[module_name] = (path.resolve(), normalized)


def loaded_adapter_source_identity() -> AdapterSourceIdentity:
    """Return the closed four-file C adapter identity, or fail closed."""

    if set(_LOADED) != set(MODULE_FILES):
        raise AdapterSourceIdentityError("C-ADAPTER-SOURCE-INCOMPLETE-MODULE-SET")
    records: list[AdapterSourceFileIdentity] = []
    for module_name, filename in sorted(MODULE_FILES.items(), key=lambda row: row[1]):
        path, content = _LOADED[module_name]
        module = sys.modules.get(module_name)
        if module is None or Path(getattr(module, "__file__", "")).resolve() != path:
            raise AdapterSourceIdentityError("C-ADAPTER-SOURCE-MODULE-PATH-MISMATCH")
        fresh = _source_bytes(path).decode("utf-8").replace("\r\n", "\n").encode("utf-8")
        if fresh != content:
            raise AdapterSourceIdentityError("C-ADAPTER-SOURCE-DRIFT")
        records.append(AdapterSourceFileIdentity(
            f"src/cltav_615a_adapter/{filename}", sha256(content).hexdigest(), len(content),
        ))
    encoded = json.dumps(
        [(item.path, item.sha256, item.byte_size) for item in records],
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return AdapterSourceIdentity(SCHEME, sha256(encoded).hexdigest(), tuple(records))


register_loaded_module(__name__, __file__)
