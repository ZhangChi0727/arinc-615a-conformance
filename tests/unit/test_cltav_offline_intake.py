"""Public synthetic end-to-end tests for the bounded offline intake slice."""

from __future__ import annotations

import json
import os
import socket
import struct
import hashlib
import subprocess
import sys
import zipfile
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from cltav_offline.capture import CaptureFormatError, CaptureReader, PCAPNG_SECTION_HEADER
from cltav_offline.cli import main as cli_main
from cltav_offline import corpus as corpus_module
from cltav_offline import pipeline as pipeline_module
from cltav_offline import controlled_resources
from cltav_offline import development_contract as development_contract_module
from cltav_offline import evidence as evidence_module
from cltav_offline.corpus import audit_manifest, publish_json, run_corpus
from cltav_offline.development_contract import accepted_record_contracts
from cltav_offline.evidence import evidence_errors
from cltav_offline.events import decode_first_slice_header
from cltav_offline.models import DatagramRecord, Ipv4Fragment, PacketRef, Timestamp, UdpDatagram
from cltav_offline.network import Ipv4Reassembler
from cltav_offline.pipeline import IntakeConfig, IntakeError, IntakeResult, run_capture
from cltav_offline.tftp import TftpReconstructor
from scripts.check_development_readiness import validate_record_instance


def _ethernet_ipv4(
    payload: bytes,
    *,
    source: str = "10.0.0.1",
    destination: str = "10.0.0.2",
    identification: int = 1,
    offset_bytes: int = 0,
    more_fragments: bool = False,
    vlan_tags: tuple[int, ...] = (),
) -> bytes:
    assert offset_bytes % 8 == 0
    flags_offset = (0x2000 if more_fragments else 0) | (offset_bytes // 8)
    ipv4 = struct.pack(
        "!BBHHHBBH4s4s",
        0x45, 0, 20 + len(payload), identification, flags_offset, 64, 17, 0,
        socket.inet_aton(source), socket.inet_aton(destination),
    ) + payload
    ethernet = b"\xaa" * 6 + b"\xbb" * 6
    for index, tag in enumerate(vlan_tags):
        ethernet += struct.pack("!H", 0x8100 if index == 0 else 0x88A8)
        ethernet += struct.pack("!H", tag & 0x0FFF)
    return ethernet + struct.pack("!H", 0x0800) + ipv4


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


def _pcapng_with_epb_comment(record: bytes) -> bytes:
    section_body = struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1)
    interface_body = struct.pack("<HHI", 1, 0, 0)
    padding = b"\0" * (-len(record) % 4)
    # A legal opt_comment followed by the required end-of-options marker.
    options = struct.pack("<HH", 1, 3) + b"abc\0" + struct.pack("<HH", 0, 0)
    epb_body = struct.pack("<IIIII", 0, 0, 1, len(record), len(record)) + record + padding + options
    return _block(0x0A0D0D0A, section_body) + _block(1, interface_body) + _block(6, epb_body)


def _lui_header() -> bytes:
    # File Length, two ASCII protocol-version bytes, acceptance status, zero-length description.
    return (9).to_bytes(4, "big") + b"A1" + b"\0\0" + b"\0"


def _role_header(role: str, declared_length: int | None = None) -> bytes:
    """Return one structurally valid bounded A1 header for every supported role."""
    suffixes = {
        "LCI": b"\0\0\0",
        "LCL": b"\0\x02",
        "LCS": b"\0\x01\0\x02\0\x03\xff\xff\0",
        "LUI": b"\0\0\0",
        "LUR": b"\0\x02",
        "LUS": b"\0\x04\0\0\x01\0\x02\xff\xff75%",
    }
    suffix = suffixes[role]
    actual_length = 6 + len(suffix)
    return (actual_length if declared_length is None else declared_length).to_bytes(4, "big") + b"A1" + suffix


def _valid_exchange() -> list[bytes]:
    request = _request(1, "load.lui")
    payload = _lui_header()
    return [
        _ethernet_ipv4(_udp(10000, 69, request), identification=10),
        _ethernet_ipv4(_udp(40000, 10000, _data(1, payload)), source="10.0.0.2", destination="10.0.0.1", identification=11),
        _ethernet_ipv4(_udp(10000, 40000, _ack(1)), identification=12),
    ]


def _corpus_manifest(corpus: Path, capture_id: str = "HC-01") -> dict[str, object]:
    """Build a public, one-file corpus manifest without retaining packet payload."""
    capture = corpus / "one.pcapng"
    return {
        "manifestId": "CLTAV-HISTORICAL-CAPTURES", "manifestVersion": "1.0",
        "purpose": "EXPLORATORY-DEVELOPMENT-ONLY", "captureCount": 1,
        "truthBoundary": "not experimental truth",
        "captures": [{
            "captureId": capture_id, "relativePath": "one.pcapng",
            "byteCount": capture.stat().st_size,
            "sha256": hashlib.sha256(capture.read_bytes()).hexdigest(),
            "observationQuality": "UNASSESSED-EXPLORATORY",
            "labelSource": "FILE-ANNOTATION-NONTRUTH", "rootCause": "UNKNOWN",
        }],
    }


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
    assert all(item.payload is None for item in result.datagrams)
    assert result.transfers[0].complete_payload is None


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


def test_partial_first_slice_parse_is_a_controlled_execution_issue(tmp_path: Path) -> None:
    partial_lui = (9).to_bytes(4, "big") + b"A1" + b"\0\0" + b"\x05"
    server = {"source": "10.0.0.2", "destination": "10.0.0.1"}
    capture = tmp_path / "partial-lui.pcap"
    capture.write_bytes(_pcap([
        _ethernet_ipv4(_udp(10012, 69, _request(1, "partial.lui")), identification=45),
        _ethernet_ipv4(_udp(40012, 10012, _data(1, partial_lui)), identification=46, **server),
    ]))
    result = run_capture(capture, capture_id="cap-partial-lui")
    parse = next(event for event in result.events if event.layer == "PARSE-RESULT")
    assert parse.fields["parseStatus"] == "PARTIAL"
    assert not any(event.layer == "APPLICATION" for event in result.events)
    assert result.has_controlled_issue is True
    evidence = result.to_dict(source_commit="a" * 40)
    assert evidence["executionStatus"] == "COMPLETE-WITH-CONTROLLED-ISSUES"
    assert evidence_errors(evidence) == []

    output = tmp_path / "partial-lui.json"
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", "cap-partial-lui", "--output", str(output),
        "--source-commit", "a" * 40,
    ]) == 2

    corpus = tmp_path / "partial-corpus"
    corpus.mkdir()
    corpus_capture = corpus / "one.pcapng"
    corpus_capture.write_bytes(_pcapng([
        _ethernet_ipv4(_udp(10012, 69, _request(1, "partial.lui")), identification=45),
        _ethernet_ipv4(_udp(40012, 10012, _data(1, partial_lui)), identification=46, **server),
    ]))
    manifest_path = tmp_path / "partial-manifest.json"
    manifest_path.write_text(json.dumps(_corpus_manifest(corpus)), encoding="utf-8")
    corpus_output = tmp_path / "partial-output"
    assert cli_main([
        "corpus", "--manifest", str(manifest_path), "--corpus-root", str(corpus), "--output-dir", str(corpus_output),
        "--source-commit", "a" * 40,
    ]) == 2
    assert json.loads((corpus_output / "corpus-index.json").read_text(encoding="utf-8"))["captures"][0]["executionStatus"] == "COMPLETE-WITH-CONTROLLED-ISSUES"


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
    manifest = _corpus_manifest(corpus)
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


@pytest.mark.parametrize("target_kind", ["same", "descendant", "ancestor", "manifest-parent"])
def test_corpus_publication_rejects_input_overlapping_targets_before_staging(
    tmp_path: Path, target_kind: str,
) -> None:
    """A result transaction must never rename/delete an input ancestor or manifest parent."""
    source_parent = tmp_path / "source-parent"
    corpus = source_parent / "corpus"
    corpus.mkdir(parents=True)
    capture = corpus / "one.pcapng"
    capture.write_bytes(_pcapng(_valid_exchange()))
    manifest_path = source_parent / "manifest.json"
    manifest_path.write_text(json.dumps(_corpus_manifest(corpus)), encoding="utf-8")
    original_capture = hashlib.sha256(capture.read_bytes()).hexdigest()
    original_manifest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    target = {
        "same": corpus,
        "descendant": corpus / "results",
        "ancestor": source_parent,
        "manifest-parent": source_parent,
    }[target_kind]
    with pytest.raises(IntakeError) as caught:
        run_corpus(
            manifest_path=manifest_path,
            corpus_root=corpus,
            output_dir=target,
            config=IntakeConfig(),
            source_commit="a" * 40,
        )
    assert caught.value.code == "UNSAFE-OUTPUT-PATH"
    assert hashlib.sha256(capture.read_bytes()).hexdigest() == original_capture
    assert hashlib.sha256(manifest_path.read_bytes()).hexdigest() == original_manifest
    assert not list(source_parent.glob(".*.staging-*"))


def test_corpus_publication_rejects_alias_output_before_writes(tmp_path: Path) -> None:
    source_parent = tmp_path / "source-parent"
    corpus = source_parent / "corpus"
    corpus.mkdir(parents=True)
    capture = corpus / "one.pcapng"
    capture.write_bytes(_pcapng(_valid_exchange()))
    manifest_path = tmp_path / "manifest.json"
    manifest = _corpus_manifest(corpus)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    safe_output = tmp_path / "safe-output"
    run_corpus(
        manifest_path=manifest_path, corpus_root=corpus, output_dir=safe_output,
        config=IntakeConfig(), source_commit="b" * 40,
    )
    old_output_hash = hashlib.sha256((safe_output / "corpus-index.json").read_bytes()).hexdigest()
    alias = tmp_path / "source-alias"
    try:
        os.symlink(source_parent, alias, target_is_directory=True)
    except OSError as exc:
        if os.name != "nt":
            pytest.skip(f"directory symlink fixture unavailable: {exc}")
        # A junction exercises the same resolved-target containment boundary on
        # Windows machines where symlink creation needs a privilege.  It is
        # confined to pytest's temporary source/alias directories.
        junction = subprocess.run(
            ["cmd.exe", "/d", "/c", "mklink", "/J", str(alias), str(source_parent)],
            check=False,
            capture_output=True,
            text=True,
        )
        if junction.returncode != 0:
            pytest.skip(f"directory alias fixture unavailable: {exc}; {junction.stderr.strip()}")
    with pytest.raises(IntakeError) as caught:
        run_corpus(
            manifest_path=manifest_path, corpus_root=corpus, output_dir=alias,
            config=IntakeConfig(), source_commit="b" * 40,
        )
    assert caught.value.code == "UNSAFE-OUTPUT-PATH"
    assert hashlib.sha256((safe_output / "corpus-index.json").read_bytes()).hexdigest() == old_output_hash


def test_corpus_publication_refuses_nonowned_target_and_unsafe_capture_id_before_writes(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "one.pcapng").write_bytes(_pcapng(_valid_exchange()))
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_corpus_manifest(corpus)), encoding="utf-8")
    output = tmp_path / "existing"
    output.mkdir()
    sentinel = output / "unrelated.txt"
    sentinel.write_text("do not replace", encoding="utf-8")
    with pytest.raises(IntakeError) as caught:
        run_corpus(
            manifest_path=manifest_path, corpus_root=corpus, output_dir=output,
            config=IntakeConfig(), source_commit="b" * 40,
        )
    assert caught.value.code == "UNSAFE-OUTPUT-PATH"
    assert sentinel.read_text(encoding="utf-8") == "do not replace"
    malicious = _corpus_manifest(corpus, "../escape")
    manifest_path.write_text(json.dumps(malicious), encoding="utf-8")
    with pytest.raises(IntakeError) as invalid_id:
        run_corpus(
            manifest_path=manifest_path, corpus_root=corpus, output_dir=output,
            config=IntakeConfig(), source_commit="b" * 40,
        )
    assert invalid_id.value.code == "CORPUS-IDENTITY-AUDIT-FAILED"
    assert not (tmp_path / "escape.json").exists()
    assert sentinel.read_text(encoding="utf-8") == "do not replace"


def test_evidence_envelope_matches_schema_and_rejects_raw_payload_field(tmp_path: Path) -> None:
    capture = tmp_path / "valid.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    evidence = run_capture(capture, capture_id="SYN-08").to_dict(source_commit="3" * 40)
    assert evidence_errors(evidence) == []
    shared_only = run_capture(
        capture, capture_id="SYN-11D", config=IntakeConfig(max_evidence_records=2),
    ).to_dict(source_commit="9" * 40)
    assert sum(
        len(shared_only[name]) for name in ("packetRefs", "datagrams", "transfers", "events", "diagnostics")
    ) <= 2
    assert shared_only["input"]["container"]["scanStatus"] == "STOPPED-RESOURCE-LIMIT"
    assert evidence_errors(shared_only) == []
    schema_path = Path(__file__).resolve().parents[2] / "configs/engineering/cltav_offline_intake_evidence.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(evidence)) == []
    mutation = deepcopy(evidence)
    mutation["rawPayload"] = "not permitted"
    assert any("Additional properties" in item for item in evidence_errors(mutation))


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


def test_reassembly_fragment_limit_and_transfer_record_limit_are_controlled(tmp_path: Path) -> None:
    payload = _udp(10001, 69, _request(1, "limited.lui"))
    first, second = payload[:16], payload[16:]
    fragmented = tmp_path / "fragment-limit.pcap"
    fragmented.write_bytes(_pcap([
        _ethernet_ipv4(first, identification=60, more_fragments=True),
        _ethernet_ipv4(second, identification=60, offset_bytes=16),
    ]))
    fragment_limited = run_capture(
        fragmented,
        capture_id="SYN-10",
        config=IntakeConfig(max_fragments_per_datagram=1),
    )
    assert [item.status for item in fragment_limited.datagrams] == ["GAPPED"]
    assert fragment_limited.datagrams[0].failure_code == "RESOURCE-FRAGMENT-COUNT-LIMIT"

    requests = tmp_path / "transfer-limit.pcap"
    requests.write_bytes(_pcap([
        _ethernet_ipv4(_udp(10020, 69, _request(1, "one.lui")), identification=61),
        _ethernet_ipv4(_udp(10021, 69, _request(1, "two.lui")), identification=62),
    ]))
    transfer_limited = run_capture(
        requests,
        capture_id="SYN-11",
        config=IntakeConfig(max_transfer_records=1),
    )
    assert len(transfer_limited.transfers) == 1
    assert any(item.code == "RESOURCE-TRANSFER-RECORD-LIMIT" for item in transfer_limited.diagnostics)
    assert transfer_limited.has_controlled_issue is True


def test_resource_limits_bound_bad_packet_evidence_and_preserve_source_identity(tmp_path: Path) -> None:
    # Non-IPv4 Ethernet frames exercise the formerly unbounded diagnostic-only path.
    capture = tmp_path / "many-unsupported.pcap"
    capture.write_bytes(_pcap([b"\0" * 20 for _ in range(12)]))
    result = run_capture(
        capture,
        capture_id="SYN-11B",
        config=IntakeConfig(max_evidence_records=2, max_packet_refs=3, max_diagnostics=3),
    )
    evidence = result.to_dict(source_commit="9" * 40)
    assert len(evidence["packetRefs"]) <= 3
    assert len(evidence["diagnostics"]) <= 3
    assert evidence["input"]["container"]["scanStatus"] == "STOPPED-RESOURCE-LIMIT"
    packet_ids = {item["packetRefId"] for item in evidence["packetRefs"]}
    for diagnostic in evidence["diagnostics"]:
        assert diagnostic["detail"]["inputSha256"] == evidence["input"]["sha256"]
        if "packetRefId" in diagnostic:
            assert diagnostic["packetRefId"] in packet_ids
    assert evidence_errors(evidence) == []


