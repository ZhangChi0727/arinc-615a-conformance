"""Authority-repository and loaded-code identity for D-stage evidence."""

from __future__ import annotations

from importlib import resources
from hashlib import sha256
from pathlib import Path
import subprocess
from typing import Any

from cltav_615a.source_identity import loaded_source_identity
from cltav_615a_adapter.contract import (
    H_B_COMMIT,
    H_B_SCENARIO_GIT_BLOB_OID,
    H_B_SCENARIO_RAW_SHA256,
    SCENARIO_PATH,
)
from cltav_615a_adapter.identity import loaded_adapter_source_identity
from cltav_runtime.bindings import SourceSnapshot

from .errors import EngineeringError

ARTIFACT_TYPE = "CLTAV-615A-ENGINEERING-EVIDENCE-V1"
PRODUCER_MODE = "CLTAV-615A-ENGINEERING-CONTROL-SLICE-V1"
SCHEMA_ID = "cltav://615a/engineering-evidence/v1"
FORBIDDEN_G3_MODES = (
    "cltav-runtime-finite-fault-driver",
    "cltav-runtime-synthetic-environment",
    "g3-two-round-alpha",
)
COMMIT_RE = __import__("re").compile(r"^[0-9a-f]{40}$")


def schema_bytes() -> bytes:
    source = resources.files("cltav_615a_engineering.resources").joinpath(
        "engineering_evidence.schema.json",
    )
    try:
        raw = source.read_bytes()
    except (OSError, FileNotFoundError) as exc:
        raise EngineeringError("SCHEMA-RESOURCE-MISSING", "packaged evidence schema is missing") from exc
    if not raw:
        raise EngineeringError("SCHEMA-RESOURCE-MISSING", "packaged evidence schema is empty")
    return raw


def require_commit(value: str) -> str:
    if not isinstance(value, str) or COMMIT_RE.fullmatch(value) is None:
        raise EngineeringError("AUTHORITY-COMMIT-MALFORMED", "authority commit must be 40 lowercase hex characters")
    return value


def require_repository(path: Path) -> Path:
    if not isinstance(path, Path):
        raise EngineeringError("AUTHORITY-REPOSITORY-INVALID", "authority repository must be a path")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise EngineeringError("AUTHORITY-REPOSITORY-INVALID", "authority repository cannot be resolved") from exc
    if resolved.is_symlink() or not resolved.is_dir():
        raise EngineeringError("AUTHORITY-REPOSITORY-INVALID", "authority repository must be an ordinary directory")
    git_dir = resolved / ".git"
    if not git_dir.exists():
        raise EngineeringError("AUTHORITY-REPOSITORY-INVALID", "authority repository is not a Git directory")
    return resolved


def _git(repository: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repository), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise EngineeringError(
            "AUTHORITY-GIT-UNAVAILABLE",
            completed.stderr.strip() or "git identity command failed",
        )
    return completed.stdout.strip()


def verify_authority_commit(repository: Path, commit: str) -> str:
    require_commit(commit)
    kind = _git(repository, "cat-file", "-t", commit)
    if kind != "commit":
        raise EngineeringError("AUTHORITY-COMMIT-MISSING", "authority commit is not a Git commit object")
    hb_kind = _git(repository, "cat-file", "-t", H_B_COMMIT)
    if hb_kind != "commit":
        raise EngineeringError("HB-AUTHORITY-MISSING", "accepted H-B commit is not present in the authority repository")
    return commit


def scenario_identity(repository: Path) -> dict[str, str]:
    snapshot = SourceSnapshot.from_git_object(
        repository=repository,
        commit=H_B_COMMIT,
        path=SCENARIO_PATH,
    )
    raw = snapshot._content
    digest = sha256(raw).hexdigest()
    if digest != H_B_SCENARIO_RAW_SHA256:
        raise EngineeringError("HB-SCENARIO-IDENTITY-MISMATCH", "H-B scenario raw digest does not match the C pin")
    return {
        "commit": H_B_COMMIT,
        "path": SCENARIO_PATH,
        "gitBlobOid": H_B_SCENARIO_GIT_BLOB_OID,
        "rawSha256": digest,
        "acceptedAuthorityCommit": "c577f34e98b91083a69f0a731a990c01aa7fa08b",
    }


def _file_digest(path: Path) -> dict[str, str | int]:
    raw = path.read_bytes().decode("utf-8").replace("\r\n", "\n").encode("utf-8")
    return {"path": path.name, "sha256": sha256(raw).hexdigest(), "byteSize": len(raw)}


def implementation_identities() -> dict[str, Any]:
    import cltav_runtime.session as runtime_session

    adapter = loaded_adapter_source_identity()
    objects = loaded_source_identity()
    engineering_root = Path(__file__).resolve().parent
    engineering_files = []
    for name in sorted(p.name for p in engineering_root.glob("*.py")):
        engineering_files.append(_file_digest(engineering_root / name))
    runtime_path = Path(runtime_session.__file__).resolve()
    return {
        "objectSource": objects.identifier,
        "adapterSource": adapter.identifier,
        "adapterFiles": [
            {"path": item.path, "sha256": item.sha256, "byteSize": item.byte_size}
            for item in adapter.files
        ],
        "runtimeSession": _file_digest(runtime_path),
        "engineeringFiles": engineering_files,
    }
