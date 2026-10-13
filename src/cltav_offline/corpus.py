"""Safe local-corpus identity audit and transactional evidence publication."""

from __future__ import annotations

import json
import os
import re
import shutil
import uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from .evidence import evidence_errors
from .pipeline import (
    IntakeConfig,
    IntakeError,
    input_identity,
    run_capture,
    validate_source_commit,
)


_ABSOLUTE_PATH_RE = re.compile(r"(?:^|[\s\"'])((?:[A-Za-z]:[\\/])|/(?:[^\s\"']+))")


def safe_relative_path(value: object) -> PurePosixPath | None:
    if not isinstance(value, str) or not value.strip() or "\\" in value:
        return None
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    if posix.is_absolute() or windows.is_absolute() or windows.drive or ".." in posix.parts:
        return None
    return posix


def audit_manifest(manifest: dict[str, Any], corpus_root: Path) -> list[str]:
    """Audit manifest identity with the same path/alias/inventory boundary as CI."""
    expected_keys = {
        "manifestId", "manifestVersion", "purpose", "captureCount", "truthBoundary", "captures",
    }
    errors: list[str] = []
    if set(manifest) != expected_keys:
        errors.append("manifest top-level fields differ from the controlled schema")
        return errors
    if manifest.get("manifestId") != "CLTAV-HISTORICAL-CAPTURES":
        errors.append("manifestId is not CLTAV-HISTORICAL-CAPTURES")
    if manifest.get("manifestVersion") != "1.0":
        errors.append("manifestVersion is not 1.0")
    if manifest.get("purpose") != "EXPLORATORY-DEVELOPMENT-ONLY":
        errors.append("manifest purpose is not exploratory-development-only")
    if not isinstance(manifest.get("truthBoundary"), str) or not manifest["truthBoundary"].strip():
        errors.append("manifest truthBoundary is missing")
    try:
        root = corpus_root.resolve(strict=True)
    except OSError:
        return errors + ["corpus root is missing or unreadable"]
    if not root.is_dir():
        return errors + ["corpus root is not a directory"]
    captures = manifest.get("captures")
    if not isinstance(captures, list) or not captures:
        return errors + ["captures must be a nonempty array"]
    if manifest.get("captureCount") != len(captures):
        errors.append("captureCount differs from captures length")
    seen_ids: set[str] = set()
    declared_paths: set[PurePosixPath] = set()
    identities: set[tuple[int, int]] = set()
    expected_row_keys = {
        "captureId", "relativePath", "byteCount", "sha256", "observationQuality", "labelSource", "rootCause",
    }
    for index, row in enumerate(captures):
        label = f"captures[{index}]"
        if not isinstance(row, dict) or set(row) != expected_row_keys:
            errors.append(f"{label} fields differ from the controlled schema")
            continue
        capture_id = row.get("captureId")
        if not isinstance(capture_id, str) or not capture_id or capture_id in seen_ids:
            errors.append(f"{label} captureId is missing or repeated")
            continue
        seen_ids.add(capture_id)
        if row.get("observationQuality") != "UNASSESSED-EXPLORATORY":
            errors.append(f"{capture_id} observationQuality is not exploratory")
        if row.get("labelSource") != "FILE-ANNOTATION-NONTRUTH":
            errors.append(f"{capture_id} labelSource is not nontruth")
        if row.get("rootCause") != "UNKNOWN":
            errors.append(f"{capture_id} rootCause must remain UNKNOWN")
        relative = safe_relative_path(row.get("relativePath"))
        if relative is None:
            errors.append(f"{capture_id} relativePath is unsafe")
            continue
        if relative in declared_paths:
            errors.append(f"{capture_id} relativePath is repeated")
            continue
        declared_paths.add(relative)
        candidate = root.joinpath(*relative.parts)
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(root)
            stat = resolved.stat()
        except (OSError, ValueError):
            errors.append(f"{capture_id} resolved path escapes corpus root or is missing")
            continue
        if not resolved.is_file():
            errors.append(f"{capture_id} is not an ordinary file")
            continue
        identity = (stat.st_dev, stat.st_ino)
        if identity in identities:
            errors.append(f"{capture_id} resolved file identity is repeated")
        identities.add(identity)
        actual = input_identity(resolved)
        if actual[0] != row.get("byteCount"):
            errors.append(f"{capture_id} byteCount differs")
        if actual[1] != row.get("sha256"):
            errors.append(f"{capture_id} sha256 differs")
    actual_paths = {
        PurePosixPath(item.relative_to(root).as_posix())
        for item in root.rglob("*") if item.is_file()
    }
    if actual_paths != declared_paths:
        if actual_paths - declared_paths:
            errors.append(f"manifest omits corpus files: {len(actual_paths - declared_paths)}")
        if declared_paths - actual_paths:
            errors.append(f"manifest declares non-corpus files: {len(declared_paths - actual_paths)}")
    return errors


