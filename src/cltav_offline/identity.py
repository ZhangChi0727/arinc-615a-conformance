"""Runtime and controlled-contract identities for offline evidence.

A supplied Git OID identifies a caller's claim.  The package never infers it
from whichever repository happens to be the process working directory.  A
recomputable source snapshot instead identifies the Python modules actually
loaded by this invocation.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


# SHA-256 of the accepted development-contract snapshot consumed by this
# bounded adapter.  This is deliberately a content identity, not "latest".
DEVELOPMENT_CONTRACT_PATH = "configs/engineering/cltav_development_contracts.json"
DEVELOPMENT_CONTRACT_SHA256 = "3331fadf2786133f161eded9d1fb42066ca58d7dd510ce6e775da1cd89a5aae1"


def runtime_source_snapshot_sha256() -> str:
    """Hash loaded-package source deterministically without consulting Git/CWD."""
    package_root = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    for path in sorted(package_root.rglob("*.py"), key=lambda item: item.relative_to(package_root).as_posix()):
        relative = path.relative_to(package_root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        content = path.read_bytes()
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def tool_identity(claimed_source_commit: str) -> dict[str, object]:
    """Render a non-deceptive identity object for a published evidence run."""
    return {
        "name": "cltav-offline",
        "sourceCommit": claimed_source_commit,
        "sourceCommitStatus": (
            "UNAVAILABLE" if claimed_source_commit == "UNVERIFIED" else "CLAIMED-UNVERIFIED"
        ),
        "runtimeSourceSha256": runtime_source_snapshot_sha256(),
        "contractIds": ["CR-2026-016", "CR-2026-017", "DD-038", "DD-040", "DD-041"],
        "contractIdentities": [{
            "path": DEVELOPMENT_CONTRACT_PATH,
            "sha256": DEVELOPMENT_CONTRACT_SHA256,
            "version": "PR19-ACCEPTED-SNAPSHOT",
        }],
    }