def test_shared_evidence_budget_counts_interfaces_and_reserves_a_stop_witness(tmp_path: Path) -> None:
    capture = tmp_path / "shared-budget.pcap"
    capture.write_bytes(_pcap(_valid_exchange()[:1]))
    result = run_capture(
        capture,
        capture_id="SYN-SHARED-BUDGET",
        config=IntakeConfig(max_evidence_records=2, max_packet_refs=10, max_diagnostics=10),
    )
    evidence = result.to_dict(source_commit="a" * 40)
    retained = (
        len(evidence["input"]["container"]["interfaces"])
        + len(evidence["packetRefs"])
        + len(evidence["datagrams"])
        + len(evidence["transfers"])
        + len(evidence["events"])
        + len(evidence["diagnostics"])
    )
    assert retained <= 2
    assert evidence["input"]["container"]["scanStatus"] == "STOPPED-RESOURCE-LIMIT"
    assert evidence["executionStatus"] == "COMPLETE-WITH-CONTROLLED-ISSUES"
    stop = next(item for item in evidence["diagnostics"] if item["code"].startswith("RESOURCE-"))
    assert stop["detail"]["lastConsumedPacketIndex"] == 1
    assert stop["detail"]["lastConsumedContainerOffset"] >= 24
    assert evidence_errors(evidence) == []

    with pytest.raises(IntakeError) as caught:
        run_capture(capture, capture_id="SYN-SHARED-INVALID", config=IntakeConfig(max_evidence_records=1))
    assert caught.value.code == "INVALID-RUNTIME-LIMIT"

    section_body = struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1)
    idb = struct.pack("<HHI", 1, 0, 65535)
    two_interfaces = tmp_path / "two-interfaces.pcapng"
    two_interfaces.write_bytes(_block(PCAPNG_SECTION_HEADER, section_body) + _block(1, idb) + _block(1, idb))
    interface_budget = run_capture(
        two_interfaces,
        capture_id="SYN-SHARED-INTERFACES",
        config=IntakeConfig(max_evidence_records=2),
    ).to_dict(source_commit="a" * 40)
    assert interface_budget["input"]["container"]["scanStatus"] == "STOPPED-RESOURCE-LIMIT"
    assert [item["code"] for item in interface_budget["diagnostics"]] == ["RESOURCE-INTERFACE-EVIDENCE-LIMIT"]
    assert evidence_errors(interface_budget) == []


def test_interface_resource_limit_is_a_named_capture_error(tmp_path: Path) -> None:
    section_body = struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1)
    idb = struct.pack("<HHI", 1, 0, 0)
    capture = tmp_path / "many-interfaces.pcapng"
    capture.write_bytes(_block(0x0A0D0D0A, section_body) + _block(1, idb) + _block(1, idb))
    with pytest.raises(IntakeError) as caught:
        run_capture(capture, capture_id="SYN-11C", config=IntakeConfig(max_interfaces=1))
    assert caught.value.code == "RESOURCE-INTERFACE-LIMIT"


def test_invalid_provenance_and_fatal_container_never_replace_existing_output(tmp_path: Path) -> None:
    output = tmp_path / "evidence.json"
    output.write_text("previous evidence", encoding="utf-8")
    valid = tmp_path / "valid.pcap"
    valid.write_bytes(_pcap(_valid_exchange()))
    assert cli_main([
        "inspect", "--input", str(valid), "--capture-id", "SYN-12", "--output", str(output),
        "--source-commit", "not-a-git-object",
    ]) == 1
    assert output.read_text(encoding="utf-8") == "previous evidence"

    truncated = tmp_path / "truncated.pcap"
    truncated.write_bytes(_pcap(_valid_exchange())[:-3])
    assert cli_main([
        "inspect", "--input", str(truncated), "--capture-id", "SYN-12", "--output", str(output),
        "--source-commit", "4" * 40,
    ]) == 1
    assert output.read_text(encoding="utf-8") == "previous evidence"


def test_input_identity_change_is_fatal_and_invalid_source_is_not_publishable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    capture = tmp_path / "valid.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    actual_identity = pipeline_module.input_identity(capture)
    calls = 0

    def changing_identity(path: Path) -> tuple[int, str]:
        nonlocal calls
        calls += 1
        return actual_identity if calls == 1 else (actual_identity[0] + 1, actual_identity[1])

    monkeypatch.setattr(pipeline_module, "input_identity", changing_identity)
    with pytest.raises(IntakeError) as caught:
        run_capture(capture, capture_id="SYN-13")
    assert caught.value.code == "INPUT-IDENTITY-CHANGED"

    evidence = IntakeResult(
        capture_id="SYN-13", byte_count=0, sha256="0" * 64, config=IntakeConfig(), capture_metadata={}
    )
    with pytest.raises(IntakeError) as invalid_commit:
        evidence.to_dict(source_commit="UNSPECIFIED")
    assert invalid_commit.value.code == "INVALID-SOURCE-COMMIT"


def test_evidence_schema_requires_immutable_source_commit(tmp_path: Path) -> None:
    capture = tmp_path / "valid.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    evidence = run_capture(capture, capture_id="SYN-14").to_dict(source_commit="5" * 40)
    evidence["tool"]["sourceCommit"] = "5" * 39
    assert any("sourceCommit" in item for item in evidence_errors(evidence))
    schema_path = Path(__file__).resolve().parents[2] / "configs/engineering/cltav_offline_intake_evidence.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(evidence))


def test_production_evidence_validation_rejects_count_and_provenance_mutations(tmp_path: Path) -> None:
    capture = tmp_path / "valid.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    evidence = run_capture(capture, capture_id="SYN-15").to_dict(source_commit="6" * 40)
    count_mutation = deepcopy(evidence)
    count_mutation["counts"]["transfers"] = 0
    assert any("counts.transfers" in item for item in evidence_errors(count_mutation))
    provenance_mutation = deepcopy(evidence)
    provenance_mutation["events"][0]["transferId"] = "TR-NOT-PRESENT"
    assert any("known transfer" in item for item in evidence_errors(provenance_mutation))
    option_mutation = deepcopy(evidence)
    option_mutation["transfers"][0]["blockSize"] = {"status": "UNKNOWN", "value": 512}
    assert any("UNKNOWN transfer blockSize" in item for item in evidence_errors(option_mutation))


def test_production_schema_and_cross_record_validation_rejects_bad_envelopes(tmp_path: Path) -> None:
    capture = tmp_path / "valid.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    evidence = run_capture(capture, capture_id="SYN-15B").to_dict(source_commit="d" * 40)
    empty_parameters = deepcopy(evidence)
    empty_parameters["runParameters"] = {}
    assert evidence_errors(empty_parameters)
    integrity_pass = deepcopy(evidence)
    integrity_pass["evidenceBoundary"]["integrity"] = "PASS"
    assert evidence_errors(integrity_pass)
    negative_length = deepcopy(evidence)
    negative_length["packetRefs"][0]["capturedLength"] = -1
    assert evidence_errors(negative_length)
    foreign_capture = deepcopy(evidence)
    foreign_capture["datagrams"][0]["captureId"] = "OTHER"
    assert any("captureId differs" in item for item in evidence_errors(foreign_capture))
    missing_diagnostic_ref = deepcopy(evidence)
    missing_diagnostic_ref["diagnostics"] = [{
        "code": "SYNTHETIC", "stage": "TEST", "severity": "ERROR", "message": "synthetic",
        "packetRefId": "SYN-15B:P99999999",
    }]
    missing_diagnostic_ref["counts"]["diagnostics"] = 1
    assert any("diagnostic packetRefId" in item for item in evidence_errors(missing_diagnostic_ref))


def test_corpus_fatal_evidence_is_schema_valid_and_invalid_inspect_does_not_publish(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    bad = corpus / "one.pcapng"
    bad.write_bytes(b"not a capture")
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_corpus_manifest(corpus)), encoding="utf-8")
    output_dir = tmp_path / "result"
    summary = run_corpus(
        manifest_path=manifest_path, corpus_root=corpus, output_dir=output_dir,
        config=IntakeConfig(), source_commit="e" * 40,
    )
    assert summary["captures"][0]["executionStatus"] == "FATAL-INPUT-ERROR"
    fatal = json.loads((output_dir / "HC-01.json").read_text(encoding="utf-8"))
    assert evidence_errors(fatal) == []
    assert fatal["diagnostics"][0]["severity"] == "ERROR"

    output = tmp_path / "inspect.json"
    output.write_text("old", encoding="utf-8")
    original = pipeline_module.IntakeResult.to_dict

    def invalid_output(self: IntakeResult, *, source_commit: str) -> dict[str, object]:
        data = original(self, source_commit=source_commit)
        data["unexpected"] = True
        return data

    monkeypatch.setattr(pipeline_module.IntakeResult, "to_dict", invalid_output)
    valid = tmp_path / "valid.pcap"
    valid.write_bytes(_pcap(_valid_exchange()))
    assert cli_main([
        "inspect", "--input", str(valid), "--capture-id", "SYN-15C", "--output", str(output),
        "--source-commit", "f" * 40,
    ]) == 1
    assert output.read_text(encoding="utf-8") == "old"


def test_corpus_only_publishes_per_file_failures_for_actual_capture_input_faults(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    malformed = corpus / "one.pcapng"
    malformed.write_bytes(b"\x0a\x0d\x0d\x0a")
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_corpus_manifest(corpus)), encoding="utf-8")
    output = tmp_path / "result"
    summary = run_corpus(
        manifest_path=manifest_path, corpus_root=corpus, output_dir=output,
        config=IntakeConfig(), source_commit="d" * 40,
    )
    assert summary["captures"][0]["executionStatus"] == "FATAL-INPUT-ERROR"
    failure = json.loads((output / "HC-01.json").read_text(encoding="utf-8"))
    diagnostic = failure["diagnostics"][0]
    assert diagnostic["code"] == "TRUNCATED-PCAPNG-BLOCK-HEADER"
    assert diagnostic["stage"] == "CAPTURE"
    assert diagnostic["containerOffset"] == 0
    assert evidence_errors(failure) == []


def test_corpus_tool_failures_abort_staging_and_preserve_prior_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    first = corpus / "one.pcapng"
    second = corpus / "two.pcapng"
    first.write_bytes(_pcapng(_valid_exchange()))
    second.write_bytes(_pcapng(_valid_exchange()))
    digest_one = hashlib.sha256(first.read_bytes()).hexdigest()
    digest_two = hashlib.sha256(second.read_bytes()).hexdigest()
    manifest = _corpus_manifest(corpus)
    manifest["captureCount"] = 2
    manifest["captures"] = [
        {**manifest["captures"][0], "captureId": "HC-01", "relativePath": "one.pcapng", "byteCount": first.stat().st_size, "sha256": digest_one},
        {**manifest["captures"][0], "captureId": "HC-02", "relativePath": "two.pcapng", "byteCount": second.stat().st_size, "sha256": digest_two},
    ]
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    output = tmp_path / "result"
    run_corpus(
        manifest_path=manifest_path, corpus_root=corpus, output_dir=output,
        config=IntakeConfig(), source_commit="e" * 40,
    )
    old_bytes = {item.name: item.read_bytes() for item in output.iterdir()}
    original_to_dict = pipeline_module.IntakeResult.to_dict

    def malformed_second(self: IntakeResult, *, source_commit: str) -> dict[str, object]:
        rendered = original_to_dict(self, source_commit=source_commit)
        if self.capture_id == "HC-02":
            rendered["unexpectedToolField"] = True
        return rendered

    monkeypatch.setattr(pipeline_module.IntakeResult, "to_dict", malformed_second)
    with pytest.raises(IntakeError) as caught:
        run_corpus(
            manifest_path=manifest_path, corpus_root=corpus, output_dir=output,
            config=IntakeConfig(), source_commit="e" * 40,
        )
    assert caught.value.code == "EVIDENCE-SCHEMA-ERROR"
    assert {item.name: item.read_bytes() for item in output.iterdir()} == old_bytes
    assert not list(tmp_path.glob(".result.staging-*"))

    fresh = tmp_path / "fresh-result"
    def malformed_first(self: IntakeResult, *, source_commit: str) -> dict[str, object]:
        rendered = original_to_dict(self, source_commit=source_commit)
        rendered["unexpectedToolField"] = True
        return rendered

    monkeypatch.setattr(pipeline_module.IntakeResult, "to_dict", malformed_first)
    with pytest.raises(IntakeError):
        run_corpus(
            manifest_path=manifest_path, corpus_root=corpus, output_dir=fresh,
            config=IntakeConfig(), source_commit="e" * 40,
        )
    assert not fresh.exists()
    assert not list(tmp_path.glob(".fresh-result.staging-*"))


def test_normal_capture_has_publicly_valid_typed_contract_projection(tmp_path: Path) -> None:
    capture = tmp_path / "projection.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    result = run_capture(capture, capture_id="cap-valid")
    evidence = result.to_dict(source_commit="a" * 40)
    projection = evidence["contractProjection"]
    assert projection["nonProjectable"] == []
    assert projection["contractIdentity"]["path"] == "configs/engineering/cltav_development_contracts.json"
    contracts = json.loads(
        (Path(__file__).resolve().parents[2] / "configs/engineering/cltav_development_contracts.json").read_text(encoding="utf-8")
    )
    definitions = {item["id"]: item for item in contracts["recordContracts"]}
    for projected in projection["records"]:
        assert validate_record_instance(definitions[projected["recordType"]], projected["payload"]) == []
    transfer = next(item["payload"] for item in projection["records"] if item["recordType"] == "TRANSFER-RECORD")
    assert transfer["blockMap"] == {"1": "cap-valid:0:0:2"}
    assert transfer["request"].startswith("event-request-")


def test_nonprojectable_identity_is_explicit_not_filled_with_fake_contract_values(tmp_path: Path) -> None:
    capture = tmp_path / "nonprojectable.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    projection = run_capture(capture, capture_id="SYN-NONCONTRACT").to_dict(source_commit="a" * 40)["contractProjection"]
    assert projection["records"] == []
    assert any(item["sourceType"] == "PACKET-REF" for item in projection["nonProjectable"])


def test_cli_marks_git_oid_as_claim_and_never_derives_it_from_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    capture = tmp_path / "identity.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    unrelated = tmp_path / "unrelated-repository"
    unrelated.mkdir()
    monkeypatch.chdir(unrelated)
    monkeypatch.setenv("GITHUB_SHA", "f" * 40)
    output = tmp_path / "unverified.json"
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", "SYN-15D", "--output", str(output),
    ]) == 0
    unverified = json.loads(output.read_text(encoding="utf-8"))
    assert unverified["tool"]["sourceCommit"] == "UNVERIFIED"
    assert unverified["tool"]["sourceCommitStatus"] == "UNAVAILABLE"
    assert len(unverified["tool"]["runtimeSourceSha256"]) == 64
    claimed_output = tmp_path / "claimed.json"
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", "SYN-15E", "--output", str(claimed_output),
        "--source-commit", "f" * 40,
    ]) == 0
    claimed = json.loads(claimed_output.read_text(encoding="utf-8"))
    assert claimed["tool"]["sourceCommit"] == "f" * 40
    assert claimed["tool"]["sourceCommitStatus"] == "CLAIMED-UNVERIFIED"


def test_tftp_tid_binding_duplicate_and_missing_block_behaviour(tmp_path: Path) -> None:
    records = [
        _ethernet_ipv4(_udp(10030, 69, _request(2, "write.lur")), identification=70),
        _ethernet_ipv4(_udp(40100, 10030, _ack(0)), source="10.0.0.2", destination="10.0.0.1", identification=71),
        _ethernet_ipv4(_udp(10030, 40100, _data(1, b"abc")), identification=72),
        _ethernet_ipv4(_udp(10030, 40100, _data(1, b"abc")), identification=73),
        _ethernet_ipv4(_udp(10031, 69, _request(1, "missing.lci")), identification=74),
        _ethernet_ipv4(_udp(40101, 10031, _data(2, b"x")), source="10.0.0.2", destination="10.0.0.1", identification=75),
    ]
    capture = tmp_path / "tid-and-gaps.pcap"
    capture.write_bytes(_pcap(records))
    result = run_capture(capture, capture_id="SYN-16")
    complete, missing = result.transfers
    assert complete.request_kind == "WRQ"
    assert complete.server_endpoint == ("10.0.0.2", 40100)
    assert complete.reconstruction_status == "COMPLETE"
    assert complete.complete_payload is None
    assert complete.complete_payload_length == 3
    assert complete.to_dict()["completePayloadLength"] == 3
    assert missing.reconstruction_status == "GAPPED"
    assert "MISSING-TFTP-DATA-BLOCK" in missing.diagnostics


