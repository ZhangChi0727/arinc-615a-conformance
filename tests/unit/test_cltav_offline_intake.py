"""Public synthetic end-to-end tests for the bounded offline intake slice."""

from __future__ import annotations

import json
import socket
import struct
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from cltav_offline.capture import CaptureReader
from cltav_offline.cli import main as cli_main
from cltav_offline import corpus as corpus_module
from cltav_offline.corpus import audit_manifest, publish_json, run_corpus
from cltav_offline.evidence import evidence_errors
from cltav_offline.pipeline import IntakeConfig, IntakeError, run_capture


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


def _request(opcode: int, filename: str, options: dict[str, str] | None = None) -> bytes:
    data = struct.pack("!H", opcode) + filename.encode("ascii") + b"\0octet\0"
    for key, value in (options or {}).items():
        data += key.encode("ascii") + b"\0" + value.encode("ascii") + b"\0"
    return data


def _data(block: int, payload: bytes) -> bytes:
    return struct.pack("!HH", 3, block) + payload


def _ack(block: int) -> bytes:
    return struct.pack("!HH", 4, block)


def _oack(options: dict[str, str]) -> bytes:
    result = struct.pack("!H", 6)
    for key, value in options.items():
        result += key.encode("ascii") + b"\0" + value.encode("ascii") + b"\0"
    return result


def _pcap(records: list[bytes], *, link_type: int = 1) -> bytes:
    result = b"\xd4\xc3\xb2\xa1" + struct.pack("<HHIIII", 2, 4, 0, 0, 65535, link_type)
    for index, record in enumerate(records, 1):
        result += struct.pack("<IIII", 1, index, len(record), len(record)) + record
    return result


def _block(block_type: int, body: bytes) -> bytes:
    total = 12 + len(body)
    assert total % 4 == 0
    return struct.pack("<II", block_type, total) + body + struct.pack("<I", total)


def _pcapng(records: list[bytes]) -> bytes:
    section_body = struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1)
    interface_body = struct.pack("<HHI", 1, 0, 65535) + struct.pack("<HHB3x", 9, 1, 6)
    result = _block(0x0A0D0D0A, section_body) + _block(1, interface_body)
    for index, record in enumerate(records, 1):
        padding = b"\0" * (-len(record) % 4)
        body = struct.pack("<IIIII", 0, 0, index, len(record), len(record)) + record + padding
        result += _block(6, body)
    return result


def _lui_header() -> bytes:
    # File Length, two ASCII protocol-version bytes, acceptance status, zero-length description.
    return (9).to_bytes(4, "big") + b"A1" + b"\0\0" + b"\0"


def _valid_exchange() -> list[bytes]:
    request = _request(1, "load.lui")
    payload = _lui_header()
    return [
        _ethernet_ipv4(_udp(10000, 69, request), identification=10),
        _ethernet_ipv4(_udp(40000, 10000, _data(1, payload)), source="10.0.0.2", destination="10.0.0.1", identification=11),
        _ethernet_ipv4(_udp(10000, 40000, _ack(1)), identification=12),
    ]


def test_pcap_pipeline_reconstructs_tftp_and_bounded_file_event(tmp_path: Path) -> None:
    capture = tmp_path / "valid.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    result = run_capture(capture, capture_id="SYN-01")
    assert result.has_controlled_issue is False
    assert [item.status for item in result.datagrams] == ["COMPLETE", "COMPLETE", "COMPLETE"]
    transfer = result.transfers[0]
    assert transfer.reconstruction_status == "COMPLETE"
    assert transfer.option_status == "DEFAULTED"
    assert transfer.effective_block_size == 512
    event_types = [item.event_type for item in result.events]
    assert event_types == [
        "TFTP-TRANSFER-OBSERVED", "FIRST-SLICE-FILE-HEADER", "FIRST-SLICE-FILE-EVIDENCE",
    ]
    evidence = result.to_dict(source_commit="0" * 40)
    assert evidence["evidenceBoundary"]["conformanceVerdict"] == "NOT-EVALUATED"
    assert evidence["transfers"][0]["completePayloadLength"] == len(_lui_header())
    assert "completePayloadBytes" not in json.dumps(evidence)


def test_pcapng_timestamp_resolution_and_container_metadata(tmp_path: Path) -> None:
    capture = tmp_path / "valid.pcapng"
    capture.write_bytes(_pcapng(_valid_exchange()[:1]))
    reader = CaptureReader(capture, "SYN-02")
    packets = list(reader)
    assert len(packets) == 1
    assert packets[0].ref.timestamp is not None
    assert packets[0].ref.timestamp.ticks_per_second == 1_000_000
    assert reader.metadata.container_format == "PCAPNG"
    assert reader.metadata.interfaces[0].link_type == 1


