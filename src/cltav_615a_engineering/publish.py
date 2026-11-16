"""Transactional directory publication for 615A engineering evidence."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4

from .errors import EngineeringError
from .jsonutil import canonical_json_bytes
from .verify import verify_document

ALGORITHM_DIR = "algorithm-visible"
EVALUATOR_DIR = "evaluator-audit"
MANIFEST_NAME = "manifest.json"


def _is_unsafe_component(path: Path) -> bool:
    return path.is_symlink() or any(parent.is_symlink() for parent in path.parents)


def safe_output_directory(output: Path, repository: Path) -> Path:
    if not isinstance(output, Path) or not output.name or output.name in {".", ".."}:
        raise EngineeringError("UNSAFE-OUTPUT-PATH", "evidence output directory is invalid")
    try:
        parent = output.parent.absolute()
        if not parent.is_dir():
            raise EngineeringError("UNSAFE-OUTPUT-PATH", "evidence output parent must exist")
        if _is_unsafe_component(parent):
            raise EngineeringError("UNSAFE-OUTPUT-PATH", "evidence output parent must not be a symlink")
        resolved_parent = parent.resolve(strict=True)
        target = resolved_parent / output.name
        repo = repository.resolve(strict=True)
    except OSError as exc:
        raise EngineeringError("UNSAFE-OUTPUT-PATH", "evidence output path cannot be resolved") from exc
    if target.exists() and (target.is_symlink() or not target.is_dir()):
        raise EngineeringError("UNSAFE-OUTPUT-PATH", "evidence output must be absent or an ordinary directory")
    try:
        target.relative_to(repo)
    except ValueError:
        return target
    raise EngineeringError("UNSAFE-OUTPUT-PATH", "evidence output must not be inside the authority repository")


def _write_tree(root: Path, document: dict[str, Any]) -> None:
    algorithm = root / ALGORITHM_DIR
    evaluator = root / EVALUATOR_DIR
    algorithm.mkdir(parents=True)
    evaluator.mkdir(parents=True)
    visible = document["algorithmVisible"]
    audit = document["evaluatorAudit"]
    (algorithm / "identities.json").write_bytes(canonical_json_bytes(visible["identities"]))
    (algorithm / "configuration.json").write_bytes(canonical_json_bytes(visible["configuration"]))
    (algorithm / "journal.json").write_bytes(canonical_json_bytes(visible["journal"]))
    (algorithm / "rounds.json").write_bytes(canonical_json_bytes(visible["rounds"]))
    (algorithm / "stop.json").write_bytes(canonical_json_bytes(visible["stop"]))
    (algorithm / "recompute.json").write_bytes(canonical_json_bytes(visible["recompute"]))
    (algorithm / "unevaluated.json").write_bytes(canonical_json_bytes(visible["unevaluatedObligations"]))
    (algorithm / "fingerprint.json").write_bytes(canonical_json_bytes({
        "fingerprintSha256": visible["fingerprintSha256"],
    }))
    (evaluator / "fault.json").write_bytes(canonical_json_bytes(audit["faultPlan"]))
    (evaluator / "reset.json").write_bytes(canonical_json_bytes(audit["reset"]))
    (evaluator / "injection.json").write_bytes(canonical_json_bytes(audit["injection"]))
    (evaluator / "limitations.json").write_bytes(canonical_json_bytes(audit["truthLimitations"]))
    (evaluator / "delivery-withhold.json").write_bytes(canonical_json_bytes(audit["deliveryWithhold"]))
    envelope = canonical_json_bytes({
        "artifactType": document["artifactType"],
        "producerMode": document["producerMode"],
        "schemaId": document["schemaId"],
        "cliExitMeaning": document["cliExitMeaning"],
        "qualityStatus": document["qualityStatus"],
        "algorithmVisible": visible,
        "evaluatorAudit": audit,
    })
    (root / "envelope.json").write_bytes(envelope)
    manifest = {
        "artifactType": document["artifactType"],
        "producerMode": document["producerMode"],
        "layout": {
            "envelope": "envelope.json",
            "algorithmVisible": ALGORITHM_DIR,
            "evaluatorAudit": EVALUATOR_DIR,
        },
        "note": "This operator manifest must not be supplied as an algorithm input.",
        "qualityStatus": document["qualityStatus"],
        "caseId": visible["identities"]["caseId"],
        "stopReason": visible["stop"]["reason"],
        "cliExitMeaning": document["cliExitMeaning"],
    }
    (root / MANIFEST_NAME).write_bytes(canonical_json_bytes(manifest))


def _rmtree(path: Path) -> None:
    if not path.exists():
        return
    for child in sorted(path.rglob("*"), reverse=True):
        if child.is_file() or child.is_symlink():
            child.unlink()
        elif child.is_dir():
            child.rmdir()
    path.rmdir()


def publish_run(
    document: dict[str, Any],
    *,
    output: Path,
    repository: Path,
    replace_fn: Callable[[Path, Path], None] | None = None,
) -> dict[str, Any]:
    """Stage, re-validate, then replace a complete evidence directory."""

    mover = replace_fn or os.replace
    target = safe_output_directory(output, repository)
    parent = target.parent
    stage = parent / f".{target.name}.staging-{uuid4().hex}"
    backup = parent / f".{target.name}.backup-{uuid4().hex}"
    moved_old = False
    try:
        stage.mkdir(parents=False)
        _write_tree(stage, document)
        verify_document(document, repository=repository, authority_commit=document["algorithmVisible"]["identities"]["authorityCommit"])
        if target.exists():
            _assert_owned_directory(target, repository=repository)
            mover(target, backup)
            moved_old = True
        mover(stage, target)
    except EngineeringError:
        _rmtree(stage)
        if moved_old and backup.exists() and not target.exists():
            mover(backup, target)
        raise
    except OSError as exc:
        _rmtree(stage)
        if moved_old and backup.exists() and not target.exists():
            try:
                mover(backup, target)
            except OSError as rollback_exc:
                raise EngineeringError("EVIDENCE-ROLLBACK-ERROR", "directory replacement failed and rollback did not complete") from rollback_exc
        raise EngineeringError("EVIDENCE-PUBLISH-ERROR", "evidence directory publication could not complete") from exc
    finally:
        if stage.exists() and stage != target:
            _rmtree(stage)
        if backup.exists() and target.exists():
            _rmtree(backup)
    return document


def _assert_owned_directory(target: Path, *, repository: Path) -> None:
    envelope = target / "envelope.json"
    if not envelope.is_file():
        raise EngineeringError("UNSAFE-OUTPUT-PATH", "refusing to replace a directory not owned by this publisher")
    from .verify import load_evidence_directory

    try:
        existing = load_evidence_directory(target)
        verify_document(
            existing,
            repository=repository,
            authority_commit=existing["algorithmVisible"]["identities"]["authorityCommit"],
        )
    except EngineeringError as exc:
        raise EngineeringError("UNSAFE-OUTPUT-PATH", "refusing to replace a directory not owned by this publisher") from exc