def test_tftp_terminal_states_are_not_recovered_by_later_data(tmp_path: Path) -> None:
    request = _ethernet_ipv4(_udp(10040, 69, _request(1, "terminal.lui")), identification=80)
    server = {"source": "10.0.0.2", "destination": "10.0.0.1"}
    full_a = _ethernet_ipv4(_udp(40040, 10040, _data(1, b"a" * 512)), identification=81, **server)
    full_b = _ethernet_ipv4(_udp(40040, 10040, _data(1, b"b" * 512)), identification=82, **server)
    terminator = _ethernet_ipv4(_udp(40040, 10040, _data(2, b"")), identification=83, **server)
    second_request = _ethernet_ipv4(_udp(10047, 69, _request(1, "error.lui")), identification=84)
    error = _ethernet_ipv4(_udp(40041, 10047, struct.pack("!HH", 5, 1) + b"no\0"), identification=85, **server)
    short = _ethernet_ipv4(_udp(40041, 10047, _data(1, b"x")), identification=86, **server)
    capture = tmp_path / "terminal.pcap"
    capture.write_bytes(_pcap([request, full_a, full_b, terminator, second_request, error, short]))
    result = run_capture(capture, capture_id="SYN-20")
    assert [item.reconstruction_status for item in result.transfers] == ["CONFLICT", "ERROR"]
    assert all(item.complete_payload_length is None for item in result.transfers)
    assert all(event.layer != "APPLICATION" for event in result.events)


def test_tftp_post_terminator_and_duplicate_request_are_conservative(tmp_path: Path) -> None:
    request = _ethernet_ipv4(_udp(10041, 69, _request(1, "duplicate.lui")), identification=86)
    server = {"source": "10.0.0.2", "destination": "10.0.0.1"}
    first = _ethernet_ipv4(_udp(40042, 10041, _data(1, b"a")), identification=87, **server)
    later = _ethernet_ipv4(_udp(40042, 10041, _data(2, b"b" * 512)), identification=88, **server)
    conflict_capture = tmp_path / "after-terminal.pcap"
    conflict_capture.write_bytes(_pcap([request, first, later]))
    conflict = run_capture(conflict_capture, capture_id="SYN-21")
    assert conflict.transfers[0].reconstruction_status == "CONFLICT"
    assert conflict.transfers[0].complete_payload_length is None

    duplicate_capture = tmp_path / "duplicate-request.pcap"
    duplicate_capture.write_bytes(_pcap([request, request, first]))
    duplicate = run_capture(duplicate_capture, capture_id="SYN-21B")
    assert len(duplicate.transfers) == 1
    assert duplicate.transfers[0].reconstruction_status == "COMPLETE"


def test_tftp_terminal_block_set_is_order_independent_and_completed_sessions_release_slots(tmp_path: Path) -> None:
    server = {"source": "10.0.0.2", "destination": "10.0.0.1"}
    # A full block above a later terminal is contradictory even when it was
    # observed first; it must never manufacture a longer COMPLETE transfer.
    above_terminal = [
        _ethernet_ipv4(_udp(10100, 69, _request(1, "above.lui")), identification=100),
        _ethernet_ipv4(_udp(40100, 10100, _data(2, b"x" * 512)), identification=101, **server),
        _ethernet_ipv4(_udp(40100, 10100, _data(1, b"short")), identification=102, **server),
    ]
    capture = tmp_path / "above-terminal.pcap"
    capture.write_bytes(_pcap(above_terminal))
    result = run_capture(capture, capture_id="SYN-TERMINAL-A")
    assert result.transfers[0].reconstruction_status == "CONFLICT"
    assert result.transfers[0].complete_payload_length is None
    assert all(event.layer != "APPLICATION" for event in result.events)

    # A terminal block may arrive before an earlier full block: filling the
    # hole below the terminal remains valid and is completed deterministically.
    fill_hole = [
        _ethernet_ipv4(_udp(10101, 69, _request(1, "fill.lui")), identification=103),
        _ethernet_ipv4(_udp(40101, 10101, _data(2, b"z")), identification=104, **server),
        _ethernet_ipv4(_udp(40101, 10101, _data(1, b"a" * 512)), identification=105, **server),
    ]
    capture = tmp_path / "fill-terminal-hole.pcap"
    capture.write_bytes(_pcap(fill_hole))
    result = run_capture(capture, capture_id="SYN-TERMINAL-B")
    assert result.transfers[0].reconstruction_status == "COMPLETE"
    assert result.transfers[0].terminal_block == 2
    assert result.transfers[0].complete_payload_length == 513

    # Completed observations do not consume active-session slots or retain
    # raw block allocations.  All eight are valid under one active slot.
    records: list[bytes] = []
    for index in range(8):
        client = 10200 + index
        tid = 40200 + index
        records.extend([
            _ethernet_ipv4(_udp(client, 69, _request(1, f"done-{index}.lui")), identification=110 + index * 2),
            _ethernet_ipv4(_udp(tid, client, _data(1, b"q" * 100)), identification=111 + index * 2, **server),
        ])
    capture = tmp_path / "completed-sessions.pcap"
    capture.write_bytes(_pcap(records))
    result = run_capture(
        capture,
        capture_id="SYN-TERMINAL-C",
        config=IntakeConfig(
            max_active_transfers=1,
            max_transfer_bytes=100,
            max_active_transfer_bytes=100,
            max_completed_payload_bytes=800,
        ),
    )
    assert [transfer.reconstruction_status for transfer in result.transfers] == ["COMPLETE"] * 8
    assert not any(item.code == "RESOURCE-ACTIVE-TRANSFER-LIMIT" for item in result.diagnostics)
    assert all(transfer.complete_payload is None for transfer in result.transfers)

    # Completed payload parsing has its own hard boundary rather than silently
    # accumulating raw transfer data after completion.
    capped = run_capture(
        capture,
        capture_id="SYN-TERMINAL-D",
        config=IntakeConfig(
            max_active_transfers=1,
            max_transfer_bytes=100,
            max_active_transfer_bytes=100,
            max_completed_payload_bytes=100,
        ),
    )
    assert capped.transfers[0].reconstruction_status == "COMPLETE"
    assert all("RESOURCE-COMPLETED-PAYLOAD-LIMIT" in item.diagnostics for item in capped.transfers[1:])

    def synthetic_udp(sequence: int, source_port: int, destination_port: int, payload: bytes) -> UdpDatagram:
        reference = PacketRef("cap-resident", sequence, sequence, 0, 1, len(payload), len(payload), Timestamp(sequence, 1))
        datagram = DatagramRecord(
            datagram_id=f"DG-{sequence:08d}", capture_id="cap-resident", interface_id=0,
            source="10.0.0.1" if destination_port == 69 else "10.0.0.2",
            destination="10.0.0.2" if destination_port == 69 else "10.0.0.1",
            protocol=17, identification=sequence, status="COMPLETE", failure_code=None,
            packet_refs=[reference], fragment_ranges=[(0, len(payload))], payload=payload,
        )
        return UdpDatagram(datagram, source_port, destination_port, payload, False)

    reconstructor = TftpReconstructor(
        capture_id="cap-resident", max_active_transfers=1, max_transfer_bytes=100,
        max_active_transfer_bytes=100, max_completed_payload_bytes=800,
    )
    for index in range(8):
        client, tid = 10400 + index, 40400 + index
        reconstructor.process(synthetic_udp(index * 2 + 1, client, 69, _request(1, f"state-{index}.lui")))
        reconstructor.process(synthetic_udp(index * 2 + 2, tid, client, _data(1, b"x" * 100)))
    usage = reconstructor.resource_usage
    assert usage["activeSessionCount"] == 0
    assert usage["activeRawPayloadBytes"] == 0
    assert usage["completedParsePayloadBytes"] == 800
    assert usage["retainedBlockDigestCount"] == 8


def test_tftp_option_evidence_and_rollover_are_not_guessed(tmp_path: Path) -> None:
    server = {"source": "10.0.0.2", "destination": "10.0.0.1"}
    too_large = [
        _ethernet_ipv4(_udp(10042, 69, _request(1, "bad.lui", {"blksize": "8"})), identification=89),
        _ethernet_ipv4(_udp(40043, 10042, _oack({"blksize": "1024"})), identification=90, **server),
        _ethernet_ipv4(_udp(40043, 10042, _data(1, b"x" * 700)), identification=91, **server),
    ]
    unknown = [
        _ethernet_ipv4(_udp(10043, 69, _request(1, "unknown.lui", {"blksize": "1024"})), identification=92),
        _ethernet_ipv4(_udp(40044, 10043, _data(2, b"x")), identification=93, **server),
    ]
    rollover = [
        _ethernet_ipv4(_udp(10044, 69, _request(1, "wrap.lui")), identification=94),
        _ethernet_ipv4(_udp(40045, 10044, _data(0, b"")), identification=95, **server),
    ]
    capture = tmp_path / "options-and-wrap.pcap"
    capture.write_bytes(_pcap(too_large + unknown + rollover))
    result = run_capture(capture, capture_id="SYN-22")
    invalid, missing, wrap = result.transfers
    assert invalid.reconstruction_status == "CONFLICT"
    assert missing.option_status == "UNKNOWN"
    assert missing.reconstruction_status == "GAPPED"
    assert wrap.reconstruction_status == "GAPPED"
    assert "UNSUPPORTED-TFTP-BLOCK-ROLLOVER" in wrap.diagnostics


def test_vlan_and_pcapng_section_contexts_do_not_cross_reassemble_or_transfer(tmp_path: Path) -> None:
    udp = _udp(10045, 69, _request(1, "vlan.lui"))
    first, second = udp[:16], udp[16:]
    vlan_capture = tmp_path / "vlan-fragments.pcap"
    vlan_capture.write_bytes(_pcap([
        _ethernet_ipv4(first, identification=96, more_fragments=True, vlan_tags=(1,)),
        _ethernet_ipv4(second, identification=96, offset_bytes=16, vlan_tags=(2,)),
    ]))
    vlan_result = run_capture(vlan_capture, capture_id="SYN-23")
    assert len(vlan_result.datagrams) == 2
    assert all(item.status == "GAPPED" for item in vlan_result.datagrams)

    request = _pcapng([_ethernet_ipv4(_udp(10046, 69, _request(1, "section.lui")), identification=97)])
    data = _pcapng([_ethernet_ipv4(
        _udp(40046, 10046, _data(1, b"x")), source="10.0.0.2", destination="10.0.0.1", identification=98,
    )])
    section_capture = tmp_path / "sections.pcapng"
    section_capture.write_bytes(request + data)
    section_result = run_capture(section_capture, capture_id="SYN-24")
    assert len(section_result.transfers) == 1
    assert section_result.transfers[0].reconstruction_status == "GAPPED"
    assert any(item.code == "UNASSOCIATED-TFTP-PACKET" for item in section_result.diagnostics)


def test_bounded_first_slice_roles_preserve_raw_contract_semantics() -> None:
    def header(suffix: bytes) -> bytes:
        return (6 + len(suffix)).to_bytes(4, "big") + b"A1" + suffix

    headers = {
        "LCI": header(b"\x00\x00\x00"),
        "LCL": header(b"\x00\x02"),
        "LCS": header(b"\x00\x01\x00\x02\x00\x03\xff\xff\x00"),
        "LUI": header(b"\x00\x00\x00"),
        "LUR": header(b"\x00\x02"),
        "LUS": header(b"\x00\x04\x00\x00\x01\x00\x02\xff\xff75%"),
    }
    parsed = {role: decode_first_slice_header(role, payload) for role, payload in headers.items()}
    assert all(item["parseStatus"] == "PARSED" for item in parsed.values())
    assert parsed["LCI"]["decodedFields"]["protocolVersion"] == "A1"
    assert parsed["LCS"]["decodedFields"]["exceptionTimer"]["present"] is True
    assert parsed["LCS"]["decodedFields"]["exceptionTimer"]["useConditionSatisfied"] is True
    assert parsed["LCS"]["decodedFields"]["estimatedTime"]["status"] == "NOT-PROVIDED"
    assert parsed["LUS"]["decodedFields"]["loadListRatio"]["rawAscii"] == "75%"


def test_truncated_nested_header_is_partial_and_never_emits_application_event(tmp_path: Path) -> None:
    # File length/version plus status and a declared five-byte description,
    # but no description bytes.  It is not a successful bounded decode.
    truncated_header = (20).to_bytes(4, "big") + b"A1" + b"\0\0\x05"
    assert decode_first_slice_header("LCI", truncated_header)["parseStatus"] == "PARTIAL"
    capture = tmp_path / "partial.lci.pcap"
    records = [
        _ethernet_ipv4(_udp(10050, 69, _request(1, "partial.lci")), identification=99),
        _ethernet_ipv4(
            _udp(40050, 10050, _data(1, truncated_header)),
            source="10.0.0.2", destination="10.0.0.1", identification=100,
        ),
    ]
    capture.write_bytes(_pcap(records))
    result = run_capture(capture, capture_id="SYN-25")
    assert any(event.fields.get("parseStatus") == "PARTIAL" for event in result.events)
    assert all(event.layer != "APPLICATION" for event in result.events)
    unknown_version = (9).to_bytes(4, "big") + b"B9" + b"\0\0\0"
    assert decode_first_slice_header("LUI", unknown_version)["parseStatus"] == "OPAQUE"


def test_pcapng_structural_errors_are_controlled_and_options_are_accepted(tmp_path: Path) -> None:
    malformed = tmp_path / "short-shb.pcapng"
    malformed.write_bytes(PCAPNG_SECTION_HEADER.to_bytes(4, "big") + struct.pack("<I", 12) + struct.pack("<I", 0x1A2B3C4D))
    output = tmp_path / "evidence.json"
    output.write_text("old evidence", encoding="utf-8")
    assert cli_main([
        "inspect", "--input", str(malformed), "--capture-id", "SYN-26", "--output", str(output),
        "--source-commit", "c" * 40,
    ]) == 1
    assert output.read_text(encoding="utf-8") == "old evidence"

    valid = tmp_path / "comment.pcapng"
    valid.write_bytes(_pcapng_with_epb_comment(_valid_exchange()[0]))
    result = run_capture(valid, capture_id="SYN-27")
    assert result.container_packet_count == 1
    assert result.packet_refs[0].captured_length == len(_valid_exchange()[0])


def test_capture_container_variants_and_unsafe_manifest_entries_are_rejected(tmp_path: Path) -> None:
    little = _pcap(_valid_exchange()[:1])
    big = b"\xa1\xb2\xc3\xd4" + struct.pack(">HHIIII", 2, 4, 0, 0, 65535, 1)
    packet = _valid_exchange()[0]
    big += struct.pack(">IIII", 1, 1, len(packet), len(packet)) + packet
    big_capture = tmp_path / "big.pcap"
    big_capture.write_bytes(big)
    result = run_capture(big_capture, capture_id="SYN-17")
    assert result.capture_metadata["byteOrder"] == "BIG"
    assert result.packet_refs[0].timestamp is not None
    assert result.packet_refs[0].timestamp.ticks_per_second == 1_000_000

    corpus = tmp_path / "corpus"
    corpus.mkdir()
    outside_relative_path = (tmp_path / "outside.pcapng").resolve().as_posix()
    manifest = {
        "manifestId": "CLTAV-HISTORICAL-CAPTURES", "manifestVersion": "1.0",
        "purpose": "EXPLORATORY-DEVELOPMENT-ONLY", "captureCount": 1,
        "truthBoundary": "not experimental truth",
        "captures": [{
            "captureId": "HC-01", "relativePath": outside_relative_path, "byteCount": 1, "sha256": "0" * 64,
            "observationQuality": "UNASSESSED-EXPLORATORY", "labelSource": "FILE-ANNOTATION-NONTRUTH", "rootCause": "UNKNOWN",
        }],
    }
    assert any("unsafe" in item for item in audit_manifest(manifest, corpus))


