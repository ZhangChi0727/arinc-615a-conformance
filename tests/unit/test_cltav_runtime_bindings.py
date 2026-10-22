"""Production-facing authority and type checks for the session runtime."""

from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from cltav_runtime.bindings import NAMED_INTERFACE_ADAPTERS, RuntimeAuthorityBinding, SourceSnapshot
from cltav_runtime.types import HistoryHandle, SessionContext


ROOT = Path(__file__).resolve().parents[2]
DEVELOPMENT_PATH = "configs/engineering/cltav_development_contracts.json"
INTERFACE_PATH = "configs/research/cltav_interface_registry.json"


def _head_commit() -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def test_runtime_binding_reads_exact_git_objects_not_the_worktree() -> None:
    binding = RuntimeAuthorityBinding.from_git_objects(
        repository=ROOT,
        development_commit=_head_commit(),
        development_path=DEVELOPMENT_PATH,
        interface_commit=_head_commit(),
        interface_path=INTERFACE_PATH,
    )

    identities = binding.identities()
    assert binding.development_artifact_id == "CLTAV-DEVELOPMENT-CONTRACTS"
    assert binding.finite_refinement_id == "AR-FINITE"
    assert "IF-HIST-UPDATE" in binding.interface_ids
    assert "HISTORY-HANDLE" in binding.record_ids
    assert set(binding.named_interface_adapters()) == binding.interface_ids
    assert binding.named_interface_adapters()["IF-SELECT-ADMIT"]["tStar"] == "selection.actionId"
    assert NAMED_INTERFACE_ADAPTERS["IF-HIST-UPDATE"]["Stop-Empty"] == "stop.empty"
    assert identities["development"]["commit"] == _head_commit()
    assert identities["interfaceRegistry"]["commit"] == _head_commit()
    assert len(identities["development"]["blobSha256"]) == 64
    assert len(identities["interfaceRegistry"]["blobSha256"]) == 64


@pytest.mark.parametrize("relative_path", ["../outside.json", "configs\\x.json"])
def test_source_snapshot_rejects_unsafe_relative_authority_paths(relative_path: str) -> None:
    with pytest.raises(ValueError, match="path"):
        SourceSnapshot.from_git_object(
            repository=ROOT, commit=_head_commit(), path=relative_path,
        )


def test_source_snapshot_rejects_runtime_derived_absolute_authority_path() -> None:
    with pytest.raises(ValueError, match="path"):
        SourceSnapshot.from_git_object(
            repository=ROOT,
            commit=_head_commit(),
            path=str(ROOT.resolve() / "outside.json"),
        )


def test_initial_history_permits_unset_member_statuses() -> None:
    history = HistoryHandle.initial(
        hypotheses={"h0", "h1"},
        compatible_state_by_hypothesis={"h0": "frontier-0", "h1": "frontier-1"},
    )

    assert history.status_by_hypothesis == {}
    assert history.version == 0
    assert history.processed is False
    with pytest.raises(ValueError, match="at least one"):
        HistoryHandle.initial(hypotheses=set(), compatible_state_by_hypothesis={})


def test_committed_history_requires_complete_controlled_statuses() -> None:
    with pytest.raises(ValueError, match="cover every"):
        HistoryHandle.committed(
            hypotheses={"h0", "h1"},
            compatible_state_by_hypothesis={"h0": "frontier-0", "h1": "frontier-1"},
            status_by_hypothesis={"h0": "KNOWN"},
            version=1,
        )
    with pytest.raises(ValueError, match="controlled vocabulary"):
        HistoryHandle.committed(
            hypotheses={"h0"},
            compatible_state_by_hypothesis={"h0": "frontier-0"},
            status_by_hypothesis={"h0": "BANANA"},
            version=1,
        )


def test_session_context_distinguishes_known_and_conservative_unknown() -> None:
    known = SessionContext.create(
        session_id="session-syn-001",
        run_id="run-syn-001",
        experiment_attempt_id=None,
        model_identity="model-1",
        current_summary="q0",
        q_status="KNOWN",
    )
    unknown = SessionContext.create(
        session_id="session-syn-001",
        run_id="run-syn-001",
        experiment_attempt_id=None,
        model_identity="model-1",
        current_summary=None,
        q_status="CONSERVATIVE-UNKNOWN",
    )

    assert known.current_summary == "q0"
    assert unknown.current_summary is None
    with pytest.raises(ValueError, match="requires a current summary"):
        SessionContext.create(
            session_id="session-syn-001",
            run_id="run-syn-001",
            experiment_attempt_id=None,
            model_identity="model-1",
            current_summary=None,
            q_status="KNOWN",
        )
