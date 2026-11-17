"""Per-attempt reset evidence (DEP-RESET).  Does not close DEC-IUT."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from json import dumps
from typing import Any, Mapping
from uuid import uuid4

from a615a_sim.bound_iut.protocol import SimulatedTarget


@dataclass(frozen=True)
class ResetEvidence:
    pairing_id: str
    reset_id: str
    reset_evidence_ref: str
    confirmed: bool
    snapshot: Mapping[str, Any]

    def as_mapping(self) -> Mapping[str, Any]:
        return {
            "pairingId": self.pairing_id,
            "resetId": self.reset_id,
            "resetEvidenceRef": self.reset_evidence_ref,
            "resetConfirmed": self.confirmed,
            "snapshot": dict(self.snapshot),
            "label": "SIMULATED-IUT",
        }


def reset_target(target: SimulatedTarget, *, pairing_id: str | None = None) -> ResetEvidence:
    snapshot = target.reset()
    payload = dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = sha256(payload).hexdigest()
    reset_id = f"RST-{uuid4().hex[:12]}"
    return ResetEvidence(
        pairing_id=pairing_id or f"PAIR-{uuid4().hex[:8]}",
        reset_id=reset_id,
        reset_evidence_ref=f"sha256:{digest}",
        confirmed=snapshot["state"] == "IDLE" and snapshot["faultId"] is None,
        snapshot=snapshot,
    )