def test_pcapng_simple_packet_uses_snaplen_not_padding_and_invalid_lengths_stay_nonprojectable(tmp_path: Path) -> None:
    section_body = struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1)
    idb = struct.pack("<HHI", 1, 0, 5)
    simple = struct.pack("<I", 10) + b"abcde" + b"\0" * 3
    simple_capture = tmp_path / "simple.pcapng"
    simple_capture.write_bytes(_block(PCAPNG_SECTION_HEADER, section_body) + _block(1, idb) + _block(3, simple))
    packet = next(iter(CaptureReader(simple_capture, "cap-spb")))
    assert packet.ref.captured_length == 5
    assert packet.ref.original_length == 10
    assert packet.data == b"abcde"

    # SnapLen zero means no snap-length truncation; padding still never joins
    # the packet payload.  The same relation is endian-independent.
    zero_snap = tmp_path / "simple-zero-snap.pcapng"
    zero_snap.write_bytes(
        _block(PCAPNG_SECTION_HEADER, section_body)
        + _block(1, struct.pack("<HHI", 1, 0, 0))
        + _block(3, struct.pack("<I", 5) + b"abcde" + b"\0" * 3)
    )
    assert next(iter(CaptureReader(zero_snap, "cap-spb-zero"))).data == b"abcde"

    def big_block(block_type: int, body: bytes) -> bytes:
        total = 12 + len(body)
        assert total % 4 == 0
        return struct.pack(">II", block_type, total) + body + struct.pack(">I", total)

    big = tmp_path / "simple-big.pcapng"
    big.write_bytes(
        big_block(PCAPNG_SECTION_HEADER, struct.pack(">IHHq", 0x1A2B3C4D, 1, 0, -1))
        + big_block(1, struct.pack(">HHI", 1, 0, 5))
        + big_block(3, struct.pack(">I", 10) + b"abcde" + b"\0" * 3)
    )
    assert next(iter(CaptureReader(big, "cap-spb-big"))).data == b"abcde"

    for name, body in {
        "short": struct.pack("<I", 10) + b"abcd",
        "extra": struct.pack("<I", 10) + b"abcde" + b"\0" * 7,
    }.items():
        malformed = tmp_path / f"simple-{name}.pcapng"
        malformed.write_bytes(_block(PCAPNG_SECTION_HEADER, section_body) + _block(1, idb) + _block(3, body))
        with pytest.raises(CaptureFormatError) as caught:
            list(CaptureReader(malformed, f"cap-spb-{name}"))
        assert caught.value.code == "INVALID-PCAPNG-SIMPLE-LENGTH"

    invalid_pcap = tmp_path / "caplen-over-orig.pcap"
    invalid_pcap.write_bytes(
        b"\xd4\xc3\xb2\xa1" + struct.pack("<HHIIII", 2, 4, 0, 0, 65535, 1)
        + struct.pack("<IIII", 1, 0, 10, 5) + b"x" * 10
    )
    invalid_epb = tmp_path / "caplen-over-orig.pcapng"
    epb = struct.pack("<IIIII", 0, 0, 1, 10, 5) + b"y" * 10 + b"\0" * 2
    invalid_epb.write_bytes(_block(PCAPNG_SECTION_HEADER, section_body) + _block(1, struct.pack("<HHI", 1, 0, 65535)) + _block(6, epb))
    for capture, capture_id in ((invalid_pcap, "cap-invalid-pcap"), (invalid_epb, "cap-invalid-epb")):
        result = run_capture(capture, capture_id=capture_id)
        assert result.has_controlled_issue is True
        assert result.packet_refs[0].captured_length > result.packet_refs[0].original_length
        evidence = result.to_dict(source_commit="a" * 40)
        assert evidence_errors(evidence) == []
        assert not any(item["recordType"] == "PACKET-REF" for item in evidence["contractProjection"]["records"])
        assert any(
            item["sourceType"] == "PACKET-REF" and item["reason"] == "CAPLEN-EXCEEDS-ORIGLEN"
            for item in evidence["contractProjection"]["nonProjectable"]
        )


def test_nonzero_pcapng_time_offset_is_explicitly_nonprojectable(tmp_path: Path) -> None:
    record = _valid_exchange()[0]
    section_body = struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1)
    # if_tsoffset=7 seconds cannot be represented by the accepted PACKET-REF
    # payload, which has only raw ticks and resolution.
    idb = (
        struct.pack("<HHI", 1, 0, 65535)
        + struct.pack("<HHq", 14, 8, 7)
        + struct.pack("<HH", 0, 0)
    )
    padding = b"\0" * (-len(record) % 4)
    epb = struct.pack("<IIIII", 0, 0, 1, len(record), len(record)) + record + padding
    capture = tmp_path / "offset.pcapng"
    capture.write_bytes(_block(PCAPNG_SECTION_HEADER, section_body) + _block(1, idb) + _block(6, epb))
    evidence = run_capture(capture, capture_id="cap-time-offset").to_dict(source_commit="a" * 40)
    assert evidence_errors(evidence) == []
    assert not any(item["recordType"] == "PACKET-REF" for item in evidence["contractProjection"]["records"])
    assert any(
        item["sourceType"] == "PACKET-REF" and item["reason"] == "TIMESTAMP-OFFSET-NONPROJECTABLE"
        for item in evidence["contractProjection"]["nonProjectable"]
    )
    assert any(
        item["sourceType"] == "PROTOCOL-EVENT"
        and item["reason"] == "RAW-SOURCE-NONPROJECTABLE"
        for item in evidence["contractProjection"]["nonProjectable"]
    )


def test_reassembly_key_prevents_cross_interface_id_reuse_and_empty_datagram_is_complete(
    tmp_path: Path,
) -> None:
    def fragment(interface_id: int, offset: int, more: bool, payload: bytes, index: int) -> Ipv4Fragment:
        reference = PacketRef("SYN-18", index, index * 100, interface_id, 1, len(payload), len(payload), None)
        return Ipv4Fragment(reference, "10.0.0.1", "10.0.0.2", 77, 17, offset, more, payload)

    reassembler = Ipv4Reassembler()
    assert reassembler.add(fragment(0, 0, True, b"abcdefgh", 1)) == []
    assert reassembler.add(fragment(1, 8, False, b"ijkl", 2)) == []
    records = reassembler.finish()
    assert len(records) == 2
    assert all(record.status == "GAPPED" for record in records)

    empty = tmp_path / "empty-ipv4.pcap"
    empty.write_bytes(_pcap([_ethernet_ipv4(b"", identification=78)]))
    result = run_capture(empty, capture_id="SYN-18B")
    assert result.datagrams[0].status == "COMPLETE"
    assert result.datagrams[0].to_dict()["payloadLength"] == 0
    assert any(item.code == "TRUNCATED-UDP-HEADER" for item in result.diagnostics)


