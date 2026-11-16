"""D-stage 615A engineering delivery: envelope, CLI, transactions, wheel."""

from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

import pytest

from cltav_615a_engineering.cli import main as engineering_main
from cltav_615a_engineering.envelope import compute_fingerprint, validate_envelope
from cltav_615a_engineering.errors import EngineeringError
from cltav_615a_engineering.jsonutil import canonical_json_bytes
from cltav_615a_engineering.publish import publish_run, safe_output_directory
from cltav_615a_engineering.verify import verify_evidence_directory
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


def test_d01_seven_probe_tampers_fail_after_fingerprint_refresh(tmp_path: Path) -> None:
    """Persistent negatives for the seven RR-009 synergistic tamper classes."""

    base = tmp_path / "ENG-CASE-NORMAL"
    assert engineering_main(["run", *_authority(), "--case-id", CASE_NORMAL, "--output", str(base)]) == 0

    def apply_tamper(label: str, fn, refresh: bool = True) -> Path:
        target = tmp_path / f"t-{label}"
        shutil.copytree(base, target)
        env = json.loads((target / "envelope.json").read_text(encoding="utf-8"))
        fn(env, target)
        if refresh:
            env["algorithmVisible"]["fingerprintSha256"] = compute_fingerprint(env["algorithmVisible"])
        (target / "envelope.json").write_bytes(canonical_json_bytes(env))
        return target

    def cost(env, d):
        r = env["algorithmVisible"]["rounds"][0]
        r["detailCharges"] = {k: 0 for k in r["detailCharges"]} or {"acquisition": 0}
        r["projectedCost"] = {k: 0 for k in r["projectedCost"]}
        for x in env["algorithmVisible"]["rounds"]:
            x["resourceRemaining"] = 8

    def hyp(env, d):
        env["algorithmVisible"]["stop"]["hypotheses"] = ["EARLY-DATA"]
        for x in env["algorithmVisible"]["rounds"]:
            x["hypotheses"] = ["EARLY-DATA"]

    def action(env, d):
        env["algorithmVisible"]["rounds"][-1]["actionId"] = "ACT-RECOVER-RECONFIRM-READY"

    def runtime_id(env, d):
        env["algorithmVisible"]["identities"]["implementation"]["runtimeSession"]["sha256"] = "0" * 64

    def drop_event(env, d):
        env["algorithmVisible"]["journal"]["events"].pop()

    def split_file(env, d):
        (d / "algorithm-visible" / "rounds.json").write_text("[]", encoding="utf-8")

    def reset_both(env, d):
        env["evaluatorAudit"]["reset"]["resetId"] = "forged"
        for e in env["algorithmVisible"]["journal"]["events"]:
            e["resetId"] = "forged"
        env["algorithmVisible"]["journal"]["resetId"] = "forged"

    expected = {
        "cost": "RESOURCE-RECOMPUTE-MISMATCH",
        "hypotheses": "HYPOTHESIS-STOP-MISMATCH",
        "action": "ACTION-KIND-MISMATCH",
        "runtime-identity": "IMPLEMENTATION-IDENTITY-MISMATCH",
        "drop-event": "REPLAY-JOURNAL-MISMATCH",
        "split-file-only": "EVIDENCE-SPLIT-MISMATCH",
        "reset-coordinated": "RESET-IDENTITY-INCONSISTENT",
    }
    for label, fn in (
        ("cost", cost),
        ("hypotheses", hyp),
        ("action", action),
        ("runtime-identity", runtime_id),
        ("drop-event", drop_event),
        ("split-file-only", split_file),
        ("reset-coordinated", reset_both),
    ):
        path = apply_tamper(label, fn)
        with pytest.raises(EngineeringError) as rejected:
            verify_evidence_directory(path, repository=ROOT, authority_commit=COMMIT)
        assert rejected.value.code == expected[label], (label, rejected.value.code)
        assert engineering_main(["verify", *_authority(), "--evidence", str(path)]) == 1


def test_d01_rr010_journal_and_evaluator_tampers_fail(tmp_path: Path) -> None:
    """RR-010: tick/actor journal fields and EARLY-WRQ truth relabel must fail verify."""

    split_visible = {
        "identities": "identities.json",
        "configuration": "configuration.json",
        "journal": "journal.json",
        "rounds": "rounds.json",
        "stop": "stop.json",
    }

    def sync_split(target: Path, env: dict) -> None:
        env["algorithmVisible"]["fingerprintSha256"] = compute_fingerprint(env["algorithmVisible"])
        (target / "envelope.json").write_bytes(canonical_json_bytes(env))
        visible = env["algorithmVisible"]
        for key, name in split_visible.items():
            (target / "algorithm-visible" / name).write_bytes(canonical_json_bytes(visible[key]))
        (target / "algorithm-visible" / "fingerprint.json").write_bytes(
            canonical_json_bytes({"fingerprintSha256": visible["fingerprintSha256"]})
        )
        audit = env["evaluatorAudit"]
        for key, name in (("faultPlan", "fault.json"), ("reset", "reset.json"), ("injection", "injection.json")):
            (target / "evaluator-audit" / name).write_bytes(canonical_json_bytes(audit[key]))

    normal = tmp_path / CASE_NORMAL
    early = tmp_path / CASE_EARLY_WRQ
    assert engineering_main(["run", *_authority(), "--case-id", CASE_NORMAL, "--output", str(normal)]) == 0
    assert engineering_main(["run", *_authority(), "--case-id", CASE_EARLY_WRQ, "--output", str(early)]) == 0

    def tick_all(env, _d):
        for event in env["algorithmVisible"]["journal"]["events"]:
            event["tick"] = event["tick"] + 1

    def tick_one(env, _d):
        env["algorithmVisible"]["journal"]["events"][0]["tick"] = env["algorithmVisible"]["journal"]["events"][0]["tick"] + 1

    def actor(env, _d):
        env["algorithmVisible"]["journal"]["events"][0]["actor"] = "FORGED-ACTOR"

    def relabel(env, _d):
        env["evaluatorAudit"]["injection"]["requestedVariant"] = "NORMAL"
        env["evaluatorAudit"]["injection"]["confirmed"] = False
        env["evaluatorAudit"]["faultPlan"]["requestedVariant"] = "NORMAL"

    expected = {
        "tick-shift": (normal, tick_all, "REPLAY-JOURNAL-MISMATCH"),
        "tick-one": (normal, tick_one, "REPLAY-JOURNAL-MISMATCH"),
        "actor": (normal, actor, "REPLAY-JOURNAL-MISMATCH"),
        "truth-relabel-earlywrq": (early, relabel, "INJECTION-CASE-MISMATCH"),
    }
    for label, (base, fn, code) in expected.items():
        target = tmp_path / f"t-{label}"
        shutil.copytree(base, target)
        env = json.loads((target / "envelope.json").read_text(encoding="utf-8"))
        fn(env, target)
        sync_split(target, env)
        with pytest.raises(EngineeringError) as rejected:
            verify_evidence_directory(target, repository=ROOT, authority_commit=COMMIT)
        assert rejected.value.code == code, (label, rejected.value.code)
        assert engineering_main(["verify", *_authority(), "--evidence", str(target)]) == 1


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
        replayed = subprocess.run(
            [str(entrypoint), "replay", "--authority-repository", str(ROOT), "--authority-commit", COMMIT,
             "--evidence", str(output)],
            cwd=work, text=True, capture_output=True, env=env,
        )
        assert replayed.returncode == 0, replayed.stderr
