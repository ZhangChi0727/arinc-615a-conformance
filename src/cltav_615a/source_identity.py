"""Bind a direct B object to the source that matches its loaded module code.

Each bounded package module registers while its module frame is executing.
The captured bytes are compiled and compared with that executing code, then
LF-normalized for hashing and retention.  Constructors never relabel cached
code with later disk bytes.
This is source provenance for ordinary Python loading, not a monkeypatch sandbox.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import sys


SCHEME = "CLTAV-615A-LOADED-SOURCE-SHA256-LF-V1"
MODULE_FILES = {
    "cltav_615a": "__init__.py",
    "cltav_615a.source_identity": "source_identity.py",
    "cltav_615a.types": "types.py",
    "cltav_615a.objects": "objects.py",
    "cltav_615a.controller": "controller.py",
}


class SourceIdentityError(ValueError):
    """A named source/loaded-code binding failure, before an attempt exists."""


@dataclass(frozen=True)
class SourceFileIdentity:
    path: str
    sha256: str
    byte_size: int


@dataclass(frozen=True)
class LoadedSourceIdentity:
    scheme: str
    digest: str
    files: tuple[SourceFileIdentity, ...]

    @property
    def identifier(self) -> str:
        return f"{self.scheme}:{self.digest}"


_PACKAGE_ROOT = Path(__file__).resolve().parent
_LOADED: dict[str, tuple[Path, bytes]] = {}


def _source_bytes(path: Path) -> bytes:
    try:
        if path.is_symlink() or not path.is_file() or path.resolve().parent != _PACKAGE_ROOT:
            raise SourceIdentityError("SOURCE-IDENTITY-UNSAFE-OR-MISSING-FILE")
        raw = path.read_bytes()
        raw.decode("utf-8")
        return raw
    except (OSError, UnicodeError) as exc:
        raise SourceIdentityError("SOURCE-IDENTITY-UNREADABLE-FILE") from exc


def register_loaded_module(module_name: str, source_file: str) -> None:
    """Capture source only if it compiles to the currently executing module."""

    expected = MODULE_FILES.get(module_name)
    path = Path(source_file)
    if expected is None or path.name != expected:
        raise SourceIdentityError("SOURCE-IDENTITY-UNEXPECTED-MODULE")
    raw = _source_bytes(path)
    frame = sys._getframe(1)
    if frame.f_globals.get("__name__") != module_name or frame.f_code.co_name != "<module>":
        raise SourceIdentityError("SOURCE-IDENTITY-NOT-MODULE-EXECUTION")
    if any(Path(value).resolve() != path.resolve() for value in (
        frame.f_globals.get("__file__", ""), frame.f_code.co_filename,
    )):
        raise SourceIdentityError("SOURCE-IDENTITY-MODULE-PATH-MISMATCH")
    try:
        compiled = compile(raw, frame.f_code.co_filename, "exec", dont_inherit=True, optimize=sys.flags.optimize)
    except (SyntaxError, ValueError) as exc:
        raise SourceIdentityError("SOURCE-IDENTITY-INVALID-SOURCE") from exc
    if compiled != frame.f_code:
        raise SourceIdentityError("SOURCE-IDENTITY-LOADED-CODE-MISMATCH")
    content = raw.decode("utf-8").replace("\r\n", "\n").encode("utf-8")
    existing = _LOADED.get(module_name)
    if existing is not None and existing != (path.resolve(), content):
        raise SourceIdentityError("SOURCE-IDENTITY-RELOAD-MISMATCH")
    _LOADED[module_name] = (path.resolve(), content)


def loaded_source_identity() -> LoadedSourceIdentity:
    """Return an immutable complete binding, refusing missing or drifted files."""

    if set(_LOADED) != set(MODULE_FILES):
        raise SourceIdentityError("SOURCE-IDENTITY-INCOMPLETE-MODULE-SET")
    records = []
    for name, filename in sorted(MODULE_FILES.items(), key=lambda item: item[1]):
        path, content = _LOADED[name]
        module = sys.modules.get(name)
        if module is None or Path(getattr(module, "__file__", "")).resolve() != path:
            raise SourceIdentityError("SOURCE-IDENTITY-MODULE-PATH-MISMATCH")
        if _source_bytes(path).decode("utf-8").replace("\r\n", "\n").encode("utf-8") != content:
            raise SourceIdentityError("SOURCE-IDENTITY-SOURCE-DRIFT")
        records.append(SourceFileIdentity(f"src/cltav_615a/{filename}", sha256(content).hexdigest(), len(content)))
    encoded = json.dumps(
        [(row.path, row.sha256, row.byte_size) for row in records], separators=(",", ":"), ensure_ascii=True,
    ).encode("utf-8")
    return LoadedSourceIdentity(SCHEME, sha256(encoded).hexdigest(), tuple(records))


register_loaded_module(__name__, __file__)