def load_and_audit_manifest(manifest_path: Path, corpus_root: Path) -> dict[str, Any]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntakeError("MANIFEST-READ-ERROR", str(exc)) from exc
    if not isinstance(manifest, dict):
        raise IntakeError("MANIFEST-INVALID", "manifest must be an object")
    errors = audit_manifest(manifest, corpus_root)
    if errors:
        raise IntakeError("CORPUS-IDENTITY-AUDIT-FAILED", "; ".join(errors))
    return manifest


def publish_json(data: dict[str, Any], output: Path) -> None:
    """Atomically replace one JSON output; a failed stage never overwrites old bytes."""
    output_parent = output.parent
    output_parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and output.is_symlink():
        raise IntakeError("UNSAFE-OUTPUT-PATH", "output file must not be a symbolic link")
    stage = output_parent / f".{output.name}.staging-{uuid.uuid4().hex}"
    try:
        with stage.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        # Read back staged JSON before replacing an existing result.
        json.loads(stage.read_text(encoding="utf-8"))
        os.replace(stage, output)
    except OSError as exc:
        raise IntakeError("OUTPUT-PUBLISH-ERROR", str(exc)) from exc
    finally:
        if stage.exists():
            stage.unlink()


def run_corpus(
    *,
    manifest_path: Path,
    corpus_root: Path,
    output_dir: Path,
    config: IntakeConfig,
    source_commit: str,
) -> dict[str, Any]:
    """Audit then process every declared corpus input into one staged directory."""
    source_commit = validate_source_commit(source_commit)
    manifest = load_and_audit_manifest(manifest_path, corpus_root)
    root = corpus_root.resolve(strict=True)
    target = output_dir.resolve(strict=False)
    try:
        target.relative_to(root)
    except ValueError:
        pass
    else:
        raise IntakeError("UNSAFE-OUTPUT-PATH", "corpus output must not be inside its input root")
    if target.exists() and target.is_symlink():
        raise IntakeError("UNSAFE-OUTPUT-PATH", "corpus output directory must not be a symbolic link")
    if target.exists() and not target.is_dir():
        raise IntakeError("UNSAFE-OUTPUT-PATH", "corpus output target must be a directory")
    parent = target.parent
    parent.mkdir(parents=True, exist_ok=True)
    stage = parent / f".{target.name}.staging-{uuid.uuid4().hex}"
    stage.mkdir()
    rows: list[dict[str, Any]] = []
    try:
        for row in sorted(manifest["captures"], key=lambda item: item["captureId"]):
            capture_id = row["captureId"]
            input_path = root.joinpath(*PurePosixPath(row["relativePath"]).parts)
            output = stage / f"{capture_id}.json"
            try:
                result = run_capture(
                    input_path,
                    capture_id=capture_id,
                    config=config,
                    expected_identity=(row["byteCount"], row["sha256"]),
                )
                data = result.to_dict(source_commit=source_commit)
                errors = evidence_errors(data)
                if errors:
                    raise IntakeError("EVIDENCE-SCHEMA-ERROR", "; ".join(errors))
                publish_json(data, output)
                rows.append({
                    "captureId": capture_id,
                    "inputSha256": row["sha256"],
                    "outputSha256": input_identity(output)[1],
                    "executionStatus": data["executionStatus"],
                    "diagnosticCount": data["counts"]["diagnostics"],
                })
            except IntakeError as exc:
                failure = _failure_evidence(capture_id, row, config, source_commit, exc)
                errors = evidence_errors(failure)
                if errors:
                    raise IntakeError("EVIDENCE-SCHEMA-ERROR", "; ".join(errors))
                publish_json(failure, output)
                rows.append({
                    "captureId": capture_id,
                    "inputSha256": row["sha256"],
                    "outputSha256": input_identity(output)[1],
                    "executionStatus": "FATAL-INPUT-ERROR",
                    "diagnosticCount": 1,
                })
        summary = {
            "artifactType": "CLTAV-OFFLINE-INTAKE-CORPUS-INDEX",
            "schemaVersion": "1.0",
            "manifestId": manifest["manifestId"],
            "manifestVersion": manifest["manifestVersion"],
            "purpose": manifest["purpose"],
            "sourceCommit": source_commit,
            "captureCount": len(rows),
            "captures": rows,
            "conformanceVerdict": "NOT-EVALUATED",
            "note": "No capture payload, absolute local path, root-cause finding or experimental truth is recorded.",
        }
        publish_json(summary, stage / "corpus-index.json")
        _publish_directory(stage, target)
    except Exception:
        if stage.exists():
            shutil.rmtree(stage)
        raise
    return summary