def test_out_of_order_duplicate_and_conflicting_ipv4_fragments_are_not_overwritten(tmp_path: Path) -> None:
    payload = _udp(10001, 69, _request(1, "fragment.lui"))
    first = payload[:16]
    second = payload[16:]
    complete = tmp_path / "fragmented.pcap"
    complete.write_bytes(_pcap([
        _ethernet_ipv4(second, identification=30, offset_bytes=16),
        _ethernet_ipv4(first, identification=30, more_fragments=True),
    ]))
    result = run_capture(complete, capture_id="SYN-03")
    assert [item.status for item in result.datagrams] == ["COMPLETE"]
    assert len(result.transfers) == 1
    duplicate = tmp_path / "duplicate.pcap"
    duplicate.write_bytes(_pcap([
        _ethernet_ipv4(first, identification=32, more_fragments=True),
        _ethernet_ipv4(first, identification=32, more_fragments=True),
        _ethernet_ipv4(second, identification=32, offset_bytes=16),
    ]))
    duplicate_result = run_capture(duplicate, capture_id="SYN-03B")
    assert [item.status for item in duplicate_result.datagrams] == ["COMPLETE"]
    conflict = tmp_path / "conflict.pcap"
    changed = bytearray(first)
    changed[-1] ^= 0xFF
    conflict.write_bytes(_pcap([
        _ethernet_ipv4(first, identification=31, more_fragments=True),
        _ethernet_ipv4(bytes(changed), identification=31, more_fragments=True),
    ]))
    conflict_result = run_capture(conflict, capture_id="SYN-04")
    assert conflict_result.datagrams[0].status == "CONFLICT"
    assert conflict_result.datagrams[0].failure_code == "CONFLICTING-FRAGMENT-BYTES"


def test_tftp_accepted_defaulted_unknown_and_zero_terminator(tmp_path: Path) -> None:
    records = [
        _ethernet_ipv4(_udp(10010, 69, _request(2, "accepted.lur", {"blksize": "1024"})), identification=40),
        _ethernet_ipv4(_udp(40010, 10010, _oack({"blksize": "1024"})), source="10.0.0.2", destination="10.0.0.1", identification=41),
        _ethernet_ipv4(_udp(10010, 40010, _data(1, b"a" * 1024)), identification=42),
        _ethernet_ipv4(_udp(10010, 40010, _data(2, b"")), identification=43),
        _ethernet_ipv4(_udp(10011, 69, _request(1, "unknown.lui", {"blksize": "1024"})), identification=44),
    ]
    capture = tmp_path / "options.pcap"
    capture.write_bytes(_pcap(records))
    result = run_capture(capture, capture_id="SYN-05")
    accepted, unknown = result.transfers
    assert accepted.option_status == "ACCEPTED"
    assert accepted.effective_block_size == 1024
    assert accepted.reconstruction_status == "COMPLETE"
    assert accepted.terminal_block == 2
    assert unknown.option_status == "UNKNOWN"
    assert unknown.effective_block_size is None
    assert unknown.reconstruction_status == "GAPPED"


def test_unknown_linktype_is_controlled_not_silently_complete(tmp_path: Path) -> None:
    capture = tmp_path / "linktype.pcap"
    capture.write_bytes(_pcap([b"\0" * 20], link_type=101))
    result = run_capture(capture, capture_id="SYN-06")
    assert result.has_controlled_issue is True
    assert result.diagnostics[0].code == "UNSUPPORTED-LINKTYPE"


def test_cli_uses_atomic_output_and_does_not_overwrite_on_fatal_input(tmp_path: Path) -> None:
    output = tmp_path / "evidence.json"
    output.write_text("old bytes", encoding="utf-8")
    assert cli_main([
        "inspect", "--input", str(tmp_path / "missing.pcap"), "--capture-id", "SYN-07", "--output", str(output),
    ]) == 1
    assert output.read_text(encoding="utf-8") == "old bytes"
    capture = tmp_path / "valid.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", "SYN-07", "--output", str(output),
        "--source-commit", "1" * 40,
    ]) == 0
    rendered = json.loads(output.read_text(encoding="utf-8"))
    assert rendered["tool"]["sourceCommit"] == "1" * 40
    assert rendered["executionStatus"] == "COMPLETE"


