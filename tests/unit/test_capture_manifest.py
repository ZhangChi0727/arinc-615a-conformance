import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("audit_capture_manifest", ROOT / "scripts" / "audit_capture_manifest.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
audit_errors = MODULE.audit_errors
MANIFEST = json.loads((ROOT / "configs/research/cltav_historical_capture_manifest.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((ROOT / "configs/research/cltav_historical_capture_manifest.schema.json").read_text(encoding="utf-8"))


def _corpus(tmp_path: Path) -> Path:
    root = tmp_path / "captures"
    root.mkdir()
    (root / "one.pcapng").write_bytes(b"one")
    (root / "two.pcapng").write_bytes(b"two")
    return root


def _manifest(root: Path) -> dict:
    import hashlib
    rows = []
    for number, path in enumerate(sorted(root.iterdir()), 1):
        rows.append({"captureId": f"HC-{number:02}", "relativePath": path.name, "byteCount": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "observationQuality": "UNASSESSED-EXPLORATORY", "labelSource": "FILE-ANNOTATION-NONTRUTH", "rootCause": "UNKNOWN"})
    return {"manifestId": "CLTAV-HISTORICAL-CAPTURES", "manifestVersion": "1.0", "purpose": "EXPLORATORY-DEVELOPMENT-ONLY", "captureCount": len(rows), "truthBoundary": "not truth", "captures": rows}


def test_schema_is_enforced_before_filesystem_audit(tmp_path):
    data = _manifest(_corpus(tmp_path))
    data["purpose"] = "CONFIRMATORY"
    assert any(error.startswith("schema:") for error in audit_errors(data, tmp_path / "missing", SCHEMA))


def test_rejects_windows_absolute_and_escaping_paths(tmp_path):
    data = _manifest(_corpus(tmp_path))
    data["captures"][0]["relativePath"] = f"{chr(67)}:{'/'}outside.pcapng"
    assert any("unsafe" in error for error in audit_errors(data, tmp_path / "captures", SCHEMA))


def test_rejects_duplicate_path_and_omitted_corpus_file(tmp_path):
    data = _manifest(_corpus(tmp_path))
    data["captures"][1]["relativePath"] = data["captures"][0]["relativePath"]
    assert any("repeated" in error for error in audit_errors(data, tmp_path / "captures", SCHEMA))
    omitted = _manifest(tmp_path / "captures")
    omitted["captures"].pop()
    omitted["captureCount"] -= 1
    assert any("omits corpus" in error for error in audit_errors(omitted, tmp_path / "captures", SCHEMA))


def test_rejects_two_aliases_for_one_resolved_file(tmp_path):
    root = _corpus(tmp_path)
    alias = root / "alias.pcapng"
    try:
        alias.hardlink_to(root / "one.pcapng")
    except OSError:
        import pytest
        pytest.skip("filesystem does not support hard links")
    data = _manifest(root)
    assert any("resolved file identity is repeated" in error for error in audit_errors(data, root, SCHEMA))


def test_valid_manifest_is_accepted(tmp_path):
    root = _corpus(tmp_path)
    assert audit_errors(_manifest(root), root, SCHEMA) == []
