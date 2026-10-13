"""Installed command-line entry point for bounded offline intake evidence."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

from . import __version__
from .corpus import publish_json, run_corpus
from .evidence import evidence_errors
from .pipeline import IntakeConfig, IntakeError, run_capture, validate_source_commit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cltav-offline",
        description=(
            "Read-only bounded CL-TAV offline intake. Produces reconstruction evidence, "
            "not a conformance verdict."
        ),
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    inspect = subparsers.add_parser("inspect", help="process one capture into one evidence JSON file")
    inspect.add_argument("--input", required=True, type=Path)
    inspect.add_argument("--capture-id", required=True)
    inspect.add_argument("--output", required=True, type=Path)
    inspect.add_argument("--source-commit", default=_source_commit_default())
    _add_limits(inspect)
    corpus = subparsers.add_parser("corpus", help="audit and process a manifest-controlled local corpus")
    corpus.add_argument("--manifest", required=True, type=Path)
    corpus.add_argument("--corpus-root", required=True, type=Path)
    corpus.add_argument("--output-dir", required=True, type=Path)
    corpus.add_argument("--source-commit", default=_source_commit_default())
    _add_limits(corpus)
    args = parser.parse_args(argv)
    config = IntakeConfig(
        max_packet_bytes=args.max_packet_bytes,
        max_container_block_bytes=args.max_container_block_bytes,
        max_active_datagrams=args.max_active_datagrams,
        max_datagram_bytes=args.max_datagram_bytes,
        max_fragments_per_datagram=args.max_fragments_per_datagram,
        max_active_transfers=args.max_active_transfers,
        max_transfer_records=args.max_transfer_records,
        max_transfer_bytes=args.max_transfer_bytes,
        max_evidence_records=args.max_evidence_records,
        tftp_service_port=args.tftp_service_port,
    )
    try:
        source_commit = validate_source_commit(args.source_commit)
        if args.command == "inspect":
            _validate_single_output(args.input, args.output)
            result = run_capture(args.input, capture_id=args.capture_id, config=config)
            data = result.to_dict(source_commit=source_commit)
            errors = evidence_errors(data)
            if errors:
                raise IntakeError("EVIDENCE-SCHEMA-ERROR", "; ".join(errors))
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
    except IntakeError as exc:
        print(f"cltav-offline: {exc.code}: {exc}", file=sys.stderr)
        return 1


def _source_commit_default() -> str:
    candidate = os.environ.get("GITHUB_SHA")
    if candidate:
        return candidate.strip().lower()
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return "UNSPECIFIED"
    value = completed.stdout.strip().lower()
    return value if re.fullmatch(r"[0-9a-f]{40}", value) else "UNSPECIFIED"


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
    limits.add_argument("--max-evidence-records", type=int, default=50_000)
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
