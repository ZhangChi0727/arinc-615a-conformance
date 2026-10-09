"""Audit only the identity of a local exploratory capture corpus.

The manifest intentionally contains no packet payload and no machine-absolute path.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "configs/research/cltav_historical_capture_manifest.schema.json"


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative_path(value: object) -> PurePosixPath | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    if posix.is_absolute() or windows.is_absolute() or windows.drive or ".." in posix.parts:
        return None
    return posix


def audit_errors(manifest: dict, corpus_root: Path, schema: dict) -> list[str]:
    errors: list[str] = []
    errors.extend(f"schema: {error.message}" for error in Draft202012Validator(schema).iter_errors(manifest))
    if errors:
        return errors
    try:
        root = corpus_root.resolve(strict=True)
    except OSError:
        return ["corpus root is missing or unreadable"]
    if not root.is_dir():
        return ["corpus root is not a directory"]
    captures = manifest.get("captures")
    if not isinstance(captures, list) or not captures:
        return ["captures must be a nonempty array"]
    seen: set[str] = set()
    declared_paths: set[PurePosixPath] = set()
    resolved_identities: set[tuple[int, int]] = set()
    for row in captures:
        ident = row.get("captureId") if isinstance(row, dict) else None
        relative = row.get("relativePath") if isinstance(row, dict) else None
        if not isinstance(ident, str) or ident in seen:
            errors.append(f"captureId is missing or repeated: {ident!r}")
            continue
        seen.add(ident)
        if not isinstance(relative, str):
            errors.append(f"{ident}: relativePath missing")
            continue
        pure = _safe_relative_path(relative)
        if pure is None:
            errors.append(f"{ident}: relativePath is unsafe")
            continue
        if pure in declared_paths:
            errors.append(f"{ident}: relativePath is repeated")
            continue
        declared_paths.add(pure)
        candidate = root.joinpath(*pure.parts)
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError):
            errors.append(f"{ident}: resolved path escapes corpus root")
            continue
        if not resolved.is_file():
            errors.append(f"{ident}: capture is missing")
            continue
        stat = resolved.stat()
        file_identity = (stat.st_dev, stat.st_ino)
        if file_identity in resolved_identities:
            errors.append(f"{ident}: resolved file identity is repeated")
            continue
        resolved_identities.add(file_identity)
        if stat.st_size != row.get("byteCount"):
            errors.append(f"{ident}: byteCount differs")
        if _digest(candidate) != row.get("sha256"):
            errors.append(f"{ident}: sha256 differs")
    if manifest.get("captureCount") != len(captures):
        errors.append("captureCount differs from captures length")
    actual_paths = {
        PurePosixPath(path.relative_to(root).as_posix())
        for path in root.rglob("*") if path.is_file()
    }
    if actual_paths != declared_paths:
        missing = actual_paths - declared_paths
        extra = declared_paths - actual_paths
        if missing:
            errors.append(f"manifest omits corpus files: {len(missing)}")
        if extra:
            errors.append(f"manifest declares non-corpus files: {len(extra)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--corpus-root", required=True, type=Path)
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"manifest is unreadable: {exc}", file=sys.stderr)
        return 1
    errors = audit_errors(manifest, args.corpus_root, schema)
    if errors:
        print("capture-manifest audit failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"capture-manifest audit passed: captures={manifest['captureCount']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