def test_corpus_audit_and_staged_run_do_not_publish_machine_paths(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    capture = corpus / "one.pcapng"
    capture.write_bytes(_pcapng(_valid_exchange()))
    size = capture.stat().st_size
    import hashlib
    sha = hashlib.sha256(capture.read_bytes()).hexdigest()
    manifest = {
        "manifestId": "CLTAV-HISTORICAL-CAPTURES", "manifestVersion": "1.0",
        "purpose": "EXPLORATORY-DEVELOPMENT-ONLY", "captureCount": 1,
        "truthBoundary": "not experimental truth",
        "captures": [{
            "captureId": "HC-01", "relativePath": "one.pcapng", "byteCount": size, "sha256": sha,
            "observationQuality": "UNASSESSED-EXPLORATORY", "labelSource": "FILE-ANNOTATION-NONTRUTH", "rootCause": "UNKNOWN",
        }],
    }
    assert audit_manifest(manifest, corpus) == []
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    output = tmp_path / "out"
    summary = run_corpus(
        manifest_path=manifest_path, corpus_root=corpus, output_dir=output,
        config=IntakeConfig(), source_commit="2" * 40,
    )
    assert summary["captures"][0]["executionStatus"] == "COMPLETE"
    text = (output / "corpus-index.json").read_text(encoding="utf-8")
    assert str(corpus) not in text
    assert (output / "HC-01.json").is_file()


def test_evidence_envelope_matches_schema_and_rejects_raw_payload_field(tmp_path: Path) -> None:
    capture = tmp_path / "valid.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    evidence = run_capture(capture, capture_id="SYN-08").to_dict(source_commit="3" * 40)
    assert evidence_errors(evidence) == []
    schema_path = Path(__file__).resolve().parents[2] / "configs/engineering/cltav_offline_intake_evidence.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(evidence)) == []
    mutation = deepcopy(evidence)
    mutation["rawPayload"] = "not permitted"
    assert any("forbidden" in item for item in evidence_errors(mutation))


def test_output_publish_failure_preserves_existing_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    output = tmp_path / "existing.json"
    output.write_text("old", encoding="utf-8")
    original_replace = corpus_module.os.replace

    def fail_replace(source: Path | str, target: Path | str) -> None:
        raise OSError("injected replacement failure")

    monkeypatch.setattr(corpus_module.os, "replace", fail_replace)
    with pytest.raises(IntakeError) as caught:
        publish_json({"safe": True}, output)
    assert caught.value.code == "OUTPUT-PUBLISH-ERROR"
    assert output.read_text(encoding="utf-8") == "old"
    monkeypatch.setattr(corpus_module.os, "replace", original_replace)


def test_directory_publish_rolls_back_and_first_failure_leaves_no_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "published"
    target.mkdir()
    (target / "old.json").write_text("old", encoding="utf-8")
    stage = tmp_path / "stage"
    stage.mkdir()
    (stage / "new.json").write_text("new", encoding="utf-8")
    original_replace = corpus_module.os.replace

    def fail_stage(source: Path | str, destination: Path | str) -> None:
        if Path(source) == stage:
            raise OSError("injected directory replacement failure")
        original_replace(source, destination)

    monkeypatch.setattr(corpus_module.os, "replace", fail_stage)
    with pytest.raises(IntakeError) as caught:
        corpus_module._publish_directory(stage, target)
    assert caught.value.code == "OUTPUT-PUBLISH-ERROR"
    assert (target / "old.json").read_text(encoding="utf-8") == "old"
    assert stage.is_dir()
    monkeypatch.setattr(corpus_module.os, "replace", original_replace)
    shutil_target = tmp_path / "first-target"
    first_stage = tmp_path / "first-stage"
    first_stage.mkdir()
    (first_stage / "new.json").write_text("new", encoding="utf-8")

    def fail_first(source: Path | str, destination: Path | str) -> None:
        if Path(source) == first_stage:
            raise OSError("injected first publication failure")
        original_replace(source, destination)

    monkeypatch.setattr(corpus_module.os, "replace", fail_first)
    with pytest.raises(IntakeError) as caught:
        corpus_module._publish_directory(first_stage, shutil_target)
    assert caught.value.code == "OUTPUT-PUBLISH-ERROR"
    assert not shutil_target.exists()


def test_pcapng_sections_keep_clock_domains_and_interface_identity_distinct(tmp_path: Path) -> None:
    first = _pcapng(_valid_exchange()[:1])
    second = _pcapng(_valid_exchange()[1:2])
    capture = tmp_path / "two-sections.pcapng"
    capture.write_bytes(first + second)
    reader = CaptureReader(capture, "SYN-09")
    packets = list(reader)
    assert [item.ref.interface_id for item in packets] == [0, 1]
    assert packets[0].ref.timestamp is not None and packets[1].ref.timestamp is not None
    assert packets[0].ref.timestamp.clock_domain != packets[1].ref.timestamp.clock_domain