def test_manifest_resolved_identity_and_repeatability_are_enforced(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    first = corpus / "one.pcapng"
    first.write_bytes(_pcapng(_valid_exchange()))
    second = corpus / "two.pcapng"
    try:
        os.link(first, second)
    except OSError as exc:
        pytest.skip(f"hard-link fixture unavailable: {exc}")
    import hashlib
    digest = hashlib.sha256(first.read_bytes()).hexdigest()
    manifest = {
        "manifestId": "CLTAV-HISTORICAL-CAPTURES", "manifestVersion": "1.0",
        "purpose": "EXPLORATORY-DEVELOPMENT-ONLY", "captureCount": 2,
        "truthBoundary": "not experimental truth",
        "captures": [
            {"captureId": "HC-01", "relativePath": "one.pcapng", "byteCount": first.stat().st_size, "sha256": digest,
             "observationQuality": "UNASSESSED-EXPLORATORY", "labelSource": "FILE-ANNOTATION-NONTRUTH", "rootCause": "UNKNOWN"},
            {"captureId": "HC-02", "relativePath": "two.pcapng", "byteCount": second.stat().st_size, "sha256": digest,
             "observationQuality": "UNASSESSED-EXPLORATORY", "labelSource": "FILE-ANNOTATION-NONTRUTH", "rootCause": "UNKNOWN"},
        ],
    }
    assert any("identity is repeated" in item for item in audit_manifest(manifest, corpus))

    capture = tmp_path / "repeatable.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    first_result = run_capture(capture, capture_id="SYN-19").to_dict(source_commit="7" * 40)
    second_result = run_capture(capture, capture_id="SYN-19").to_dict(source_commit="7" * 40)
    assert first_result == second_result


def test_contract_projection_is_a_production_gate_with_complete_disposition(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mutating an emitted projection must fail the real CLI before replace."""
    capture = tmp_path / "contract-gate.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    evidence = run_capture(capture, capture_id="cap-contract-gate").to_dict(source_commit="a" * 40)
    assert evidence_errors(evidence) == []
    assert set(accepted_record_contracts()) >= {
        "PACKET-REF", "DATAGRAM-RECORD", "TRANSFER-RECORD", "PROTOCOL-EVENT",
    }

    bad_payload = deepcopy(evidence)
    packet = next(item for item in bad_payload["contractProjection"]["records"] if item["recordType"] == "PACKET-REF")
    packet["payload"] = {}
    assert any("RC-PACKET" in error for error in evidence_errors(bad_payload))

    bad_identity = deepcopy(evidence)
    bad_identity["contractProjection"]["contractIdentity"]["sha256"] = "0" * 64
    assert any("identity" in error for error in evidence_errors(bad_identity))

    bad_tool_identity = deepcopy(evidence)
    bad_tool_identity["tool"]["contractIdentities"][0]["sha256"] = "0" * 64
    assert any("tool contractIdentities" in error for error in evidence_errors(bad_tool_identity))

    missing_disposition = deepcopy(evidence)
    missing_disposition["contractProjection"]["records"] = [
        item for item in missing_disposition["contractProjection"]["records"]
        if item["recordType"] != "TRANSFER-RECORD"
    ]
    assert any("TRANSFER-RECORD" in error and ("omits" in error or "parentage" in error) for error in evidence_errors(missing_disposition))

    bad_packet_length = deepcopy(evidence)
    packet = next(item for item in bad_packet_length["contractProjection"]["records"] if item["recordType"] == "PACKET-REF")
    packet["payload"]["caplen"] = packet["payload"]["origlen"] + 1
    assert any("RC-PACKET-CAPLEN" in error for error in evidence_errors(bad_packet_length))

    bad_parentage = deepcopy(evidence)
    transfer = bad_parentage["transfers"][0]
    transfer["packetRefIds"] = []
    for event in bad_parentage["events"]:
        event["sourcePacketRefIds"] = []
    assert evidence_errors(bad_parentage)

    output = tmp_path / "protected.json"
    output.write_text("old projection", encoding="utf-8")
    original = pipeline_module.IntakeResult.to_dict

    def malformed_projection(self: IntakeResult, *, source_commit: str) -> dict[str, object]:
        rendered = original(self, source_commit=source_commit)
        projected = next(item for item in rendered["contractProjection"]["records"] if item["recordType"] == "PACKET-REF")
        projected["payload"] = {}
        return rendered

    monkeypatch.setattr(pipeline_module.IntakeResult, "to_dict", malformed_projection)
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", "cap-contract-gate", "--output", str(output),
        "--source-commit", "a" * 40,
    ]) == 1
    assert output.read_text(encoding="utf-8") == "old projection"


def test_transfer_projection_requires_exact_role_witness_and_keeps_request_only_evidence(
    tmp_path: Path,
) -> None:
    capture = tmp_path / "transfer-witness.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    evidence = run_capture(capture, capture_id="cap-transfer-witness").to_dict(source_commit="a" * 40)
    assert evidence_errors(evidence) == []
    packet_refs = {
        item["sourceId"]: item["payload"]
        for item in evidence["contractProjection"]["records"]
        if item["recordType"] == "PACKET-REF"
    }
    request_event = next(
        item for item in evidence["contractProjection"]["records"]
        if item["recordType"] == "PROTOCOL-EVENT" and item["sourceId"].startswith("event-request-")
    )
    transfer = next(
        item for item in evidence["contractProjection"]["records"]
        if item["recordType"] == "TRANSFER-RECORD"
    )
    request_ref = request_event["payload"]["rawRefs"][0]
    other_ref = next(value for value in packet_refs.values() if value != request_ref)

    wrong_request = deepcopy(evidence)
    request = next(
        item for item in wrong_request["contractProjection"]["records"]
        if item["sourceId"] == request_event["sourceId"]
    )
    request["payload"]["rawRefs"] = [other_ref]
    assert evidence_errors(wrong_request)

    wrong_block = deepcopy(evidence)
    projected = next(
        item for item in wrong_block["contractProjection"]["records"]
        if item["sourceId"] == transfer["sourceId"]
    )
    projected["payload"]["blockMap"] = {"1": request_ref}
    assert any("TRANSFER-RECORD" in error for error in evidence_errors(wrong_block))

    # An observed RRQ is still a normal WIRE record when no server TID/DATA
    # evidence exists.  Only the TRANSFER-RECORD claim is non-projectable.
    request_only = tmp_path / "request-only.pcap"
    request_only.write_bytes(_pcap([_ethernet_ipv4(_udp(10000, 69, _request(1, "only.lui")))]))
    partial = run_capture(request_only, capture_id="cap-request-only").to_dict(source_commit="a" * 40)
    assert evidence_errors(partial) == []
    assert any(
        item["recordType"] == "PROTOCOL-EVENT" and item["sourceId"].startswith("event-request-")
        for item in partial["contractProjection"]["records"]
    )
    assert any(
        item == {
            "sourceType": "TRANSFER-RECORD",
            "sourceId": partial["transfers"][0]["transferId"],
            "reason": "TID-OR-BLOCK-SOURCE-NONPROJECTABLE",
        }
        for item in partial["contractProjection"]["nonProjectable"]
    )


def test_same_direction_data_cannot_substitute_another_block_source(tmp_path: Path) -> None:
    """A complete transfer's block labels need independent source-role proof."""
    server = {"source": "10.0.0.2", "destination": "10.0.0.1"}
    capture = tmp_path / "same-direction-blocks.pcap"
    capture.write_bytes(_pcap([
        _ethernet_ipv4(_udp(10300, 69, _request(1, "blocks.lui")), identification=850),
        _ethernet_ipv4(_udp(40300, 10300, _data(1, b"a" * 512)), identification=851, **server),
        _ethernet_ipv4(_udp(40300, 10300, _data(2, b"z")), identification=852, **server),
    ]))
    baseline = run_capture(capture, capture_id="cap-same-direction-blocks").to_dict(source_commit="a" * 40)
    assert evidence_errors(baseline) == []
    mutated = deepcopy(baseline)
    transfer = mutated["transfers"][0]
    witness = transfer["sourceWitness"]
    assert isinstance(witness, dict)
    first_packet, second_packet = witness["blockPacketRefIds"]["1"], witness["blockPacketRefIds"]["2"]
    first_datagram, second_datagram = witness["blockDatagramIds"]["1"], witness["blockDatagramIds"]["2"]
    # Both packets are server-to-client and both follow the request.  A
    # direction/order-only validator would accept this coordinated swap even
    # though DATA(1) and DATA(2) now substantiate the wrong block labels.
    witness["blockPacketRefIds"] = {"1": second_packet, "2": first_packet}
    witness["blockDatagramIds"] = {"1": second_datagram, "2": first_datagram}
    witness["completionPacketRefId"] = first_packet
    witness["completionDatagramId"] = first_datagram
    projection = mutated["contractProjection"]
    packet_contract_ids = {
        item["packetRefId"]: (
            f"{item['captureId']}:{item['sectionId']}:{item['interfaceId']}:{item['packetIndex']}"
        )
        for item in mutated["packetRefs"]
    }
    projected = next(
        item for item in projection["records"]
        if item["recordType"] == "TRANSFER-RECORD" and item["sourceId"] == transfer["transferId"]
    )
    projected["payload"]["blockMap"] = {
        "1": packet_contract_ids[second_packet], "2": packet_contract_ids[first_packet],
    }
    projected["payload"]["completionEvidence"] = [f"pkt-{packet_contract_ids[first_packet]}"]
    assert evidence_errors(mutated)


def test_provenance_mutations_fail_real_inspect_and_corpus_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A shape-valid projection mutation must not replace a prior publication."""
    capture = tmp_path / "provenance.pcap"
    server = {"source": "10.0.0.2", "destination": "10.0.0.1"}
    capture.write_bytes(_pcap([
        _ethernet_ipv4(_udp(10400, 69, _request(1, "provenance.lui")), identification=860),
        _ethernet_ipv4(_udp(40400, 10400, _data(1, b"a" * 512)), identification=861, **server),
        _ethernet_ipv4(_udp(40400, 10400, _data(2, b"z")), identification=862, **server),
    ]))
    original = pipeline_module.IntakeResult.to_dict

    def transfer_rows(rendered: dict[str, object]) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
        projection = rendered["contractProjection"]
        assert isinstance(projection, dict)
        records = projection["records"]
        assert isinstance(records, list)
        transfer = next(item for item in rendered["transfers"] if isinstance(item, dict))
        projected = next(item for item in records if item["recordType"] == "TRANSFER-RECORD")
        request = next(
            item for item in records
            if item["recordType"] == "PROTOCOL-EVENT" and str(item["sourceId"]).startswith("event-request-")
        )
        assert isinstance(transfer, dict) and isinstance(projected, dict) and isinstance(request, dict)
        return transfer, projected, request

    def packet_contract_refs(rendered: dict[str, object]) -> dict[str, str]:
        rows = rendered["packetRefs"]
        assert isinstance(rows, list)
        return {
            item["packetRefId"]: (
                f"{item['captureId']}:{item['sectionId']}:{item['interfaceId']}:{item['packetIndex']}"
            )
            for item in rows
            if isinstance(item, dict)
        }

    def clear_block_and_completion(rendered: dict[str, object]) -> None:
        transfer, projected, _request = transfer_rows(rendered)
        witness = transfer["sourceWitness"]
        assert isinstance(witness, dict)
        witness["blockPacketRefIds"] = {}
        witness["blockDatagramIds"] = {}
        witness["completionPacketRefId"] = None
        witness["completionDatagramId"] = None
        payload = projected["payload"]
        assert isinstance(payload, dict)
        payload["blockMap"] = {}
        payload["completionEvidence"] = []

    def swap_request_source(rendered: dict[str, object]) -> None:
        transfer, _projected, request = transfer_rows(rendered)
        witness = transfer["sourceWitness"]
        assert isinstance(witness, dict)
        replacement = next(iter(witness["blockPacketRefIds"].values()))
        replacement_datagram = next(iter(witness["blockDatagramIds"].values()))
        witness["requestPacketRefId"] = replacement
        witness["requestDatagramId"] = replacement_datagram
        projection = rendered["contractProjection"]
        assert isinstance(projection, dict)
        ref_by_source = packet_contract_refs(rendered)
        payload = request["payload"]
        assert isinstance(payload, dict)
        payload["rawRefs"] = [ref_by_source[replacement]]

    def swap_completion_source(rendered: dict[str, object]) -> None:
        transfer, projected, _request = transfer_rows(rendered)
        witness = transfer["sourceWitness"]
        assert isinstance(witness, dict)
        request_packet = witness["requestPacketRefId"]
        request_datagram = witness["requestDatagramId"]
        assert isinstance(request_packet, str) and isinstance(request_datagram, str)
        witness["blockPacketRefIds"] = {"1": request_packet}
        witness["blockDatagramIds"] = {"1": request_datagram}
        witness["completionPacketRefId"] = request_packet
        witness["completionDatagramId"] = request_datagram
        projection = rendered["contractProjection"]
        assert isinstance(projection, dict)
        ref_by_source = packet_contract_refs(rendered)
        payload = projected["payload"]
        assert isinstance(payload, dict)
        payload["completionEvidence"] = [f"pkt-{ref_by_source[request_packet]}"]

    def swap_same_direction_data_blocks(rendered: dict[str, object]) -> None:
        """Coordinate every visible transfer/projection field for a role swap."""
        transfer, projected, _request = transfer_rows(rendered)
        witness = transfer["sourceWitness"]
        assert isinstance(witness, dict)
        first_packet, second_packet = (
            witness["blockPacketRefIds"]["1"], witness["blockPacketRefIds"]["2"],
        )
        first_datagram, second_datagram = (
            witness["blockDatagramIds"]["1"], witness["blockDatagramIds"]["2"],
        )
        witness["blockPacketRefIds"] = {"1": second_packet, "2": first_packet}
        witness["blockDatagramIds"] = {"1": second_datagram, "2": first_datagram}
        witness["completionPacketRefId"] = first_packet
        witness["completionDatagramId"] = first_datagram
        ref_by_source = packet_contract_refs(rendered)
        payload = projected["payload"]
        assert isinstance(payload, dict)
        payload["blockMap"] = {
            "1": ref_by_source[second_packet], "2": ref_by_source[first_packet],
        }
        payload["completionEvidence"] = [f"pkt-{ref_by_source[first_packet]}"]

    def prune_to_request(rendered: dict[str, object]) -> None:
        transfer, _projected, _request = transfer_rows(rendered)
        witness = transfer["sourceWitness"]
        assert isinstance(witness, dict)
        request_packet = witness["requestPacketRefId"]
        first_datagram = transfer["datagramIds"][0]
        transfer["packetRefIds"] = [request_packet]
        transfer["datagramIds"] = [first_datagram]
        witness["packetRefIds"] = [request_packet]
        witness["datagramIds"] = [first_datagram]
        witness["blockPacketRefIds"] = {}
        witness["blockDatagramIds"] = {}
        witness["completionPacketRefId"] = None
        witness["completionDatagramId"] = None
        for event in rendered["events"]:
            event["sourcePacketRefIds"] = [request_packet]
            event["sourceDatagramIds"] = [first_datagram]

    def clear_datagram_ancestry(rendered: dict[str, object]) -> None:
        transfer, _projected, _request = transfer_rows(rendered)
        witness = transfer["sourceWitness"]
        assert isinstance(witness, dict)
        transfer["datagramIds"] = []
        witness["datagramIds"] = []
        for event in rendered["events"]:
            event["sourceDatagramIds"] = []

    mutations = [
        clear_block_and_completion,
        swap_request_source,
        swap_completion_source,
        swap_same_direction_data_blocks,
        prune_to_request,
        clear_datagram_ancestry,
    ]
    # Each historical semantic attack must fail the library entry point first;
    # the CLI/corpus loops below then prove the same gate is not presentation
    # only.  The mutations update every relevant public witness/projection
    # field, rather than relying on a superficial stale-reference failure.
    baseline = run_capture(capture, capture_id="cap-provenance").to_dict(source_commit="a" * 40)
    for mutate in mutations:
        candidate = deepcopy(baseline)
        mutate(candidate)
        assert evidence_errors(candidate)
    for index, mutate in enumerate(mutations):
        def mutated(self: IntakeResult, *, source_commit: str, _mutate=mutate) -> dict[str, object]:
            rendered = original(self, source_commit=source_commit)
            _mutate(rendered)
            return rendered

        monkeypatch.setattr(pipeline_module.IntakeResult, "to_dict", mutated)
        output = tmp_path / f"inspect-{index}.json"
        output.write_text("prior publication", encoding="utf-8")
        assert cli_main([
            "inspect", "--input", str(capture), "--capture-id", "cap-provenance", "--output", str(output),
            "--source-commit", "a" * 40,
        ]) == 1
        assert output.read_text(encoding="utf-8") == "prior publication"

    # The same semantic closure is a corpus transaction gate, rather than an
    # inspect-only guard.  Exercise all five mutations through the publishing
    # transaction, preserving the requirement that no failed stage appears.
    corpus_root = tmp_path / "corpus"
    corpus_root.mkdir()
    corpus_capture = corpus_root / "one.pcapng"
    corpus_capture.write_bytes(capture.read_bytes())
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_corpus_manifest(corpus_root)), encoding="utf-8")
    for index, mutate in enumerate(mutations):
        def mutated(self: IntakeResult, *, source_commit: str, _mutate=mutate) -> dict[str, object]:
            rendered = original(self, source_commit=source_commit)
            _mutate(rendered)
            return rendered

        monkeypatch.setattr(pipeline_module.IntakeResult, "to_dict", mutated)
        output_dir = tmp_path / f"corpus-output-{index}"
        with pytest.raises(IntakeError) as caught:
            run_corpus(
                manifest_path=manifest_path, corpus_root=corpus_root, output_dir=output_dir,
                config=IntakeConfig(), source_commit="a" * 40,
            )
        assert caught.value.code == "EVIDENCE-SCHEMA-ERROR"
        assert not output_dir.exists()


def test_declared_file_length_mismatch_stays_a_controlled_parse_failure(tmp_path: Path) -> None:
    payload = (99).to_bytes(4, "big") + b"A1" + b"\0\0\0"
    capture = tmp_path / "declared-length.pcap"
    capture.write_bytes(_pcap([
        _ethernet_ipv4(_udp(10000, 69, _request(1, "length.lui")), identification=201),
        _ethernet_ipv4(
            _udp(40000, 10000, _data(1, payload)),
            source="10.0.0.2", destination="10.0.0.1", identification=202,
        ),
        _ethernet_ipv4(_udp(10000, 40000, _ack(1)), identification=203),
    ]))
    result = run_capture(capture, capture_id="cap-declared-length")
    header = next(item for item in result.events if item.event_type == "FIRST-SLICE-FILE-HEADER")
    assert header.fields["parseStatus"] == "MALFORMED"
    assert header.fields["reason"] == "DECLARED-FILE-LENGTH-MISMATCH"
    assert header.fields["decodedFields"]["declaredFileLength"] == 99
    assert header.fields["decodedFields"]["observedFileLength"] == len(payload)
    assert not any(item.layer == "APPLICATION" for item in result.events)
    assert evidence_errors(result.to_dict(source_commit="a" * 40)) == []


@pytest.mark.parametrize("opcode", [1, 2])
def test_request_only_rrq_and_wrq_publish_controlled_evidence_through_cli(
    tmp_path: Path, opcode: int,
) -> None:
    capture = tmp_path / f"request-{opcode}.pcap"
    capture.write_bytes(_pcap([
        _ethernet_ipv4(_udp(10000, 69, _request(opcode, "only.lui")), identification=270 + opcode),
    ]))
    output = tmp_path / f"request-{opcode}.json"
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", f"cap-request-{opcode}",
        "--output", str(output), "--source-commit", "a" * 40,
    ]) == 2
    rendered = json.loads(output.read_text(encoding="utf-8"))
    assert rendered["executionStatus"] == "COMPLETE-WITH-CONTROLLED-ISSUES"
    assert evidence_errors(rendered) == []
    assert any(item["sourceId"].startswith("event-request-") for item in rendered["contractProjection"]["records"])
    assert any(item["reason"] == "TID-OR-BLOCK-SOURCE-NONPROJECTABLE" for item in rendered["contractProjection"]["nonProjectable"])


@pytest.mark.parametrize("opcode", [1, 2])
def test_request_only_capture_stays_a_controlled_corpus_row(tmp_path: Path, opcode: int) -> None:
    corpus_root = tmp_path / "request-only-corpus"
    corpus_root.mkdir()
    capture = corpus_root / "one.pcapng"
    capture.write_bytes(_pcap([
        _ethernet_ipv4(_udp(10000, 69, _request(opcode, "only.lui")), identification=280 + opcode),
    ]))
    manifest_path = tmp_path / "request-only-manifest.json"
    manifest_path.write_text(json.dumps(_corpus_manifest(corpus_root)), encoding="utf-8")
    output_dir = tmp_path / "request-only-output"
    summary = run_corpus(
        manifest_path=manifest_path, corpus_root=corpus_root, output_dir=output_dir,
        config=IntakeConfig(), source_commit="a" * 40,
    )
    assert summary["captures"][0]["executionStatus"] == "COMPLETE-WITH-CONTROLLED-ISSUES"
    assert evidence_errors(json.loads((output_dir / "HC-01.json").read_text(encoding="utf-8"))) == []


@pytest.mark.parametrize("role", ["LCI", "LCL", "LCS", "LUI", "LUR", "LUS"])
@pytest.mark.parametrize("direction", ["too-small", "too-large"])
def test_all_supported_role_length_contradictions_are_controlled_through_cli(
    tmp_path: Path, role: str, direction: str,
) -> None:
    normal = _role_header(role)
    declared = len(normal) - 1 if direction == "too-small" else len(normal) + 1000
    payload = _role_header(role, declared)
    capture = tmp_path / f"{role}-{direction}.pcap"
    capture.write_bytes(_pcap([
        _ethernet_ipv4(_udp(10000, 69, _request(1, f"sample.{role.lower()}")), identification=310),
        _ethernet_ipv4(
            _udp(40000, 10000, _data(1, payload)),
            source="10.0.0.2", destination="10.0.0.1", identification=311,
        ),
        _ethernet_ipv4(_udp(10000, 40000, _ack(1)), identification=312),
    ]))
    output = tmp_path / f"{role}-{direction}.json"
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", f"cap-{role.lower()}-{direction}",
        "--output", str(output), "--source-commit", "a" * 40,
    ]) == 2
    rendered = json.loads(output.read_text(encoding="utf-8"))
    assert rendered["executionStatus"] == "COMPLETE-WITH-CONTROLLED-ISSUES"
    assert any(
        event["layer"] == "PARSE-RESULT"
        and event["fields"].get("reason") == "DECLARED-FILE-LENGTH-MISMATCH"
        for event in rendered["events"]
    )
    assert not any(event["layer"] == "APPLICATION" for event in rendered["events"])
    assert evidence_errors(rendered) == []


@pytest.mark.parametrize("role", ["LCI", "LCL", "LCS", "LUI", "LUR", "LUS"])
def test_all_supported_role_normal_lengths_remain_clean(role: str) -> None:
    decoded = decode_first_slice_header(role, _role_header(role))
    assert decoded["parseStatus"] == "PARSED"
    assert decoded["decodedFields"]["declaredFileLength"] == decoded["decodedFields"]["observedFileLength"]


@pytest.mark.parametrize("role", ["LCI", "LCL", "LCS", "LUI", "LUR", "LUS"])
def test_all_supported_role_normal_lengths_publish_application_evidence_through_cli(
    tmp_path: Path, role: str,
) -> None:
    """The twelve contradiction cases retain one real clean control per role."""
    capture = tmp_path / f"{role}-normal.pcap"
    capture.write_bytes(_pcap([
        _ethernet_ipv4(_udp(10000, 69, _request(1, f"sample.{role.lower()}")), identification=330),
        _ethernet_ipv4(
            _udp(40000, 10000, _data(1, _role_header(role))),
            source="10.0.0.2", destination="10.0.0.1", identification=331,
        ),
        _ethernet_ipv4(_udp(10000, 40000, _ack(1)), identification=332),
    ]))
    output = tmp_path / f"{role}-normal.json"
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", f"cap-{role.lower()}-normal",
        "--output", str(output), "--source-commit", "a" * 40,
    ]) == 0
    rendered = json.loads(output.read_text(encoding="utf-8"))
    assert rendered["executionStatus"] == "COMPLETE"
    assert any(event["layer"] == "APPLICATION" for event in rendered["events"])
    assert evidence_errors(rendered) == []


def test_file_length_matrix_remains_controlled_through_corpus_publication(tmp_path: Path) -> None:
    """Every supported role/direction is a real corpus-row quality witness."""
    corpus_root = tmp_path / "length-matrix-corpus"
    corpus_root.mkdir()
    captures: list[dict[str, object]] = []
    cases: list[tuple[str, str, str]] = []
    for index, (role, direction) in enumerate(
        (role, direction)
        for role in ("LCI", "LCL", "LCS", "LUI", "LUR", "LUS")
        for direction in ("too-small", "too-large")
    ):
        normal = _role_header(role)
        declared = len(normal) - 1 if direction == "too-small" else len(normal) + 1000
        capture = corpus_root / f"case-{index:02d}.pcap"
        capture.write_bytes(_pcap([
            _ethernet_ipv4(_udp(10000, 69, _request(1, f"sample.{role.lower()}")), identification=350 + index * 3),
            _ethernet_ipv4(
                _udp(40000, 10000, _data(1, _role_header(role, declared))),
                source="10.0.0.2", destination="10.0.0.1", identification=351 + index * 3,
            ),
            _ethernet_ipv4(_udp(10000, 40000, _ack(1)), identification=352 + index * 3),
        ]))
        capture_id = f"HC-{index + 1:02d}"
        captures.append({
            "captureId": capture_id,
            "relativePath": capture.name,
            "byteCount": capture.stat().st_size,
            "sha256": hashlib.sha256(capture.read_bytes()).hexdigest(),
            "observationQuality": "UNASSESSED-EXPLORATORY",
            "labelSource": "FILE-ANNOTATION-NONTRUTH",
            "rootCause": "UNKNOWN",
        })
        cases.append((capture_id, role, direction))
    manifest = {
        "manifestId": "CLTAV-HISTORICAL-CAPTURES",
        "manifestVersion": "1.0",
        "purpose": "EXPLORATORY-DEVELOPMENT-ONLY",
        "captureCount": len(captures),
        "truthBoundary": "not experimental truth",
        "captures": captures,
    }
    manifest_path = tmp_path / "length-matrix-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    output_dir = tmp_path / "length-matrix-output"
    summary = run_corpus(
        manifest_path=manifest_path, corpus_root=corpus_root, output_dir=output_dir,
        config=IntakeConfig(), source_commit="a" * 40,
    )
    assert {item["captureId"] for item in summary["captures"]} == {case[0] for case in cases}
    assert {item["executionStatus"] for item in summary["captures"]} == {"COMPLETE-WITH-CONTROLLED-ISSUES"}
    for capture_id, _role, _direction in cases:
        rendered = json.loads((output_dir / f"{capture_id}.json").read_text(encoding="utf-8"))
        assert any(
            event["layer"] == "PARSE-RESULT"
            and event["fields"].get("reason") == "DECLARED-FILE-LENGTH-MISMATCH"
            for event in rendered["events"]
        )
        assert not any(event["layer"] == "APPLICATION" for event in rendered["events"])
        assert evidence_errors(rendered) == []


def test_contradictory_file_length_cannot_be_relabelled_complete_for_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = _role_header("LUI", 1000)
    capture = tmp_path / "forced-complete.pcap"
    capture.write_bytes(_pcap([
        _ethernet_ipv4(_udp(10000, 69, _request(1, "forced.lui")), identification=320),
        _ethernet_ipv4(_udp(40000, 10000, _data(1, payload)), source="10.0.0.2", destination="10.0.0.1", identification=321),
        _ethernet_ipv4(_udp(10000, 40000, _ack(1)), identification=322),
    ]))
    output = tmp_path / "forced-complete.json"
    output.write_text("prior quality output", encoding="utf-8")
    original = pipeline_module.IntakeResult.to_dict

    def falsely_clean(self: IntakeResult, *, source_commit: str) -> dict[str, object]:
        rendered = original(self, source_commit=source_commit)
        rendered["executionStatus"] = "COMPLETE"
        header = next(
            item for item in rendered["events"]
            if item["eventType"] == "FIRST-SLICE-FILE-HEADER"
        )
        header["fields"] = {
            "parseStatus": "PARSED",
            "decodedFields": {},
            "unparsedRemainderBytes": 0,
            "codecScope": "BOUNDED-FIRST-SLICE-HEADER-ONLY",
        }
        for item in rendered["contractProjection"]["records"]:
            if item["recordType"] == "PROTOCOL-EVENT" and item["sourceId"] == header["eventId"]:
                item["payload"]["parseBoundary"] = "COMPLETE"
        return rendered

    monkeypatch.setattr(pipeline_module.IntakeResult, "to_dict", falsely_clean)
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", "cap-forced-complete", "--output", str(output),
        "--source-commit", "a" * 40,
    ]) == 1
    assert output.read_text(encoding="utf-8") == "prior quality output"


def test_capture_versions_snaplen_and_shb_options_are_checked(tmp_path: Path) -> None:
    packet = b"x" * 10
    bad_pcap_version = tmp_path / "pcap-version.pcap"
    bad_pcap_version.write_bytes(
        b"\xd4\xc3\xb2\xa1" + struct.pack("<HHIIII", 9, 9, 0, 0, 65535, 1)
    )
    with pytest.raises(CaptureFormatError, match="supported 2.4 profile") as caught:
        list(CaptureReader(bad_pcap_version, "cap-pcap-version"))
    assert caught.value.code == "UNSUPPORTED-PCAP-VERSION"

    snap_pcap = tmp_path / "pcap-snaplen.pcap"
    snap_pcap.write_bytes(
        b"\xd4\xc3\xb2\xa1" + struct.pack("<HHIIII", 2, 4, 0, 0, 5, 1)
        + struct.pack("<IIII", 1, 0, len(packet), len(packet)) + packet
    )
    pcap_result = run_capture(snap_pcap, capture_id="cap-pcap-snap")
    assert "CAPLEN-EXCEEDS-SNAPLEN" in pcap_result.packet_refs[0].quality_codes
    pcap_evidence = pcap_result.to_dict(source_commit="a" * 40)
    assert evidence_errors(pcap_evidence) == []
    assert any(item["reason"] == "CAPLEN-EXCEEDS-SNAPLEN" for item in pcap_evidence["contractProjection"]["nonProjectable"])

    big_snap_pcap = tmp_path / "pcap-snaplen-big.pcap"
    big_snap_pcap.write_bytes(
        b"\xa1\xb2\xc3\xd4" + struct.pack(">HHIIII", 2, 4, 0, 0, 5, 1)
        + struct.pack(">IIII", 1, 0, len(packet), len(packet)) + packet
    )
    assert "CAPLEN-EXCEEDS-SNAPLEN" in run_capture(
        big_snap_pcap, capture_id="cap-pcap-snap-big",
    ).packet_refs[0].quality_codes

    shb = struct.pack("<IHHq", 0x1A2B3C4D, 1, 2, -1)
    idb = struct.pack("<HHI", 1, 0, 5)
    epb = struct.pack("<IIIII", 0, 0, 1, len(packet), len(packet)) + packet + b"\0" * 2
    snap_pcapng = tmp_path / "pcapng-snaplen.pcapng"
    snap_pcapng.write_bytes(_block(PCAPNG_SECTION_HEADER, shb) + _block(1, idb) + _block(6, epb))
    pcapng_result = run_capture(snap_pcapng, capture_id="cap-pcapng-snap")
    assert "CAPLEN-EXCEEDS-SNAPLEN" in pcapng_result.packet_refs[0].quality_codes

    def big_block(block_type: int, body: bytes) -> bytes:
        total = 12 + len(body)
        assert total % 4 == 0
        return struct.pack(">II", block_type, total) + body + struct.pack(">I", total)

    big_snap_pcapng = tmp_path / "pcapng-snaplen-big.pcapng"
    big_shb = struct.pack(">IHHq", 0x1A2B3C4D, 1, 2, -1)
    big_epb = struct.pack(">IIIII", 0, 0, 1, len(packet), len(packet)) + packet + b"\0" * 2
    big_snap_pcapng.write_bytes(big_block(PCAPNG_SECTION_HEADER, big_shb) + big_block(1, struct.pack(">HHI", 1, 0, 5)) + big_block(6, big_epb))
    assert "CAPLEN-EXCEEDS-SNAPLEN" in run_capture(
        big_snap_pcapng, capture_id="cap-pcapng-snap-big",
    ).packet_refs[0].quality_codes

    compatible = tmp_path / "pcapng-12-compatible.pcapng"
    compatible_epb = struct.pack("<IIIII", 0, 0, 1, len(packet), len(packet)) + packet + b"\0" * 2
    compatible.write_bytes(
        _block(PCAPNG_SECTION_HEADER, struct.pack("<IHHq", 0x1A2B3C4D, 1, 2, -1))
        + _block(1, struct.pack("<HHI", 1, 0, 0)) + _block(6, compatible_epb)
    )
    compatible_packets = list(CaptureReader(compatible, "cap-pcapng-12"))
    assert len(compatible_packets) == 1
    assert compatible_packets[0].ref.capture_snap_length == 0
    assert compatible_packets[0].ref.quality_codes == ()

    unsupported = tmp_path / "pcapng-version.pcapng"
    unsupported.write_bytes(_block(PCAPNG_SECTION_HEADER, struct.pack("<IHHq", 0x1A2B3C4D, 99, 99, -1)))
    with pytest.raises(CaptureFormatError) as caught:
        list(CaptureReader(unsupported, "cap-pcapng-version"))
    assert caught.value.code == "UNSUPPORTED-PCAPNG-VERSION"

    invalid_options = tmp_path / "pcapng-shb-options.pcapng"
    invalid_shb = struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1) + struct.pack("<HH", 0, 1)
    invalid_options.write_bytes(_block(PCAPNG_SECTION_HEADER, invalid_shb))
    with pytest.raises(CaptureFormatError) as caught:
        list(CaptureReader(invalid_options, "cap-pcapng-options"))
    assert caught.value.code == "INVALID-PCAPNG-OPTION"

    legal_options = tmp_path / "pcapng-shb-unknown-options.pcapng"
    legal_shb = (
        struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1)
        + struct.pack("<HH", 0x00FF, 3) + b"abc\0" + struct.pack("<HH", 0, 0)
    )
    legal_options.write_bytes(_block(PCAPNG_SECTION_HEADER, legal_shb))
    assert list(CaptureReader(legal_options, "cap-pcapng-unknown-options")) == []


def test_snaplen_quality_is_published_through_cli_and_corpus(tmp_path: Path) -> None:
    """Container quality is not merely a reader-local observation."""
    packet = b"x" * 10
    pcap = tmp_path / "snaplen-cli.pcap"
    pcap.write_bytes(
        b"\xd4\xc3\xb2\xa1" + struct.pack("<HHIIII", 2, 4, 0, 0, 5, 1)
        + struct.pack("<IIII", 1, 0, len(packet), len(packet)) + packet
    )
    cli_output = tmp_path / "snaplen-cli.json"
    assert cli_main([
        "inspect", "--input", str(pcap), "--capture-id", "cap-snaplen-cli",
        "--output", str(cli_output), "--source-commit", "a" * 40,
    ]) == 2
    cli_evidence = json.loads(cli_output.read_text(encoding="utf-8"))
    assert cli_evidence["packetRefs"][0]["captureSnapLength"] == 5
    assert "CAPLEN-EXCEEDS-SNAPLEN" in cli_evidence["packetRefs"][0]["qualityCodes"]
    assert any(item["reason"] == "CAPLEN-EXCEEDS-SNAPLEN" for item in cli_evidence["contractProjection"]["nonProjectable"])
    assert evidence_errors(cli_evidence) == []

    shb = struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1)
    idb = struct.pack("<HHI", 1, 0, 5)
    epb = struct.pack("<IIIII", 0, 0, 1, len(packet), len(packet)) + packet + b"\0" * 2
    corpus_root = tmp_path / "snaplen-corpus"
    corpus_root.mkdir()
    corpus_capture = corpus_root / "one.pcapng"
    corpus_capture.write_bytes(_block(PCAPNG_SECTION_HEADER, shb) + _block(1, idb) + _block(6, epb))
    manifest_path = tmp_path / "snaplen-manifest.json"
    manifest_path.write_text(json.dumps(_corpus_manifest(corpus_root)), encoding="utf-8")
    output_dir = tmp_path / "snaplen-corpus-output"
    summary = run_corpus(
        manifest_path=manifest_path, corpus_root=corpus_root, output_dir=output_dir,
        config=IntakeConfig(), source_commit="a" * 40,
    )
    assert summary["captures"][0]["executionStatus"] == "COMPLETE-WITH-CONTROLLED-ISSUES"
    corpus_evidence = json.loads((output_dir / "HC-01.json").read_text(encoding="utf-8"))
    assert corpus_evidence["packetRefs"][0]["captureSnapLength"] == 5
    assert "CAPLEN-EXCEEDS-SNAPLEN" in corpus_evidence["packetRefs"][0]["qualityCodes"]
    assert evidence_errors(corpus_evidence) == []


def test_snaplen_quality_cannot_be_erased_from_container_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A clean-looking packet cannot replace a snaplen-bounded source fact."""
    packet = b"x" * 10
    capture = tmp_path / "snaplen-erasure.pcap"
    capture.write_bytes(
        b"\xd4\xc3\xb2\xa1" + struct.pack("<HHIIII", 2, 4, 0, 0, 5, 1)
        + struct.pack("<IIII", 1, 0, len(packet), len(packet)) + packet
    )
    baseline = run_capture(capture, capture_id="cap-snaplen-erasure").to_dict(source_commit="a" * 40)

    def erase_quality(rendered: dict[str, object]) -> None:
        rendered["executionStatus"] = "COMPLETE"
        rendered["diagnostics"] = []
        rendered["counts"]["diagnostics"] = 0
        rendered["input"]["container"]["interfaces"] = []
        for ref in rendered["packetRefs"]:
            ref["captureSnapLength"] = None
            ref["qualityCodes"] = []
        projection = rendered["contractProjection"]
        projection["nonProjectable"] = [
            item for item in projection["nonProjectable"]
            if item["sourceType"] != "PACKET-REF"
        ]
        ref = rendered["packetRefs"][0]
        projection["records"].append({
            "recordType": "PACKET-REF",
            "sourceId": ref["packetRefId"],
            "payload": {
                "captureId": ref["captureId"],
                "sectionId": ref["sectionId"],
                "interfaceId": ref["interfaceId"],
                "packetNumber": ref["packetIndex"],
                "rawTicks": ref["timestamp"]["ticks"],
                "resolution": {"ticksPerSecond": ref["timestamp"]["ticksPerSecond"]},
                "caplen": ref["capturedLength"],
                "origlen": ref["originalLength"],
                "decodeStatus": "FULL",
            },
        })

    erased = deepcopy(baseline)
    erase_quality(erased)
    assert any("container interface" in item for item in evidence_errors(erased))

    output = tmp_path / "snaplen-erasure.json"
    output.write_text("prior snaplen output", encoding="utf-8")
    original = pipeline_module.IntakeResult.to_dict

    def falsified(self: IntakeResult, *, source_commit: str) -> dict[str, object]:
        rendered = original(self, source_commit=source_commit)
        erase_quality(rendered)
        return rendered

    monkeypatch.setattr(pipeline_module.IntakeResult, "to_dict", falsified)
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", "cap-snaplen-erasure", "--output", str(output),
        "--source-commit", "a" * 40,
    ]) == 1
    assert output.read_text(encoding="utf-8") == "prior snaplen output"


