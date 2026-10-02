"""Audit only the identity of a local exploratory capture corpus.

The manifest intentionally contains no packet payload and no machine-absolute path.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_errors(manifest: dict, corpus_root: Path) -> list[str]:
    errors: list[str] = []
    captures = manifest.get("captures")
    if not isinstance(captures, list) or not captures:
        return ["captures must be a nonempty array"]
    seen: set[str] = set()
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
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts or "\\" in relative:
            errors.append(f"{ident}: relativePath is unsafe")
            continue
        candidate = corpus_root.joinpath(*pure.parts)
        if not candidate.is_file():
            errors.append(f"{ident}: capture is missing")
            continue
        if candidate.stat().st_size != row.get("byteCount"):
            errors.append(f"{ident}: byteCount differs")
        if _digest(candidate) != row.get("sha256"):
            errors.append(f"{ident}: sha256 differs")
    if manifest.get("captureCount") != len(captures):
        errors.append("captureCount differs from captures length")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--corpus-root", required=True, type=Path)
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"manifest is unreadable: {exc}", file=sys.stderr)
        return 1
    errors = audit_errors(manifest, args.corpus_root)
    if errors:
        print("capture-manifest audit failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"capture-manifest audit passed: captures={manifest['captureCount']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
