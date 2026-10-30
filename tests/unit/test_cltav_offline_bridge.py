"""G4 production-boundary tests for the limited offline replay bridge.

Positive fixtures always flow through the real PR22 ``cltav-offline inspect``
producer.  A hand-written bridge-shaped dictionary is never a bridge oracle.
"""

from __future__ import annotations

import json
import os
import socket
import struct
import subprocess
import sys
import zipfile
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

import pytest

from cltav_offline import bridge as bridge_module
from cltav_offline.bridge import (
    OfflineReplayError,
    adapt_offline_evidence_bytes,
    canonical_json_bytes,
    offline_replay_document,
    publish_offline_replay,
    validate_offline_replay_bytes,
)
from cltav_offline.cli import main as offline_main
from cltav_runtime.interpretation import replay_ownership as runtime_replay_ownership
from cltav_runtime.session import ReferenceSession


def _ethernet_ipv4(
    payload: bytes,
    *,
    source: str = "10.0.0.1",
    destination: str = "10.0.0.2",
    identification: int = 1,
    offset_bytes: int = 0,
    more_fragments: bool = False,
) -> bytes:
    assert offset_bytes % 8 == 0
    flags_offset = (0x2000 if more_fragments else 0) | (offset_bytes // 8)
    ipv4 = struct.pack(
        "!BBHHHBBH4s4s",
        0x45, 0, 20 + len(payload), identification, flags_offset, 64, 17, 0,
        socket.inet_aton(source), socket.inet_aton(destination),
    ) + payload
    return b"\xaa" * 6 + b"\xbb" * 6 + struct.pack("!H", 0x0800) + ipv4


def _udp(source_port: int, destination_port: int, payload: bytes) -> bytes:
    return struct.pack("!HHHH", source_port, destination_port, 8 + len(payload), 0) + payload


def _request(opcode: int, filename: str) -> bytes:
    return struct.pack("!H", opcode) + filename.encode("ascii") + b"\0octet\0"


def _data(block: int, payload: bytes) -> bytes:
    return struct.pack("!HH", 3, block) + payload


def _ack(block: int) -> bytes:
    return struct.pack("!HH", 4, block)


def _pcap(records: list[bytes]) -> bytes:
    result = b"\xd4\xc3\xb2\xa1" + struct.pack("<HHIIII", 2, 4, 0, 0, 65535, 1)
    for index, record in enumerate(records, 1):
        result += struct.pack("<IIII", 1, index, len(record), len(record)) + record
    return result


def _lui_header(*, declared_length: int = 9) -> bytes:
    return declared_length.to_bytes(4, "big") + b"A1" + b"\0\0" + b"\0"


def _complete_exchange(filename: str = "load.lui") -> list[bytes]:
    return [
        _ethernet_ipv4(_udp(10000, 69, _request(1, filename)), identification=10),
        _ethernet_ipv4(
            _udp(40000, 10000, _data(1, _lui_header())),
            source="10.0.0.2", destination="10.0.0.1", identification=11,
        ),
        _ethernet_ipv4(_udp(10000, 40000, _ack(1)), identification=12),
    ]


def _produce_evidence(
    tmp_path: Path,
    *,
    name: str,
    capture_id: str,
    records: list[bytes],
    expected_exit: int = 0,
) -> tuple[Path, Path, bytes]:
    """Use the actual production CLI producer, not a fixture dictionary."""

    capture = tmp_path / f"{name}.pcap"
    evidence = tmp_path / f"{name}.intake.json"
    capture.write_bytes(_pcap(records))
    assert offline_main([
        "inspect", "--input", str(capture), "--capture-id", capture_id,
        "--output", str(evidence), "--source-commit", "a" * 40,
    ]) == expected_exit
    return capture, evidence, evidence.read_bytes()


def _assert_non_scoring(document: dict[str, object]) -> None:
    assert document["mode"] == "OFFLINE-REPLAY"
    assert document["boundary"] == {
        "purpose": "EXPLORATORY-DEVELOPMENT-ONLY",
        "statement": (
            "This is a passive, non-scoring structural replay of bounded offline intake evidence. "
            "It does not issue an action, charge a cost, reset a session, update history, "
            "claim a protocol verdict, or attribute an IUT failure."
        ),
        "conformanceVerdict": "NOT-EVALUATED",
        "integrity": "NOT-EVALUATED",
    }
    assert document["activeExecution"] == {
        "issuedActionCount": 0,
        "chargedCost": 0,
        "attemptCount": 0,
        "resetApplied": False,
        "historyUpdated": False,
        "activeFeedbackApplied": False,
    }
    records = document["records"]
    assert isinstance(records, list) and records
    assert all(record["scoring"]["disposition"] == "NOT-SCORED" for record in records)
    assert all(record["scoring"]["protocolVerdict"] == "NOT-EVALUATED" for record in records)
    assert all("measurementInterval" not in record and "deadline" not in record for record in records)
    rendered = json.dumps(document, sort_keys=True)
    assert '"PASS"' not in rendered
    assert '"FAIL"' not in rendered
    assert "IUT-FINDING" not in rendered


def test_real_decoder_projection_reaches_only_public_structural_ownership_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """BR01/BR05: PR22 output is rebuilt before non-scoring ownership replay."""

    capture, evidence_path, evidence_raw = _produce_evidence(
        tmp_path, name="complete", capture_id="cap-g4-complete", records=_complete_exchange(),
    )
    calls: list[tuple[object, object]] = []

    def record_public_replay(events: object, contract: object, **kwargs: object) -> object:
        calls.append((events, contract))
        return runtime_replay_ownership(events, contract, **kwargs)

    def no_active_step(*args: object, **kwargs: object) -> object:
        raise AssertionError("offline replay must not start a ReferenceSession execution")

    monkeypatch.setattr(bridge_module, "replay_ownership", record_public_replay)
    monkeypatch.setattr(ReferenceSession, "step", no_active_step)
    bridge_path = tmp_path / "complete.bridge.json"
    assert offline_main([
        "replay", "--input", str(capture), "--offline-evidence", str(evidence_path), "--output", str(bridge_path),
    ]) == 0
    assert calls, "bridge did not use the public ownership replay component"
    assert offline_main([
        "validate-replay", "--input", str(capture), "--offline-evidence", str(evidence_path), "--bridge", str(bridge_path),
    ]) == 0

    source = json.loads(evidence_raw)
    document = json.loads(bridge_path.read_bytes())
    _assert_non_scoring(document)
    assert document["source"]["captureIdentity"] == {
        key: source["input"][key] for key in ("captureId", "byteCount", "sha256")
    }
    assert document["source"]["tool"] == source["tool"]
    assert document["source"]["contractProjectionIdentity"] == source["contractProjection"]["contractIdentity"]
    assert document["offlineEvidence"] == source
    record = document["records"][0]
    assert record["sourceRefs"]["requestProjectionId"].startswith("event-request-")
    assert record["sourceRefs"]["packetRefIds"]
    assert record["sourceRefs"]["datagramIds"]
    assert record["sourceRefs"]["eventIds"]
    assert record["ownershipReplay"]["qualified"] is False
    assert record["scoring"]["reason"] == "OFFLINE-CLOCK-ACCURACY-UNKNOWN"
    assert record["clock"]["accuracy"] == "UNKNOWN"


@pytest.mark.parametrize(
    ("name", "capture_id", "records", "expected_reason"),
    [
        (
            "gapped",
            "cap-g4-gapped",
            [
                _ethernet_ipv4(
                    _udp(10001, 69, _request(1, "fragment.lui"))[:16],
                    identification=31, more_fragments=True,
                ),
            ],
            "OFFLINE-DATAGRAM-QUALITY-GAPPED",
        ),
        (
            "conflict",
            "cap-g4-conflict",
            [
                _ethernet_ipv4(b"abcdefghijklmnop", identification=32, more_fragments=True),
                _ethernet_ipv4(b"abcdefghijklmnoX", identification=32, more_fragments=True),
            ],
            "OFFLINE-DATAGRAM-QUALITY-CONFLICT",
        ),
        (
            "partial",
            "cap-g4-partial",
            [
                _ethernet_ipv4(_udp(10002, 69, _request(1, "partial.lui")), identification=33),
                _ethernet_ipv4(
                    _udp(40002, 10002, _data(1, _lui_header(declared_length=1000))),
                    source="10.0.0.2", destination="10.0.0.1", identification=34,
                ),
            ],
            "OFFLINE-PARSE-QUALITY-NOT-PARSED",
        ),
    ],
)
def test_quality_states_are_preserved_without_promoting_to_a_verdict(
    tmp_path: Path,
    name: str,
    capture_id: str,
    records: list[bytes],
    expected_reason: str,
) -> None:
    """BR02: incomplete, conflict and partial quality never become a verdict."""

    capture, evidence_path, evidence_raw = _produce_evidence(
        tmp_path, name=name, capture_id=capture_id, records=records, expected_exit=2,
    )
    run = adapt_offline_evidence_bytes(evidence_raw, capture_path=capture, evidence_path=evidence_path)
    document = offline_replay_document(run)
    _assert_non_scoring(document)
    assert any(record["scoring"]["reason"] == expected_reason for record in document["records"])
    bridge_path = tmp_path / f"{name}.bridge.json"
    publish_offline_replay(run, output=bridge_path)
    assert validate_offline_replay_bytes(
        bridge_path.read_bytes(), capture_path=capture, offline_evidence_raw=evidence_raw, evidence_path=evidence_path,
    ) == document


def test_nonprojectable_pr22_transfer_is_retained_as_source_limited_not_scored_evidence(tmp_path: Path) -> None:
    """A valid old capture identity need not satisfy the new projection ID profile.

    The PR22 producer explicitly records the limitation in ``nonProjectable``.
    G4 must retain that lineage as a named bridge limit rather than inventing
    a request for the ownership component or rejecting valid passive evidence.
    """

    capture, evidence_path, evidence_raw = _produce_evidence(
        tmp_path, name="old-id", capture_id="SYN-01", records=_complete_exchange(),
    )
    source = json.loads(evidence_raw)
    assert source["contractProjection"]["nonProjectable"]
    run = adapt_offline_evidence_bytes(evidence_raw, capture_path=capture, evidence_path=evidence_path)
    document = offline_replay_document(run)
    _assert_non_scoring(document)
    record = document["records"][0]
    assert record["scoring"]["reason"] == "OFFLINE-REQUEST-PROJECTION-UNAVAILABLE"
    assert "ownershipReplay" not in record
    transfer_id = source["transfers"][0]["transferId"]
    assert record["quality"]["nonProjectable"] == [
        item for item in source["contractProjection"]["nonProjectable"] if item["sourceId"] == transfer_id
    ]


def test_bridge_rejects_tampered_producer_chain_without_overwriting_owned_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """BR03/BR06: source identity, version and ancestry failures are named and safe."""

    capture, evidence_path, evidence_raw = _produce_evidence(
        tmp_path, name="source", capture_id="cap-g4-source", records=_complete_exchange(),
    )
    run = adapt_offline_evidence_bytes(evidence_raw, capture_path=capture, evidence_path=evidence_path)
    protected = tmp_path / "protected.bridge.json"
    publish_offline_replay(run, output=protected)
    old = protected.read_bytes()

    mutated = json.loads(evidence_raw)
    mutated["schemaVersion"] = "99.0"
    invalid_evidence = tmp_path / "wrong-version.json"
    invalid_evidence.write_bytes(canonical_json_bytes(mutated))
    assert offline_main([
        "replay", "--input", str(capture), "--offline-evidence", str(invalid_evidence), "--output", str(protected),
    ]) == 1
    assert "OFFLINE-EVIDENCE-VERSION-ERROR" in capsys.readouterr().err
    assert protected.read_bytes() == old

    bad_witness = json.loads(evidence_raw)
    bad_witness["transfers"][0]["sourceWitness"]["requestPacketRefId"] = "pkt-not-present"
    with pytest.raises(OfflineReplayError) as caught:
        adapt_offline_evidence_bytes(canonical_json_bytes(bad_witness), capture_path=capture)
    assert caught.value.code == "OFFLINE-EVIDENCE-INVALID"

    other_capture = tmp_path / "other.pcap"
    other_capture.write_bytes(_pcap(_complete_exchange("other.lui")))
    with pytest.raises(OfflineReplayError) as mismatched:
        adapt_offline_evidence_bytes(evidence_raw, capture_path=other_capture)
    assert mismatched.value.code in {"OFFLINE-SOURCE-MISMATCH", "OFFLINE-SOURCE-REBUILD-ERROR"}

    duplicate_event = json.loads(evidence_raw)
    duplicate_event["events"].append(deepcopy(duplicate_event["events"][0]))
    duplicate_event["counts"]["events"] += 1
    with pytest.raises(OfflineReplayError) as repeated:
        adapt_offline_evidence_bytes(canonical_json_bytes(duplicate_event), capture_path=capture)
    assert repeated.value.code == "OFFLINE-EVIDENCE-INVALID"


@pytest.mark.parametrize("mutation", ["wrong-key", "invented-cancel", "cross-domain"])
def test_unproven_ownership_or_termination_facts_cannot_create_an_offline_verdict(
    tmp_path: Path,
    mutation: str,
) -> None:
    """BR04: passive source drift is rejected before any ownership conclusion."""

    capture, evidence_path, evidence_raw = _produce_evidence(
        tmp_path, name=mutation, capture_id=f"cap-g4-{mutation}", records=_complete_exchange(),
    )
    source = json.loads(evidence_raw)
    if mutation == "wrong-key":
        request = next(
            item for item in source["contractProjection"]["records"]
            if item["sourceId"].startswith("event-request-")
        )
        request["payload"]["correlationKey"] = "corr-not-from-source"
    elif mutation == "invented-cancel":
        invented = deepcopy(source["events"][0])
        invented["eventId"] = "event-invented-cancel"
        invented["eventType"] = "CANCEL"
        invented["layer"] = "WIRE"
        source["events"].append(invented)
        source["counts"]["events"] += 1
    else:
        # The PR22 transfer reconstructor will not associate across domains.
        # A hand-edited domain is therefore source drift, not permission to
        # compute a cross-domain timing delta in the bridge.
        source["packetRefs"][-1]["timestamp"]["clockDomain"] = "FOREIGN-UNPROVEN-DOMAIN"
    mutated_raw = canonical_json_bytes(source)
    # Keep the declared evidence file aligned with the caller-supplied bytes:
    # this test exercises source/projection drift, while the separate evidence
    # drift test exercises file-versus-byte identity rejection.
    evidence_path.write_bytes(mutated_raw)
    with pytest.raises(OfflineReplayError) as rejected:
        adapt_offline_evidence_bytes(
            mutated_raw, capture_path=capture, evidence_path=evidence_path,
        )
    assert rejected.value.code in {"OFFLINE-EVIDENCE-INVALID", "OFFLINE-SOURCE-MISMATCH"}


def test_bridge_publishing_is_atomic_for_validation_and_replacement_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """BR06: failed staging/swap cannot replace a prior owned artifact."""

    capture_one, evidence_one, raw_one = _produce_evidence(
        tmp_path, name="first", capture_id="cap-g4-first", records=_complete_exchange("first.lui"),
    )
    first = adapt_offline_evidence_bytes(raw_one, capture_path=capture_one, evidence_path=evidence_one)
    target = tmp_path / "transaction.bridge.json"
    first_document = publish_offline_replay(first, output=target)
    old = target.read_bytes()

    real_document = bridge_module.offline_replay_document
    rendered = 0

    def stale_relation(run: object) -> dict[str, object]:
        nonlocal rendered
        rendered += 1
        forged = real_document(run)
        if rendered != 1:
            return forged
        forged["records"][0]["sourceRefs"]["requestProjectionId"] = "forged-after-stage"
        payload = {key: value for key, value in forged.items() if key != "integrity"}
        forged["integrity"] = {"canonicalPayloadSha256": sha256(canonical_json_bytes(payload)).hexdigest()}
        return forged

    # The forged artifact has a coherent self-hash. Only the actual staged
    # source-rebuild relation check can stop it before the existing output is
    # moved aside.
    with monkeypatch.context() as staged:
        staged.setattr(bridge_module, "offline_replay_document", stale_relation)
        with pytest.raises(OfflineReplayError) as stage_error:
            publish_offline_replay(first, output=target)
    assert stage_error.value.code == "OFFLINE-BRIDGE-RELATION-MISMATCH"
    assert target.read_bytes() == old

    def fail_new_swap(source: Path, destination: Path) -> None:
        if destination == target and source.name.startswith(f".{target.name}.staging-"):
            raise OSError("deliberate replacement failure")
        os.replace(source, destination)

    with pytest.raises(OfflineReplayError) as replacement_error:
        publish_offline_replay(first, output=target, replace_fn=fail_new_swap)
    assert replacement_error.value.code == "OFFLINE-BRIDGE-PUBLISH-ERROR"
    assert target.read_bytes() == old

    first_failure = tmp_path / "first-failure.bridge.json"
    with pytest.raises(OfflineReplayError):
        publish_offline_replay(
            first,
            output=first_failure,
            replace_fn=lambda _source, _destination: (_ for _ in ()).throw(OSError("deliberate first failure")),
        )
    assert not first_failure.exists()
    assert not list(tmp_path.glob(".first-failure.bridge.json.*"))

    published = publish_offline_replay(first, output=target)
    assert published == first_document
    assert target.read_bytes() == old
    assert validate_offline_replay_bytes(
        target.read_bytes(), capture_path=capture_one, offline_evidence_raw=raw_one, evidence_path=evidence_one,
    ) == published


def test_bridge_rechecks_the_capture_bytes_before_replacing_an_existing_artifact(tmp_path: Path) -> None:
    """The adapter's earlier input check is not reused as a stale publish authority."""

    capture, evidence, raw = _produce_evidence(
        tmp_path, name="source-drift", capture_id="cap-g4-source-drift", records=_complete_exchange(),
    )
    run = adapt_offline_evidence_bytes(raw, capture_path=capture, evidence_path=evidence)
    target = tmp_path / "source-drift.bridge.json"
    publish_offline_replay(run, output=target)
    old = target.read_bytes()
    capture.write_bytes(_pcap(_complete_exchange("changed-after-adapt.lui")))
    with pytest.raises(OfflineReplayError) as changed:
        publish_offline_replay(run, output=target)
    assert changed.value.code == "OFFLINE-SOURCE-MISMATCH"
    assert target.read_bytes() == old


def test_bridge_rechecks_the_declared_evidence_bytes_before_replacing_an_existing_artifact(tmp_path: Path) -> None:
    """The on-disk evidence identity remains authoritative through publication."""

    capture, evidence, raw = _produce_evidence(
        tmp_path, name="evidence-drift", capture_id="cap-g4-evidence-drift", records=_complete_exchange(),
    )
    run = adapt_offline_evidence_bytes(raw, capture_path=capture, evidence_path=evidence)
    target = tmp_path / "evidence-drift.bridge.json"
    publish_offline_replay(run, output=target)
    old = target.read_bytes()
    evidence.write_bytes(raw + b"\n")
    with pytest.raises(OfflineReplayError) as changed:
        publish_offline_replay(run, output=target)
    assert changed.value.code == "OFFLINE-EVIDENCE-IDENTITY-MISMATCH"
    assert target.read_bytes() == old


def test_bridge_preserves_the_prior_backup_when_rollback_itself_cannot_complete(tmp_path: Path) -> None:
    """A double replacement fault must retain, rather than silently delete, old bytes."""

    capture, evidence, raw = _produce_evidence(
        tmp_path, name="rollback", capture_id="cap-g4-rollback", records=_complete_exchange(),
    )
    run = adapt_offline_evidence_bytes(raw, capture_path=capture, evidence_path=evidence)
    target = tmp_path / "rollback.bridge.json"
    publish_offline_replay(run, output=target)
    old = target.read_bytes()
    calls = 0

    def fail_forward_and_restore(source: Path, destination: Path) -> None:
        nonlocal calls
        calls += 1
        if calls >= 2:
            raise OSError("deliberate forward and rollback failure")
        os.replace(source, destination)

    with pytest.raises(OfflineReplayError) as failed:
        publish_offline_replay(run, output=target, replace_fn=fail_forward_and_restore)
    assert failed.value.code == "OFFLINE-BRIDGE-ROLLBACK-ERROR"
    backups = list(tmp_path.glob(".rollback.bridge.json.backup-*"))
    assert not target.exists()
    assert len(backups) == 1
    assert backups[0].read_bytes() == old


def test_bridge_rejects_input_output_overlap_and_noncanonical_numeric_values(tmp_path: Path) -> None:
    """Bridge output cannot overwrite sources and rejects lossy JSON values."""

    capture, evidence_path, evidence_raw = _produce_evidence(
        tmp_path, name="overlap", capture_id="cap-g4-overlap", records=_complete_exchange(),
    )
    run = adapt_offline_evidence_bytes(evidence_raw, capture_path=capture, evidence_path=evidence_path)
    with pytest.raises(OfflineReplayError) as capture_overlap:
        publish_offline_replay(run, output=capture)
    assert capture_overlap.value.code == "OFFLINE-BRIDGE-OUTPUT-PATH-ERROR"
    with pytest.raises(OfflineReplayError) as evidence_overlap:
        publish_offline_replay(run, output=evidence_path)
    assert evidence_overlap.value.code == "OFFLINE-BRIDGE-OUTPUT-PATH-ERROR"

    user_material = tmp_path / "user-material.json"
    user_material.write_text("do not replace", encoding="utf-8")
    with pytest.raises(OfflineReplayError) as unowned:
        publish_offline_replay(run, output=user_material)
    assert unowned.value.code == "OFFLINE-BRIDGE-OUTPUT-PATH-ERROR"
    assert user_material.read_text(encoding="utf-8") == "do not replace"

    bridge = offline_replay_document(run)
    bridge["records"][0]["clock"]["ticksPerSecond"] = 1.5
    raw = canonical_json_bytes(bridge)
    with pytest.raises(OfflineReplayError) as floating:
        validate_offline_replay_bytes(raw, capture_path=capture, offline_evidence_raw=evidence_raw)
    assert floating.value.code == "OFFLINE-BRIDGE-SHAPE-ERROR"


def test_bridge_rejects_symbolic_link_inputs_before_reading_or_publishing(tmp_path: Path) -> None:
    """A leaf alias cannot redirect bridge input or evade output-overlap checks."""

    capture, evidence_path, evidence_raw = _produce_evidence(
        tmp_path, name="link", capture_id="cap-g4-link", records=_complete_exchange(),
    )
    linked_capture = tmp_path / "capture-link.pcap"
    linked_evidence = tmp_path / "evidence-link.json"
    try:
        os.symlink(capture, linked_capture)
        os.symlink(evidence_path, linked_evidence)
    except OSError:
        pytest.skip("symbolic links are unavailable in this local test environment")
    with pytest.raises(OfflineReplayError) as capture_error:
        adapt_offline_evidence_bytes(evidence_raw, capture_path=linked_capture)
    assert capture_error.value.code == "OFFLINE-CAPTURE-READ-ERROR"
    with pytest.raises(OfflineReplayError) as evidence_error:
        adapt_offline_evidence_bytes(evidence_raw, capture_path=capture, evidence_path=linked_evidence)
    assert evidence_error.value.code == "OFFLINE-EVIDENCE-READ-ERROR"


def test_installed_wheel_runs_real_offline_replay_without_network_or_source_import(tmp_path: Path) -> None:
    """BR06: the non-editable command works outside the checkout and stays passive."""

    root = Path(__file__).resolve().parents[2]
    wheel_dir = tmp_path / "wheel"
    wheel_dir.mkdir()
    build = subprocess.run(
        [
            sys.executable, "-m", "pip", "wheel", "--no-deps", "--no-build-isolation",
            "--wheel-dir", str(wheel_dir), str(root),
        ],
        text=True,
        capture_output=True,
    )
    assert build.returncode == 0, build.stderr
    wheel = next(wheel_dir.glob("*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        assert "cltav_offline/bridge.py" in archive.namelist()
        assert "cltav_offline/cli.py" in archive.namelist()

    venv = tmp_path / "wheel-venv"
    create = subprocess.run(
        [sys.executable, "-m", "venv", str(venv)],
        text=True,
        capture_output=True,
    )
    assert create.returncode == 0, create.stderr
    binary_dir = venv / ("Scripts" if os.name == "nt" else "bin")
    python = binary_dir / ("python.exe" if os.name == "nt" else "python")
    entrypoint = binary_dir / ("cltav-offline.exe" if os.name == "nt" else "cltav-offline")
    clean_environment = {
        key: value
        for key, value in os.environ.items()
        if key not in {"PYTHONHOME", "PYTHONPATH"}
    }
    clean_environment["PYTHONNOUSERSITE"] = "1"
    clean_environment["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    # Install declared runtime dependencies into this plain venv.  Do not
    # inherit the developer environment merely because jsonschema happens to
    # be available to the test runner.
    install = subprocess.run(
        [str(python), "-m", "pip", "install", "--no-input", str(wheel)],
        text=True,
        capture_output=True,
        env=clean_environment,
    )
    assert install.returncode == 0, install.stderr
    dependency_check = subprocess.run(
        [str(python), "-m", "pip", "check"],
        text=True,
        capture_output=True,
        env=clean_environment,
    )
    assert dependency_check.returncode == 0, dependency_check.stdout + dependency_check.stderr
    outside = tmp_path / "unrelated-wheel-cwd"
    outside.mkdir()
    loaded = subprocess.run(
        [str(python), "-c", "import cltav_offline; print(cltav_offline.__file__)"],
        cwd=outside,
        text=True,
        capture_output=True,
        env=clean_environment,
    )
    assert loaded.returncode == 0, loaded.stderr
    loaded_path = loaded.stdout.replace("\\", "/").strip().lower()
    assert "/site-packages/cltav_offline/" in loaded_path
    assert str(root).replace("\\", "/").lower() not in loaded_path

    socket_guard = tmp_path / "socket-guard"
    socket_guard.mkdir()
    marker = socket_guard / "loaded.txt"
    (socket_guard / "sitecustomize.py").write_text(
        "import os\n"
        "from pathlib import Path\n"
        "import socket\n"
        "Path(os.environ['G4_SOCKET_GUARD_MARKER']).write_text('loaded', encoding='utf-8')\n"
        "def _blocked(*args, **kwargs):\n"
        "    raise AssertionError('G4 offline bridge must not create a network socket')\n"
        "socket.create_connection = _blocked\n"
        "class _BlockedSocket(socket.socket):\n"
        "    def connect(self, *args, **kwargs):\n"
        "        return _blocked(*args, **kwargs)\n"
        "    def connect_ex(self, *args, **kwargs):\n"
        "        return _blocked(*args, **kwargs)\n"
        "    def send(self, *args, **kwargs):\n"
        "        return _blocked(*args, **kwargs)\n"
        "    def sendall(self, *args, **kwargs):\n"
        "        return _blocked(*args, **kwargs)\n"
        "    def sendto(self, *args, **kwargs):\n"
        "        return _blocked(*args, **kwargs)\n"
        "    def bind(self, *args, **kwargs):\n"
        "        return _blocked(*args, **kwargs)\n"
        "    def listen(self, *args, **kwargs):\n"
        "        return _blocked(*args, **kwargs)\n"
        "socket.socket = _BlockedSocket\n",
        encoding="utf-8",
    )
    environment = dict(clean_environment)
    environment["PYTHONPATH"] = str(socket_guard)
    environment["G4_SOCKET_GUARD_MARKER"] = str(marker)
    capture = outside / "wheel.pcap"
    evidence = outside / "wheel.intake.json"
    bridge = outside / "wheel.bridge.json"
    capture.write_bytes(_pcap(_complete_exchange()))
    inspected = subprocess.run(
        [
            str(entrypoint), "inspect", "--input", str(capture), "--capture-id", "cap-g4-wheel",
            "--output", str(evidence), "--source-commit", "a" * 40,
        ],
        cwd=outside,
        text=True,
        capture_output=True,
        env=environment,
    )
    assert inspected.returncode == 0, inspected.stderr
    replayed = subprocess.run(
        [str(entrypoint), "replay", "--input", str(capture), "--offline-evidence", str(evidence), "--output", str(bridge)],
        cwd=outside,
        text=True,
        capture_output=True,
        env=environment,
    )
    assert replayed.returncode == 0, replayed.stderr
    assert marker.read_text(encoding="utf-8") == "loaded"
    document = json.loads(bridge.read_text(encoding="utf-8"))
    _assert_non_scoring(document)
    validated = subprocess.run(
        [str(entrypoint), "validate-replay", "--input", str(capture), "--offline-evidence", str(evidence), "--bridge", str(bridge)],
        cwd=outside,
        text=True,
        capture_output=True,
        env=environment,
    )
    assert validated.returncode == 0, validated.stderr

    old = bridge.read_bytes()
    forged = json.loads(evidence.read_bytes())
    forged["schemaVersion"] = "99.0"
    bad_evidence = outside / "wheel.bad-intake.json"
    bad_evidence.write_bytes(canonical_json_bytes(forged))
    rejected = subprocess.run(
        [str(entrypoint), "replay", "--input", str(capture), "--offline-evidence", str(bad_evidence), "--output", str(bridge)],
        cwd=outside,
        text=True,
        capture_output=True,
        env=environment,
    )
    assert rejected.returncode == 1
    assert "OFFLINE-EVIDENCE-VERSION-ERROR" in rejected.stderr
    assert bridge.read_bytes() == old