def test_both_endian_snaplen_quality_reaches_cli_and_corpus(tmp_path: Path) -> None:
    """The public quality disposition is independent of container byte order."""
    packet = _valid_exchange()[0]

    def block(order: str, block_type: int, body: bytes) -> bytes:
        total = 12 + len(body)
        assert total % 4 == 0
        return struct.pack(f"{order}II", block_type, total) + body + struct.pack(f"{order}I", total)

    def pcap(order: str) -> bytes:
        magic = b"\xd4\xc3\xb2\xa1" if order == "<" else b"\xa1\xb2\xc3\xd4"
        return (
            magic + struct.pack(f"{order}HHIIII", 2, 4, 0, 0, 5, 1)
            + struct.pack(f"{order}IIII", 1, 0, len(packet), len(packet)) + packet
        )

    def pcapng(order: str) -> bytes:
        padding = b"\0" * (-len(packet) % 4)
        return (
            block(order, PCAPNG_SECTION_HEADER, struct.pack(f"{order}IHHq", 0x1A2B3C4D, 1, 0, -1))
            + block(order, 1, struct.pack(f"{order}HHI", 1, 0, 5))
            + block(order, 6, struct.pack(f"{order}IIIII", 0, 0, 1, len(packet), len(packet)) + packet + padding)
        )

    cases = {
        "pcap-little": pcap("<"), "pcap-big": pcap(">"),
        "pcapng-little": pcapng("<"), "pcapng-big": pcapng(">"),
    }
    for index, (label, content) in enumerate(cases.items()):
        capture = tmp_path / f"{label}.capture"
        capture.write_bytes(content)
        output = tmp_path / f"{label}.json"
        assert cli_main([
            "inspect", "--input", str(capture), "--capture-id", f"cap-{label}", "--output", str(output),
            "--source-commit", "a" * 40,
        ]) == 2
        rendered = json.loads(output.read_text(encoding="utf-8"))
        assert rendered["packetRefs"][0]["captureSnapLength"] == 5
        assert "CAPLEN-EXCEEDS-SNAPLEN" in rendered["packetRefs"][0]["qualityCodes"]
        assert evidence_errors(rendered) == []

    corpus_root = tmp_path / "snaplen-endian-corpus"
    corpus_root.mkdir()
    captures: list[dict[str, object]] = []
    for index, (label, content) in enumerate(cases.items(), 1):
        path = corpus_root / f"{label}.capture"
        path.write_bytes(content)
        captures.append({
            "captureId": f"HC-{index:02d}", "relativePath": path.name,
            "byteCount": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "observationQuality": "UNASSESSED-EXPLORATORY",
            "labelSource": "FILE-ANNOTATION-NONTRUTH", "rootCause": "UNKNOWN",
        })
    manifest = {
        "manifestId": "CLTAV-HISTORICAL-CAPTURES", "manifestVersion": "1.0",
        "purpose": "EXPLORATORY-DEVELOPMENT-ONLY", "captureCount": len(captures),
        "truthBoundary": "not experimental truth", "captures": captures,
    }
    manifest_path = tmp_path / "snaplen-endian-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    output_dir = tmp_path / "snaplen-endian-output"
    summary = run_corpus(
        manifest_path=manifest_path, corpus_root=corpus_root, output_dir=output_dir,
        config=IntakeConfig(), source_commit="a" * 40,
    )
    assert {row["executionStatus"] for row in summary["captures"]} == {"COMPLETE-WITH-CONTROLLED-ISSUES"}
    for item in captures:
        rendered = json.loads((output_dir / f"{item['captureId']}.json").read_text(encoding="utf-8"))
        assert rendered["packetRefs"][0]["captureSnapLength"] == 5
        assert evidence_errors(rendered) == []