def _publish_directory(stage: Path, target: Path) -> None:
    """Replace a directory with rollback if the second rename fails."""
    backup = target.parent / f".{target.name}.backup-{uuid.uuid4().hex}"
    moved_old = False
    try:
        if target.exists():
            os.replace(target, backup)
            moved_old = True
        os.replace(stage, target)
    except OSError as exc:
        if moved_old and backup.exists() and not target.exists():
            os.replace(backup, target)
        raise IntakeError("OUTPUT-PUBLISH-ERROR", str(exc)) from exc
    else:
        if backup.exists():
            shutil.rmtree(backup)


def _failure_evidence(
    capture_id: str,
    row: dict[str, Any],
    config: IntakeConfig,
    source_commit: str,
    error: IntakeError,
) -> dict[str, Any]:
    return {
        "artifactType": "CLTAV-OFFLINE-INTAKE-EVIDENCE",
        "schemaVersion": "1.0",
        "evidenceBoundary": {
            "purpose": "EXPLORATORY-DEVELOPMENT-ONLY",
            "conformanceVerdict": "NOT-EVALUATED",
        },
        "tool": {"name": "cltav-offline", "sourceCommit": source_commit},
        "input": {
            "captureId": capture_id,
            "byteCount": row["byteCount"],
            "sha256": row["sha256"],
        },
        "runParameters": config.to_dict(),
        "executionStatus": "FATAL-INPUT-ERROR",
        "counts": {
            "containerPackets": 0,
            "evidencePacketRefs": 0,
            "datagrams": 0,
            "transfers": 0,
            "events": 0,
            "diagnostics": 1,
        },
        "packetRefs": [],
        "datagrams": [],
        "transfers": [],
        "events": [],
        "diagnostics": [{
            "code": error.code,
            "stage": "INPUT",
            "message": _public_error_message(error),
        }],
    }


def _public_error_message(error: IntakeError) -> str:
    """Keep a stable cause without publishing a caller's local filesystem path."""
    message = str(error)
    if error.code == "INPUT-READ-ERROR" or _ABSOLUTE_PATH_RE.search(message):
        return "the declared capture input could not be read"
    return message
