"""Installed command-line entry point for bounded offline intake evidence."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .bridge import (
    OfflineReplayError,
    adapt_offline_evidence_bytes,
    publish_offline_replay,
    validate_offline_replay_bytes,
)
from .corpus import publish_json, run_corpus
from .evidence import evidence_errors, evidence_failure_code
from .pipeline import IntakeConfig, IntakeError, run_capture, validate_source_commit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cltav-offline",
        description=(
            "Read-only bounded CL-TAV offline intake. Produces reconstruction evidence, "
            "or a non-scoring structural replay; never a conformance verdict."
        ),
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    inspect = subparsers.add_parser("inspect", help="process one capture into one evidence JSON file")
    inspect.add_argument("--input", required=True, type=Path)
    inspect.add_argument("--capture-id", required=True)
    inspect.add_argument("--output", required=True, type=Path)
    inspect.add_argument("--source-commit", default=None)
    _add_limits(inspect)
    corpus = subparsers.add_parser("corpus", help="audit and process a manifest-controlled local corpus")
    corpus.add_argument("--manifest", required=True, type=Path)
    corpus.add_argument("--corpus-root", required=True, type=Path)
    corpus.add_argument("--output-dir", required=True, type=Path)
    corpus.add_argument("--source-commit", default=None)
    _add_limits(corpus)
    replay = subparsers.add_parser(
        "replay",
        help="rebuild an intake envelope from capture bytes and publish a non-scoring OFFLINE-REPLAY bridge",
    )
    replay.add_argument("--input", required=True, type=Path)
    replay.add_argument("--offline-evidence", required=True, type=Path)
    replay.add_argument("--output", required=True, type=Path)
    validate_replay = subparsers.add_parser(
        "validate-replay",
        help="rebuild capture and intake evidence, then validate a persisted OFFLINE-REPLAY bridge",
    )
    validate_replay.add_argument("--input", required=True, type=Path)
    validate_replay.add_argument("--offline-evidence", required=True, type=Path)
    validate_replay.add_argument("--bridge", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command in {"replay", "validate-replay"}:
            try:
                offline_raw = args.offline_evidence.read_bytes()
            except OSError as exc:
                raise OfflineReplayError("OFFLINE-EVIDENCE-READ-ERROR", "offline evidence file cannot be read") from exc
            if args.command == "replay":
                run = adapt_offline_evidence_bytes(
                    offline_raw,
                    capture_path=args.input,
                    evidence_path=args.offline_evidence,
                )
                document = publish_offline_replay(run, output=args.output)
                print(
                    "cltav-offline: wrote replay "
                    f"{args.output.name}: {len(document['records'])} bridge record(s), NOT-SCORED",
                )
                return 0
            try:
                bridge_raw = args.bridge.read_bytes()
            except OSError as exc:
                raise OfflineReplayError("OFFLINE-BRIDGE-READ-ERROR", "offline replay file cannot be read") from exc
            document = validate_offline_replay_bytes(
                bridge_raw,
                capture_path=args.input,
                offline_evidence_raw=offline_raw,
                evidence_path=args.offline_evidence,
            )
            print(
                "cltav-offline: validated replay "
                f"{args.bridge.name}: {len(document['records'])} bridge record(s), NOT-SCORED",
            )
            return 0
        config = IntakeConfig(
            max_packet_bytes=args.max_packet_bytes,
            max_container_block_bytes=args.max_container_block_bytes,
            max_active_datagrams=args.max_active_datagrams,
            max_datagram_bytes=args.max_datagram_bytes,
            max_fragments_per_datagram=args.max_fragments_per_datagram,
            max_active_transfers=args.max_active_transfers,
            max_transfer_records=args.max_transfer_records,
            max_transfer_bytes=args.max_transfer_bytes,
            max_active_transfer_bytes=args.max_active_transfer_bytes,
            max_completed_payload_bytes=args.max_completed_payload_bytes,
            max_evidence_records=args.max_evidence_records,
            max_packet_refs=args.max_packet_refs,
            max_diagnostics=args.max_diagnostics,
            max_events=args.max_events,
            max_interfaces=args.max_interfaces,
            tftp_service_port=args.tftp_service_port,
        )
        source_commit = validate_source_commit(args.source_commit)
        if args.command == "inspect":
            _validate_single_output(args.input, args.output)
            result = run_capture(args.input, capture_id=args.capture_id, config=config)
            data = result.to_dict(source_commit=source_commit)
            errors = evidence_errors(data)
            if errors:
                raise IntakeError(evidence_failure_code(errors), "; ".join(errors))
            publish_json(data, args.output)
            print(f"offline intake wrote {args.output.name}: {data['executionStatus']}")
            return 0 if data["executionStatus"] == "COMPLETE" else 2
        summary = run_corpus(
            manifest_path=args.manifest,
            corpus_root=args.corpus_root,
            output_dir=args.output_dir,
            config=config,
            source_commit=source_commit,
        )
        controlled = any(row["executionStatus"] != "COMPLETE" for row in summary["captures"])
        print(
            f"offline corpus intake wrote {len(summary['captures'])} capture records: "
            f"{'COMPLETE-WITH-CONTROLLED-ISSUES' if controlled else 'COMPLETE'}"
        )
        return 2 if controlled else 0
    except (IntakeError, OfflineReplayError) as exc:
        print(f"cltav-offline: {exc.code}: {exc}", file=sys.stderr)
        return 1


def _add_limits(parser: argparse.ArgumentParser) -> None:
    limits = parser.add_argument_group("implementation resource limits (not protocol constants)")
    limits.add_argument("--max-packet-bytes", type=int, default=2 * 1024 * 1024)
    limits.add_argument("--max-container-block-bytes", type=int, default=4 * 1024 * 1024)
    limits.add_argument("--max-active-datagrams", type=int, default=128)
    limits.add_argument("--max-datagram-bytes", type=int, default=65_535)
    limits.add_argument("--max-fragments-per-datagram", type=int, default=8_192)
    limits.add_argument("--max-active-transfers", type=int, default=128)
    limits.add_argument("--max-transfer-records", type=int, default=50_000)
    limits.add_argument("--max-transfer-bytes", type=int, default=16 * 1024 * 1024)
    limits.add_argument("--max-active-transfer-bytes", type=int, default=16 * 1024 * 1024)
    limits.add_argument("--max-completed-payload-bytes", type=int, default=16 * 1024 * 1024)
    limits.add_argument("--max-evidence-records", type=int, default=50_000)
    limits.add_argument("--max-packet-refs", type=int, default=50_000)
    limits.add_argument("--max-diagnostics", type=int, default=50_000)
    limits.add_argument("--max-events", type=int, default=50_000)
    limits.add_argument("--max-interfaces", type=int, default=1_024)
    limits.add_argument("--tftp-service-port", type=int, default=69)


def _validate_single_output(input_path: Path, output: Path) -> None:
    try:
        resolved_input = input_path.resolve(strict=True)
    except OSError as exc:
        raise IntakeError("INPUT-READ-ERROR", str(exc)) from exc
    if not resolved_input.is_file():
        raise IntakeError("INPUT-READ-ERROR", "input must be an ordinary file")
    resolved_output = output.resolve(strict=False)
    if resolved_output == resolved_input:
        raise IntakeError("UNSAFE-OUTPUT-PATH", "output must not overwrite the input capture")
    if output.exists() and output.is_symlink():
        raise IntakeError("UNSAFE-OUTPUT-PATH", "output must not be a symbolic link")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
