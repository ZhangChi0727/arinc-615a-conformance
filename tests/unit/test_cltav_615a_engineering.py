"""D-stage 615A engineering delivery: envelope, CLI, transactions, wheel."""

from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest

from cltav_615a_engineering.cli import main as engineering_main
from cltav_615a_engineering.envelope import compute_fingerprint, validate_envelope
from cltav_615a_engineering.errors import EngineeringError
from cltav_615a_engineering.publish import publish_run, safe_output_directory
from cltav_615a_engineering.runner import (
    CASE_ACCESS_GAP,
    CASE_EARLY_DATA,
    CASE_EARLY_WRQ,
    CASE_NORMAL,
    run_case,
)
from cltav_615a_engineering.verify import compare_semantic, load_evidence_directory, verify_document
from cltav_offline import cli as offline_cli
from cltav_runtime import cli as runtime_cli

ROOT = Path(__file__).resolve().parents[2]
COMMIT = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()


def _authority() -> list[str]:
    return [
        "--authority-repository", str(ROOT),
        "--authority-commit", COMMIT,
    ]


def _refresh(document: dict) -> dict:
    visible = document["algorithmVisible"]
    visible["fingerprintSha256"] = compute_fingerprint(visible)
    return document


def test_d02_envelope_rejects_evaluator_fields_and_g3_impersonation() -> None:
    executed = run_case(
        repository=ROOT,
        authority_commit=COMMIT,
        case_id=CASE_NORMAL,
        resource_mode="ROUNDS",
        resource_remaining=8,
    )
    leaked = deepcopy(executed.document)
    leaked["algorithmVisible"]["faultId"] = "EARLY-WRQ"
    with pytest.raises(EngineeringError) as rejected:
        validate_envelope(_refresh(leaked))
    assert rejected.value.code == "EVALUATOR-FIELD-IN-ALGORITHM-VISIBLE"
    g3 = deepcopy(executed.document)
    g3["producerMode"] = "cltav-runtime-finite-fault-driver"
    with pytest.raises(EngineeringError) as impersonation:
        validate_envelope(g3)
    assert impersonation.value.code == "G3-PRODUCER-IMPERSONATION"


@pytest.mark.parametrize("case_id", [CASE_NORMAL, CASE_EARLY_WRQ, CASE_EARLY_DATA, CASE_ACCESS_GAP])
def test_d01_run_verify_replay_semantic_consistency(tmp_path: Path, case_id: str) -> None:
    output = tmp_path / case_id.lower()
    assert engineering_main(["run", *_authority(), "--case-id", case_id, "--output", str(output)]) == 0
    document = load_evidence_directory(output)
    assert document["qualityStatus"] == "ENGINEERING-RECORD-VALID"
    assert document["cliExitMeaning"] == "ZERO-MEANS-VALID-ENGINEERING-RECORD-NOT-IUT-PASS"
    assert (output / "algorithm-visible").is_dir()
    assert (output / "evaluator-audit").is_dir()
    assert "faultPlan" not in document["algorithmVisible"]
    if case_id == CASE_ACCESS_GAP:
        assert document["algorithmVisible"]["stop"]["reason"] == "Stop-Prediction-Gap"
        assert "CONSERVATIVE-PREDICTION-GAP" in document["algorithmVisible"]["stop"]["diagnostics"]
        assert set(document["algorithmVisible"]["stop"]["historyStatuses"].values()) == {"CONSERVATIVE-UNKNOWN"}
    assert engineering_main(["verify", *_authority(), "--evidence", str(output)]) == 0
    assert engineering_main(["replay", *_authority(), "--evidence", str(output)]) == 0


def test_d01_six_tamper_classes_fail_after_fingerprint_refresh(tmp_path: Path) -> None:
    executed = run_case(
        repository=ROOT,
        authority_commit=COMMIT,
        case_id=CASE_EARLY_DATA,
        resource_mode="ROUNDS",
        resource_remaining=8,
    )

    def fail(mutator, code: str) -> None:
        tampered = mutator(deepcopy(executed.document))
        _refresh(tampered)
        with pytest.raises(EngineeringError) as rejected:
            verify_document(tampered, repository=ROOT, authority_commit=COMMIT)
        assert rejected.value.code == code

    def direction(document):
        document["algorithmVisible"]["journal"]["events"][-1]["direction"] = "DL-TO-TH"
        return document

    def version(document):
        document["algorithmVisible"]["rounds"][-1]["historyVersion"] = -1
        return document

    def cost(document):
        document["algorithmVisible"]["rounds"][-1]["resourceRemaining"] = -3
        return document

    def identity(document):
        document["algorithmVisible"]["identities"]["scenario"]["rawSha256"] = "0" * 64
        return document

    def fault(document):
        document["evaluatorAudit"]["injection"]["requestedVariant"] = "EARLY-WRQ"
        document["evaluatorAudit"]["injection"]["confirmed"] = True
        return document

    def reset(document):
        document["evaluatorAudit"]["reset"]["resetId"] = "forged-reset"
        return document

    fail(direction, "EVENT-DIRECTION-MISMATCH")
    fail(version, "HISTORY-VERSION-ORDER")
    fail(cost, "RESOURCE-RECOMPUTE-INVALID")
    fail(identity, "SCENARIO-IDENTITY-MISMATCH")
    fail(fault, "FAULT-READBACK-MISMATCH")
    fail(reset, "RESET-EVIDENCE-MISMATCH")