def test_both_endian_container_version_and_shb_option_boundaries_reach_cli(tmp_path: Path) -> None:
    """Fatal container structure never becomes a clean supported capture."""
    packet = _valid_exchange()[0]

    def block(order: str, block_type: int, body: bytes) -> bytes:
        total = 12 + len(body)
        assert total % 4 == 0
        return struct.pack(f"{order}II", block_type, total) + body + struct.pack(f"{order}I", total)

    for order, label in (("<", "little"), (">", "big")):
        magic = b"\xd4\xc3\xb2\xa1" if order == "<" else b"\xa1\xb2\xc3\xd4"
        bad_pcap = tmp_path / f"bad-pcap-{label}.pcap"
        bad_pcap.write_bytes(magic + struct.pack(f"{order}HHIIII", 99, 99, 0, 0, 65535, 1))
        pcap_output = tmp_path / f"bad-pcap-{label}.json"
        pcap_output.write_text("old pcap publication", encoding="utf-8")
        assert cli_main([
            "inspect", "--input", str(bad_pcap), "--capture-id", f"cap-bad-pcap-{label}",
            "--output", str(pcap_output), "--source-commit", "a" * 40,
        ]) == 1
        assert pcap_output.read_text(encoding="utf-8") == "old pcap publication"

        bad_version = tmp_path / f"bad-pcapng-version-{label}.pcapng"
        bad_version.write_bytes(block(order, PCAPNG_SECTION_HEADER, struct.pack(f"{order}IHHq", 0x1A2B3C4D, 99, 99, -1)))
        version_output = tmp_path / f"bad-pcapng-version-{label}.json"
        version_output.write_text("old pcapng publication", encoding="utf-8")
        assert cli_main([
            "inspect", "--input", str(bad_version), "--capture-id", f"cap-bad-pcapng-{label}",
            "--output", str(version_output), "--source-commit", "a" * 40,
        ]) == 1
        assert version_output.read_text(encoding="utf-8") == "old pcapng publication"

        malformed_options = tmp_path / f"bad-pcapng-options-{label}.pcapng"
        malformed_shb = struct.pack(f"{order}IHHq", 0x1A2B3C4D, 1, 0, -1) + struct.pack(f"{order}HH", 0, 1)
        malformed_options.write_bytes(block(order, PCAPNG_SECTION_HEADER, malformed_shb))
        options_output = tmp_path / f"bad-pcapng-options-{label}.json"
        options_output.write_text("old option publication", encoding="utf-8")
        assert cli_main([
            "inspect", "--input", str(malformed_options), "--capture-id", f"cap-bad-options-{label}",
            "--output", str(options_output), "--source-commit", "a" * 40,
        ]) == 1
        assert options_output.read_text(encoding="utf-8") == "old option publication"

        # A supported 1.2 SHB, legal unknown padded option, and snaplen zero
        # remains an admitted container; TFTP incompleteness is a separate
        # controlled issue, not a snaplen/parser failure.
        padding = b"\0" * (-len(packet) % 4)
        legal_shb = (
            struct.pack(f"{order}IHHq", 0x1A2B3C4D, 1, 2, -1)
            + struct.pack(f"{order}HH", 0x00FF, 3) + b"abc\0" + struct.pack(f"{order}HH", 0, 0)
        )
        accepted = tmp_path / f"accepted-pcapng-{label}.pcapng"
        accepted.write_bytes(
            block(order, PCAPNG_SECTION_HEADER, legal_shb)
            + block(order, 1, struct.pack(f"{order}HHI", 1, 0, 0))
            + block(order, 6, struct.pack(f"{order}IIIII", 0, 0, 1, len(packet), len(packet)) + packet + padding)
        )
        accepted_output = tmp_path / f"accepted-pcapng-{label}.json"
        assert cli_main([
            "inspect", "--input", str(accepted), "--capture-id", f"cap-accepted-{label}",
            "--output", str(accepted_output), "--source-commit", "a" * 40,
        ]) == 2
        rendered = json.loads(accepted_output.read_text(encoding="utf-8"))
        assert rendered["packetRefs"][0]["captureSnapLength"] == 0
        assert "CAPLEN-EXCEEDS-SNAPLEN" not in rendered["packetRefs"][0]["qualityCodes"]
        assert evidence_errors(rendered) == []


def test_shared_evidence_budget_is_live_and_keeps_post_scan_boundaries_truthful(tmp_path: Path) -> None:
    packet = _valid_exchange()[0]
    section = _block(PCAPNG_SECTION_HEADER, struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1))
    idb = _block(1, struct.pack("<HHI", 1, 0, 65535))
    padding = b"\0" * (-len(packet) % 4)
    epb = _block(6, struct.pack("<IIIII", 0, 0, 1, len(packet), len(packet)) + packet + padding)
    tail = _block(1, struct.pack("<HHI", 1, 0, 65535)) * 3
    capture = tmp_path / "tail-interfaces.pcapng"
    capture.write_bytes(section + idb + epb + tail)
    limited = run_capture(capture, capture_id="cap-tail-idb", config=IntakeConfig(max_evidence_records=5))
    rendered = limited.to_dict(source_commit="a" * 40)
    retained = (
        len(rendered["input"]["container"]["interfaces"])
        + sum(len(rendered[name]) for name in ("packetRefs", "datagrams", "transfers", "events", "diagnostics"))
    )
    assert retained <= 5
    assert rendered["input"]["container"]["scanStatus"] == "STOPPED-RESOURCE-LIMIT"
    witness = next(item for item in rendered["diagnostics"] if item["code"] == "RESOURCE-INTERFACE-EVIDENCE-LIMIT")
    assert witness["detail"]["unconsumedSuffix"] == "NOT-CONSUMED"
    assert witness["detail"]["lastConsumedPacketRefId"] == rendered["packetRefs"][-1]["packetRefId"]
    assert evidence_errors(rendered) == []

    # Event retention can end after the entire capture has been consumed; it
    # must not counterfeit an unread-input resource stop.
    complete = tmp_path / "event-boundary.pcap"
    complete.write_bytes(_pcap(_valid_exchange()))
    post_scan = run_capture(complete, capture_id="cap-event-boundary", config=IntakeConfig(max_evidence_records=10))
    post_rendered = post_scan.to_dict(source_commit="a" * 40)
    event_witness = next(item for item in post_rendered["diagnostics"] if item["code"] == "RESOURCE-EVENT-LIMIT")
    assert post_rendered["input"]["container"]["scanStatus"] == "COMPLETE"
    assert "unconsumedSuffix" not in post_rendered["input"]["container"]
    assert event_witness["detail"]["scanStatus"] == "COMPLETE"
    assert evidence_errors(post_rendered) == []


def test_private_capture_and_tftp_diagnostics_cannot_bypass_live_evidence_budget(tmp_path: Path) -> None:
    """Producer-local diagnostic queues must not defer shared-budget enforcement."""
    malformed_capture = tmp_path / "capture-diagnostic-limit.pcap"
    malformed_capture.write_bytes(
        b"\xd4\xc3\xb2\xa1" + struct.pack("<HHIIII", 2, 4, 0, 0, 5, 1)
        + struct.pack("<IIII", 1, 0, 10, 5) + b"x" * 10
    )
    capture_limited = run_capture(
        malformed_capture,
        capture_id="cap-capture-diagnostic-limit",
        config=IntakeConfig(max_evidence_records=3, max_diagnostics=3),
    ).to_dict(source_commit="a" * 40)
    assert capture_limited["input"]["container"]["scanStatus"] == "STOPPED-RESOURCE-LIMIT"
    assert len(capture_limited["diagnostics"]) == 2
    # The malformed-packet diagnostic is ordinary evidence.  The packet that
    # would otherwise exceed the shared bound is the real input-stop cause,
    # so retain its precise witness rather than relabelling it as a generic
    # diagnostic limit.
    assert capture_limited["diagnostics"][-1]["code"] == "RESOURCE-PACKET-REF-LIMIT"
    assert capture_limited["diagnostics"][0]["detail"]["packetRefUnavailable"].endswith("P00000001")
    assert evidence_errors(capture_limited) == []

    tftp_capture = tmp_path / "tftp-diagnostic-limit.pcap"
    tftp_capture.write_bytes(_pcap([
        _ethernet_ipv4(_udp(10000, 69, b"\0\0"), identification=290),
        _ethernet_ipv4(_udp(10001, 69, b"\0\0"), identification=291),
    ]))
    tftp_limited = run_capture(
        tftp_capture,
        capture_id="cap-tftp-diagnostic-limit",
        config=IntakeConfig(max_evidence_records=50, max_diagnostics=1),
    ).to_dict(source_commit="a" * 40)
    # A bounded producer diagnostic alone is not an unread-input boundary.
    # The two packets were consumed; publish the post-scan diagnostic-retention
    # boundary instead of falsely stopping the capture at the first one.
    assert tftp_limited["input"]["container"]["scanStatus"] == "COMPLETE"
    assert [item["code"] for item in tftp_limited["diagnostics"]] == ["RESOURCE-DIAGNOSTIC-LIMIT"]
    assert tftp_limited["diagnostics"][0]["detail"]["retentionBoundary"] == "POST-SCAN-DIAGNOSTICS-TRUNCATED"
    assert evidence_errors(tftp_limited) == []


def test_live_budget_accounts_for_fragment_state_and_never_overreads_after_a_stop(tmp_path: Path) -> None:
    """EOF-owned reassembly differs from a real input-stop boundary."""
    incomplete = tmp_path / "one-fragment-at-eof.pcap"
    incomplete.write_bytes(_pcap([
        _ethernet_ipv4(b"abcdefgh", identification=301, more_fragments=True),
    ]))
    eof_result = run_capture(
        incomplete,
        capture_id="cap-one-fragment-eof",
        config=IntakeConfig(max_evidence_records=3),
    ).to_dict(source_commit="a" * 40)
    assert eof_result["input"]["container"]["containerPacketCount"] == 1
    assert eof_result["input"]["container"]["scanStatus"] == "COMPLETE"
    assert "unconsumedSuffix" not in eof_result["input"]["container"]
    assert [item["status"] for item in eof_result["datagrams"]] == ["GAPPED"]
    assert not any(item["code"].startswith("RESOURCE-") for item in eof_result["diagnostics"])
    assert evidence_errors(eof_result) == []

    three_packets = tmp_path / "early-stop-does-not-overread.pcap"
    three_packets.write_bytes(_pcap([
        _ethernet_ipv4(_udp(11000 + index, 12000, b"x"), identification=310 + index)
        for index in range(3)
    ]))
    stopped = run_capture(
        three_packets,
        capture_id="cap-no-overread",
        config=IntakeConfig(max_evidence_records=3),
    ).to_dict(source_commit="a" * 40)
    assert stopped["input"]["container"]["containerPacketCount"] == 1
    assert stopped["input"]["container"]["scanStatus"] == "STOPPED-RESOURCE-LIMIT"
    witness = next(item for item in stopped["diagnostics"] if item["code"] == "RESOURCE-DATAGRAM-RECORD-LIMIT")
    assert witness["detail"]["lastConsumedPacketIndex"] == 1
    assert evidence_errors(stopped) == []

    section = _block(PCAPNG_SECTION_HEADER, struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1))
    interface = _block(1, struct.pack("<HHI", 1, 0, 65535))
    no_packet_interfaces = tmp_path / "two-interfaces-budget-two.pcapng"
    no_packet_interfaces.write_bytes(section + interface + interface)
    interface_limited = run_capture(
        no_packet_interfaces,
        capture_id="cap-idb-budget-two",
        config=IntakeConfig(max_evidence_records=2),
    ).to_dict(source_commit="a" * 40)
    assert len(interface_limited["input"]["container"]["interfaces"]) == 1
    assert interface_limited["input"]["container"]["scanStatus"] == "STOPPED-RESOURCE-LIMIT"
    assert [item["code"] for item in interface_limited["diagnostics"]] == ["RESOURCE-INTERFACE-EVIDENCE-LIMIT"]
    assert evidence_errors(interface_limited) == []


def test_live_budget_charges_transfer_sessions_and_event_generation_before_slicing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    def exchange(client_port: int, server_port: int, identification: int) -> list[bytes]:
        return [
            _ethernet_ipv4(_udp(client_port, 69, _request(1, f"{client_port}.lui")), identification=identification),
            _ethernet_ipv4(
                _udp(server_port, client_port, _data(1, _lui_header())),
                source="10.0.0.2", destination="10.0.0.1", identification=identification + 1,
            ),
            _ethernet_ipv4(_udp(client_port, server_port, _ack(1)), identification=identification + 2),
        ]

    two = tmp_path / "two-transfers.pcap"
    two.write_bytes(_pcap(exchange(10100, 40100, 500) + exchange(10200, 40200, 510)))
    limited = run_capture(two, capture_id="cap-two-live", config=IntakeConfig(max_evidence_records=10))
    limited_rendered = limited.to_dict(source_commit="a" * 40)
    total = len(limited_rendered["input"]["container"]["interfaces"]) + sum(
        len(limited_rendered[name]) for name in ("packetRefs", "datagrams", "transfers", "events", "diagnostics")
    )
    assert total <= 10
    assert limited_rendered["input"]["container"]["scanStatus"] == "STOPPED-RESOURCE-LIMIT"
    assert any(item["code"].startswith("RESOURCE-") for item in limited_rendered["diagnostics"])
    assert evidence_errors(limited_rendered) == []

    # The production pipeline requests only a bounded prefix plus one
    # look-ahead boundary event; it must not materialise the whole event list.
    complete = tmp_path / "event-stream.pcap"
    complete.write_bytes(_pcap(_valid_exchange()))
    original_iter = pipeline_module.iter_first_slice_events
    pulls = 0

    def counted_iter(records: list[object]):
        nonlocal pulls
        for event in original_iter(records):
            pulls += 1
            yield event

    monkeypatch.setattr(pipeline_module, "iter_first_slice_events", counted_iter)
    bounded = run_capture(
        complete, capture_id="cap-event-stream",
        config=IntakeConfig(max_evidence_records=50, max_events=1),
    )
    assert len(bounded.events) == 1
    assert pulls == 2
    assert any(item.code == "RESOURCE-EVENT-LIMIT" for item in bounded.diagnostics)


