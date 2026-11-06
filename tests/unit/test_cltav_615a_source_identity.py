"""R9/R10: real loaded-source provenance, distinct from caller labels/releases."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, asdict
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from cltav_615a import FaultVariant, LurStartController, SourceIdentityError
from cltav_615a.source_identity import MODULE_FILES, SCHEME


ROOT = Path(__file__).resolve().parents[2]


def _copy_package(tmp_path: Path) -> Path:
    package = tmp_path / "src" / "cltav_615a"
    package.mkdir(parents=True)
    for filename in MODULE_FILES.values():
        shutil.copyfile(ROOT / "src/cltav_615a" / filename, package / filename)
    return package


def _run_copy(package: Path, script: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, PYTHONPATH=str(package.parent), PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run(
        [sys.executable, "-B", "-c", script], cwd=package.parent.parent,
        env=env, capture_output=True, text=True, timeout=15,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result


def test_verified_source_manifest_uses_actual_canonical_bytes_and_not_a_caller_label() -> None:
    controller = LurStartController(run_label="FAKE-UNBOUND-SOURCE")
    identity = controller.source_identity
    assert identity.scheme == SCHEME
    assert {row.path for row in identity.files} == {f"src/cltav_615a/{name}" for name in MODULE_FILES.values()}
    rows = []
    for row in identity.files:
        content = (ROOT / row.path).read_bytes().decode("utf-8").replace("\r\n", "\n").encode("utf-8")
        assert row.sha256 == sha256(content).hexdigest() and row.byte_size == len(content)
        rows.append((row.path, row.sha256, row.byte_size))
    assert identity.digest == sha256(json.dumps(rows, separators=(",", ":"), ensure_ascii=True).encode()).hexdigest()
    assert controller.implementation_identity == f"{SCHEME}:{identity.digest}"
    assert controller.run_label == "FAKE-UNBOUND-SOURCE" != controller.implementation_identity
    assert LurStartController(implementation_identity=identity.identifier).source_identity == identity
    with pytest.raises(FrozenInstanceError):
        identity.digest = "forged"
    for fake in ("", " ", "FAKE-UNBOUND-SOURCE", f"{SCHEME}:{'0' * 64}"):
        with pytest.raises(SourceIdentityError, match="^SOURCE-IDENTITY-REQUEST-MISMATCH$"):
            LurStartController(implementation_identity=fake)
    controller.record_list_submission_precondition()
    public = json.dumps(asdict(controller.public_snapshot()))
    assert controller.run_label not in public and identity.identifier not in public
    assert all(row.sha256 not in public and row.path not in public for row in identity.files)


def test_reset_install_activation_failed_attempt_and_archive_share_one_frozen_manifest() -> None:
    controller = LurStartController()
    identity = controller.source_identity
    first_reset = controller.reset_history[-1]
    installed = controller.install_fault(FaultVariant.EARLY_WRQ)
    controller.record_list_submission_precondition()
    assert controller.advance_loader().accepted
    assert controller.evaluator_audit()[-1].activation_records
    failed_reset = controller.full_reset(force_revocation_failure=True)
    old = controller.evaluator_audit()[-1]
    assert not failed_reset.success and old.final_readback.attempt_blocked
    assert old.source_identity is identity
    for record in (
        first_reset, first_reset.after, installed, failed_reset,
        controller.evaluator_fault_readback(), old, old.final_readback,
        *old.installation_records, *old.activation_records,
    ):
        assert record.code_identity == identity.identifier
    assert controller.full_reset().success
    assert controller.evaluator_audit()[0] == old
    assert controller.evaluator_audit()[-1].source_identity is identity
    assert controller.evaluator_audit()[-1].attempt_id != old.attempt_id
    assert controller.reset_history[0] == first_reset
    assert all(reset.code_identity == identity.identifier for reset in controller.reset_history)


@pytest.mark.parametrize("change,diagnostic", (
    ("drift", "SOURCE-IDENTITY-SOURCE-DRIFT"),
    ("missing", "SOURCE-IDENTITY-UNSAFE-OR-MISSING-FILE"),
))
def test_imported_code_cannot_be_relabelled_with_changed_or_missing_disk_source(
    tmp_path: Path, change: str, diagnostic: str,
) -> None:
    package = _copy_package(tmp_path)
    result = _run_copy(package, f'''
from pathlib import Path
import cltav_615a
from cltav_615a import LurStartController, SourceIdentityError
root = Path(cltav_615a.__file__).resolve().parent
assert root == Path("src/cltav_615a").resolve()
before = LurStartController().source_identity
target = root / "objects.py"
if {change!r} == "missing":
    target.unlink()
else:
    target.write_bytes(target.read_bytes() + b"\\n# changed after import\\n")
try:
    LurStartController()
except SourceIdentityError as exc:
    assert str(exc) == {diagnostic!r}
    print(str(exc))
else:
    raise AssertionError("accepted stale code under altered source binding")
''')
    assert result.stdout.strip() == diagnostic


def test_fresh_source_changes_change_identity_but_lf_crlf_do_not(tmp_path: Path) -> None:
    package = _copy_package(tmp_path)
    script = "from cltav_615a import LurStartController; print(LurStartController().implementation_identity)"
    original = _run_copy(package, script).stdout.strip()
    for source in package.glob("*.py"):
        source.write_bytes(source.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    assert _run_copy(package, script).stdout.strip() == original
    source = package / "objects.py"
    source.write_bytes(source.read_bytes() + b"\r\n# source revision, same bounded behavior\r\n")
    changed = _run_copy(package, script).stdout.strip()
    assert changed.startswith(SCHEME + ":") and changed != original


def test_stale_bytecode_cannot_pass_source_code_equality_check(tmp_path: Path) -> None:
    package = _copy_package(tmp_path)
    result = _run_copy(package, '''
from pathlib import Path
import os
import py_compile
target = Path("src/cltav_615a/objects.py").resolve()
raw = target.read_bytes()
changed = raw.replace(b'"WRQ-EMITTED"', b'"BAD-EMITTED"')
assert raw != changed and len(raw) == len(changed)
py_compile.compile(str(target), doraise=True)
stamp = target.stat()
target.write_bytes(changed)
os.utime(target, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))
try:
    from cltav_615a import LurStartController
except ValueError as exc:
    assert str(exc) == "SOURCE-IDENTITY-LOADED-CODE-MISMATCH"
    print(str(exc))
else:
    raise AssertionError("accepted stale module code as current source")
''')
    assert result.stdout.strip() == "SOURCE-IDENTITY-LOADED-CODE-MISMATCH"