def test_d03_publish_success_and_mid_failure_rollback(tmp_path: Path) -> None:
    first = run_case(
        repository=ROOT, authority_commit=COMMIT, case_id=CASE_NORMAL,
        resource_mode="ROUNDS", resource_remaining=8,
    )
    output = tmp_path / "published"
    publish_run(first.document, output=output, repository=ROOT)
    original = (output / "envelope.json").read_bytes()
    second = run_case(
        repository=ROOT, authority_commit=COMMIT, case_id=CASE_EARLY_WRQ,
        resource_mode="ROUNDS", resource_remaining=8,
    )
    calls = {"count": 0}

    def boom(src: Path, dst: Path) -> None:
        calls["count"] += 1
        if ".staging-" in src.name:
            raise OSError("injected mid-publish failure")
        os.replace(src, dst)

    with pytest.raises(EngineeringError) as rejected:
        publish_run(second.document, output=output, repository=ROOT, replace_fn=boom)
    assert rejected.value.code == "EVIDENCE-PUBLISH-ERROR"
    assert (output / "envelope.json").read_bytes() == original
    first_fail = tmp_path / "fresh-fail"

    def always_fail(src: Path, dst: Path) -> None:
        raise OSError("first publication fails")

    with pytest.raises(EngineeringError):
        publish_run(first.document, output=first_fail, repository=ROOT, replace_fn=always_fail)
    assert not first_fail.exists()
    assert list(tmp_path.glob(".fresh-fail.staging-*")) == []


def test_d03_rejects_repository_escape_and_symlink_alias(tmp_path: Path) -> None:
    with pytest.raises(EngineeringError) as inside:
        safe_output_directory(ROOT / "docs" / "engineering-output", ROOT)
    assert inside.value.code == "UNSAFE-OUTPUT-PATH"
    link_parent = tmp_path / "link-parent"
    link_parent.mkdir()
    linked = tmp_path / "linked-out"
    try:
        linked.symlink_to(link_parent, target_is_directory=True)
    except OSError:
        pytest.skip("symlink creation is unavailable on this host")
    with pytest.raises(EngineeringError) as linked_error:
        safe_output_directory(linked / "evidence", ROOT)
    assert linked_error.value.code == "UNSAFE-OUTPUT-PATH"


def test_d04_missing_schema_resource_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    from cltav_615a_engineering import identity as identity_module
    from importlib import resources as resources_module

    class Empty:
        def read_bytes(self) -> bytes:
            return b""

        def joinpath(self, name: str) -> "Empty":
            return self

    monkeypatch.setattr(resources_module, "files", lambda package: Empty())
    with pytest.raises(EngineeringError) as rejected:
        identity_module.schema_bytes()
    assert rejected.value.code == "SCHEMA-RESOURCE-MISSING"


def test_d05_old_runtime_and_offline_entrypoints_remain_importable() -> None:
    assert runtime_cli.main.__name__ == "main"
    assert offline_cli.main.__name__ == "main"


def test_d04_noneditable_wheel_runs_all_four_examples(tmp_path: Path) -> None:
    wheel_dir = tmp_path / "wheel"
    wheel_dir.mkdir()
    build = subprocess.run(
        [sys.executable, "-m", "pip", "wheel", "--no-deps", "--no-build-isolation", "--wheel-dir", str(wheel_dir), str(ROOT)],
        text=True, capture_output=True,
    )
    assert build.returncode == 0, build.stderr
    wheel = next(wheel_dir.glob("*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        assert any(name.endswith("cltav_615a_engineering/cli.py") for name in names)
        assert any(name.endswith("engineering_evidence.schema.json") for name in names)
    venv = tmp_path / "clean-wheel-venv"
    create = subprocess.run([sys.executable, "-m", "venv", str(venv)], text=True, capture_output=True)
    assert create.returncode == 0, create.stderr
    binary_dir = venv / ("Scripts" if os.name == "nt" else "bin")
    python = binary_dir / ("python.exe" if os.name == "nt" else "python")
    entrypoint = binary_dir / ("cltav-615a-engineering.exe" if os.name == "nt" else "cltav-615a-engineering")
    env = {key: value for key, value in os.environ.items() if key not in {"PYTHONHOME", "PYTHONPATH"}}
    env["PYTHONNOUSERSITE"] = "1"
    env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    install = subprocess.run(
        [str(python), "-m", "pip", "install", "--no-input", str(wheel)],
        text=True, capture_output=True, env=env,
    )
    assert install.returncode == 0, install.stderr
    loaded = subprocess.run(
        [str(python), "-c", "import cltav_615a_engineering, pathlib; print(pathlib.Path(cltav_615a_engineering.__file__).resolve())"],
        cwd=tmp_path, text=True, capture_output=True, env=env,
    )
    assert loaded.returncode == 0, loaded.stderr
    loaded_path = loaded.stdout.replace("\\", "/").strip()
    assert "/site-packages/cltav_615a_engineering/" in loaded_path.replace("\\", "/")
    assert str(ROOT).replace("\\", "/").lower() not in loaded_path.lower()
    assert entrypoint.is_file()
    work = tmp_path / "unrelated"
    work.mkdir()
    for case_id in (CASE_NORMAL, CASE_EARLY_WRQ, CASE_EARLY_DATA, CASE_ACCESS_GAP):
        output = work / case_id
        ran = subprocess.run(
            [str(entrypoint), "run", "--authority-repository", str(ROOT), "--authority-commit", COMMIT,
             "--case-id", case_id, "--output", str(output)],
            cwd=work, text=True, capture_output=True, env=env,
        )
        assert ran.returncode == 0, ran.stderr
        verified = subprocess.run(
            [str(entrypoint), "verify", "--authority-repository", str(ROOT), "--authority-commit", COMMIT,
             "--evidence", str(output)],
            cwd=work, text=True, capture_output=True, env=env,
        )
        assert verified.returncode == 0, verified.stderr