def test_published_transfer_count_cannot_exceed_its_declared_run_limit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The envelope's retained transfer count is a live-budget defense too."""
    def exchange(client_port: int, server_port: int, identification: int) -> list[bytes]:
        return [
            _ethernet_ipv4(_udp(client_port, 69, _request(1, f"{client_port}.lui")), identification=identification),
            _ethernet_ipv4(
                _udp(server_port, client_port, _data(1, _lui_header())),
                source="10.0.0.2", destination="10.0.0.1", identification=identification + 1,
            ),
            _ethernet_ipv4(_udp(client_port, server_port, _ack(1)), identification=identification + 2),
        ]

    capture = tmp_path / "two-transfer-limit.pcap"
    capture.write_bytes(_pcap(exchange(11200, 41200, 600) + exchange(11300, 41300, 610)))
    config = IntakeConfig(max_transfer_records=2)
    baseline = run_capture(capture, capture_id="cap-transfer-limit", config=config).to_dict(source_commit="a" * 40)
    assert len(baseline["transfers"]) == 2
    assert evidence_errors(baseline) == []
    tampered = deepcopy(baseline)
    tampered["runParameters"]["maxTransferRecords"] = 1
    assert any("published transfers exceed" in item for item in evidence_errors(tampered))

    output = tmp_path / "two-transfer-limit.json"
    output.write_text("prior transfer-limit publication", encoding="utf-8")
    original = pipeline_module.IntakeResult.to_dict

    def lowered_limit(self: IntakeResult, *, source_commit: str) -> dict[str, object]:
        rendered = original(self, source_commit=source_commit)
        rendered["runParameters"]["maxTransferRecords"] = 1
        return rendered

    monkeypatch.setattr(pipeline_module.IntakeResult, "to_dict", lowered_limit)
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", "cap-transfer-limit", "--output", str(output),
        "--source-commit", "a" * 40, "--max-transfer-records", "2",
    ]) == 1
    assert output.read_text(encoding="utf-8") == "prior transfer-limit publication"


def test_local_transfer_limit_preserves_the_real_shared_budget_boundary(tmp_path: Path) -> None:
    """A local TFTP cap cannot impersonate a later scan/output boundary."""
    def request(client_port: int, identification: int) -> bytes:
        return _ethernet_ipv4(
            _udp(client_port, 69, _request(1, f"{client_port}.lui")),
            identification=identification,
        )

    two = tmp_path / "two-request-transfer-limit.pcap"
    two.write_bytes(_pcap([request(12000, 701), request(12001, 702)]))
    config = IntakeConfig(max_evidence_records=7, max_transfer_records=1)
    complete = run_capture(two, capture_id="cap-local-transfer-limit", config=config).to_dict(
        source_commit="a" * 40,
    )
    # One interface, two packet refs, two datagrams, and one admitted transfer
    # leave only the final shared slot.  The second-request diagnostic is local
    # and must not consume it; the first omitted derived event must instead
    # publish a truthful post-scan boundary.
    assert complete["input"]["container"]["scanStatus"] == "COMPLETE"
    assert complete["counts"]["containerPackets"] == 2
    assert [item["code"] for item in complete["diagnostics"]] == ["RESOURCE-EVENT-LIMIT"]
    assert complete["diagnostics"][0]["detail"]["retentionBoundary"] == "DERIVED-EVENTS-TRUNCATED"
    assert complete["diagnostics"][0]["detail"]["earlierDiagnosticRetention"] == "NOT-RETAINED"
    assert evidence_errors(complete) == []

    output = tmp_path / "two-request-transfer-limit.json"
    assert cli_main([
        "inspect", "--input", str(two), "--capture-id", "cap-local-transfer-limit-cli",
        "--output", str(output), "--source-commit", "a" * 40,
        "--max-evidence-records", "7", "--max-transfer-records", "1",
    ]) == 2
    cli_rendered = json.loads(output.read_text(encoding="utf-8"))
    assert cli_rendered["input"]["container"]["scanStatus"] == "COMPLETE"
    assert [item["code"] for item in cli_rendered["diagnostics"]] == ["RESOURCE-EVENT-LIMIT"]
    assert evidence_errors(cli_rendered) == []

    three = tmp_path / "three-request-transfer-limit.pcap"
    three.write_bytes(_pcap([request(12000, 701), request(12001, 702), request(12002, 703)]))
    stopped = run_capture(
        three, capture_id="cap-real-transfer-boundary", config=config,
    ).to_dict(source_commit="a" * 40)
    # The third packet actually exhausts the shared intake capacity.  Its
    # witness, not the earlier local transfer-record condition, must explain
    # why input stopped.
    assert stopped["input"]["container"]["scanStatus"] == "STOPPED-RESOURCE-LIMIT"
    assert stopped["counts"]["containerPackets"] == 3
    witness = next(item for item in stopped["diagnostics"] if item["code"] == "RESOURCE-PACKET-REF-LIMIT")
    assert witness["detail"]["lastConsumedPacketIndex"] == 3
    assert witness["detail"]["unconsumedSuffix"] == "NOT-CONSUMED"
    assert evidence_errors(stopped) == []


def test_missing_controlled_resource_is_named_and_prevents_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    """A resource/tool failure never degrades into a capture controlled issue."""
    capture = tmp_path / "resource-missing.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    output = tmp_path / "resource.json"
    output.write_text("old resource output", encoding="utf-8")
    original_path = controlled_resources._source_authority_path

    def unavailable_source(filename: str) -> Path:
        return tmp_path / "missing-controlled-resources" / filename

    monkeypatch.setattr(controlled_resources, "_source_authority_path", unavailable_source)
    class MissingFiles:
        def joinpath(self, _filename: str) -> "MissingFiles":
            return self

        def read_bytes(self) -> bytes:
            raise FileNotFoundError("missing resource")

    monkeypatch.setattr(controlled_resources.resources, "files", lambda _package: MissingFiles())
    controlled_resources.controlled_resource_bytes.cache_clear()
    controlled_resources.controlled_resource_json.cache_clear()
    development_contract_module.development_contract_snapshot.cache_clear()
    evidence_module._validator.cache_clear()
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", "cap-resource", "--output", str(output),
        "--source-commit", "a" * 40,
    ]) == 1
    assert "CONTROLLED-RESOURCE-UNAVAILABLE" in capsys.readouterr().err
    assert output.read_text(encoding="utf-8") == "old resource output"
    controlled_resources.controlled_resource_bytes.cache_clear()
    controlled_resources.controlled_resource_json.cache_clear()
    development_contract_module.development_contract_snapshot.cache_clear()
    evidence_module._validator.cache_clear()
    monkeypatch.setattr(controlled_resources, "_source_authority_path", original_path)


def test_changed_controlled_contract_resource_is_named_and_prevents_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    capture = tmp_path / "resource-changed.pcap"
    capture.write_bytes(_pcap(_valid_exchange()))
    output = tmp_path / "resource-changed.json"
    output.write_text("old changed-resource output", encoding="utf-8")
    original_bytes = controlled_resources.controlled_resource_bytes

    def changed_bytes(resource_id: str) -> bytes:
        if resource_id == "development-contract":
            return b"{}"
        return original_bytes(resource_id)

    monkeypatch.setattr(controlled_resources, "controlled_resource_bytes", changed_bytes)
    development_contract_module.development_contract_snapshot.cache_clear()
    assert cli_main([
        "inspect", "--input", str(capture), "--capture-id", "cap-resource-changed", "--output", str(output),
        "--source-commit", "a" * 40,
    ]) == 1
    assert "DEVELOPMENT-CONTRACT-IDENTITY-MISMATCH" in capsys.readouterr().err
    assert output.read_text(encoding="utf-8") == "old changed-resource output"
    development_contract_module.development_contract_snapshot.cache_clear()


def test_controlled_resource_identity_normalizes_only_crlf_record_separators(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The content identity is stable across Git CRLF/LF checkout variants."""
    raw = b'{\r\n  "escaped": "\\\\r\\\\n"\r\n}\r\n'
    monkeypatch.setattr(controlled_resources, "controlled_resource_bytes", lambda _: raw)
    expected = hashlib.sha256(b'{\n  "escaped": "\\\\r\\\\n"\n}\n').hexdigest()
    assert controlled_resources.controlled_resource_sha256("development-contract") == expected


def test_noneditable_wheel_contains_authoritative_resources_and_real_cli_runs(tmp_path: Path) -> None:
    """Exercise the installed entry point from an unrelated CWD, offline."""
    root = Path(__file__).resolve().parents[2]
    wheel_dir = tmp_path / "wheel"
    wheel_dir.mkdir()
    build = subprocess.run(
        [sys.executable, "-m", "pip", "wheel", "--no-deps", "--no-build-isolation", "--wheel-dir", str(wheel_dir), str(root)],
        text=True, capture_output=True,
    )
    assert build.returncode == 0, build.stderr
    wheel = next(wheel_dir.glob("*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        for filename in (
            "cltav_development_contracts.json",
            "cltav_development_contracts.schema.json",
            "cltav_offline_intake_evidence.schema.json",
        ):
            member = f"cltav_offline/resources/{filename}"
            assert archive.read(member) == (root / "configs" / "engineering" / filename).read_bytes()

    venv = tmp_path / "wheel-venv"
    create = subprocess.run([sys.executable, "-m", "venv", "--system-site-packages", str(venv)], text=True, capture_output=True)
    assert create.returncode == 0, create.stderr
    binary_dir = venv / ("Scripts" if os.name == "nt" else "bin")
    python = binary_dir / ("python.exe" if os.name == "nt" else "python")
    entrypoint = binary_dir / ("cltav-offline.exe" if os.name == "nt" else "cltav-offline")
    install = subprocess.run([str(python), "-m", "pip", "install", "--no-deps", str(wheel)], text=True, capture_output=True)
    assert install.returncode == 0, install.stderr
    unrelated = tmp_path / "unrelated"
    unrelated.mkdir()
    loaded = subprocess.run(
        [str(python), "-c", "import cltav_offline; print(cltav_offline.__file__)"],
        cwd=unrelated, text=True, capture_output=True,
    )
    assert loaded.returncode == 0 and "site-packages" in loaded.stdout.replace("\\", "/")

    normal = tmp_path / "wheel-normal.pcap"
    normal.write_bytes(_pcap(_valid_exchange()))
    normal_output = tmp_path / "wheel-normal.json"
    completed = subprocess.run([
        str(entrypoint), "inspect", "--input", str(normal), "--capture-id", "cap-wheel", "--output", str(normal_output),
        "--source-commit", "a" * 40,
    ], cwd=unrelated, text=True, capture_output=True)
    assert completed.returncode == 0, completed.stderr
    assert evidence_errors(json.loads(normal_output.read_text(encoding="utf-8"))) == []

    controlled = tmp_path / "wheel-controlled.pcap"
    controlled.write_bytes(_pcap([b"\0" * 20]))
    controlled_output = tmp_path / "wheel-controlled.json"
    completed = subprocess.run([
        str(entrypoint), "inspect", "--input", str(controlled), "--capture-id", "cap-wheel-issue", "--output", str(controlled_output),
        "--source-commit", "a" * 40,
    ], cwd=unrelated, text=True, capture_output=True)
    assert completed.returncode == 2, completed.stderr
    assert json.loads(controlled_output.read_text(encoding="utf-8"))["executionStatus"] == "COMPLETE-WITH-CONTROLLED-ISSUES"

    # A lawful incomplete RRQ is not a tool/schema failure in the packaged
    # entry point: its request event is publishable while its transfer remains
    # explicitly non-projectable until a responder TID is observed.
    for opcode in (1, 2):
        request_only = tmp_path / f"wheel-request-only-{opcode}.pcap"
        request_only.write_bytes(_pcap([
            _ethernet_ipv4(_udp(10000, 69, _request(opcode, "only.lui")), identification=400 + opcode),
        ]))
        request_output = tmp_path / f"wheel-request-only-{opcode}.json"
        completed = subprocess.run([
            str(entrypoint), "inspect", "--input", str(request_only), "--capture-id", f"cap-wheel-request-{opcode}",
            "--output", str(request_output), "--source-commit", "a" * 40,
        ], cwd=unrelated, text=True, capture_output=True)
        assert completed.returncode == 2, completed.stderr
        request_rendered = json.loads(request_output.read_text(encoding="utf-8"))
        assert evidence_errors(request_rendered) == []
        assert any(item["sourceId"].startswith("event-request-") for item in request_rendered["contractProjection"]["records"])

    # A packaged entry point also preserves a parse-quality contradiction as
    # controlled evidence rather than promoting a clean application record.
    wheel_quality = tmp_path / "wheel-length-mismatch.pcap"
    wheel_quality.write_bytes(_pcap([
        _ethernet_ipv4(_udp(10000, 69, _request(1, "mismatch.lui")), identification=410),
        _ethernet_ipv4(
            _udp(40000, 10000, _data(1, _role_header("LUI", 1000))),
            source="10.0.0.2", destination="10.0.0.1", identification=411,
        ),
        _ethernet_ipv4(_udp(10000, 40000, _ack(1)), identification=412),
    ]))
    quality_output = tmp_path / "wheel-length-mismatch.json"
    completed = subprocess.run([
        str(entrypoint), "inspect", "--input", str(wheel_quality), "--capture-id", "cap-wheel-length",
        "--output", str(quality_output), "--source-commit", "a" * 40,
    ], cwd=unrelated, text=True, capture_output=True)
    assert completed.returncode == 2, completed.stderr
    quality_rendered = json.loads(quality_output.read_text(encoding="utf-8"))
    assert any(
        event["layer"] == "PARSE-RESULT"
        and event["fields"].get("reason") == "DECLARED-FILE-LENGTH-MISMATCH"
        for event in quality_rendered["events"]
    )
    assert not any(event["layer"] == "APPLICATION" for event in quality_rendered["events"])
    assert evidence_errors(quality_rendered) == []

    fatal = tmp_path / "wheel-fatal.pcap"
    fatal.write_bytes(b"not a capture")
    protected = tmp_path / "wheel-protected.json"
    protected.write_text("old installed output", encoding="utf-8")
    completed = subprocess.run([
        str(entrypoint), "inspect", "--input", str(fatal), "--capture-id", "cap-wheel-fatal", "--output", str(protected),
        "--source-commit", "a" * 40,
    ], cwd=unrelated, text=True, capture_output=True)
    assert completed.returncode == 1
    assert protected.read_text(encoding="utf-8") == "old installed output"

    corpus_root = tmp_path / "wheel-corpus"
    corpus_root.mkdir()
    corpus_capture = corpus_root / "one.pcapng"
    corpus_capture.write_bytes(_pcapng(_valid_exchange()))
    manifest = tmp_path / "wheel-manifest.json"
    manifest.write_text(json.dumps(_corpus_manifest(corpus_root)), encoding="utf-8")
    corpus_output = tmp_path / "wheel-corpus-output"
    completed = subprocess.run([
        str(entrypoint), "corpus", "--manifest", str(manifest), "--corpus-root", str(corpus_root),
        "--output-dir", str(corpus_output), "--source-commit", "a" * 40,
    ], cwd=unrelated, text=True, capture_output=True)
    assert completed.returncode == 0, completed.stderr
    assert (corpus_output / "corpus-index.json").is_file()
