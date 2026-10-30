"""Installed command line for finite CL-TAV synthetic evidence.

The CLI deliberately requires an explicit local Git authority repository,
commit and paths.  It neither discovers a current checkout nor imports a test
fixture.  It contains no network, capture or IUT operation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .evidence import (
    CHECKPOINT_ARTIFACT_TYPE,
    EvidenceError,
    continue_checkpoint,
    create_checkpoint,
    load_evidence_bytes,
    load_sources,
    publish_checkpoint,
    publish_run,
    run_scenario,
    validate_checkpoint_bytes,
    validate_evidence_bytes,
)


def _add_authority_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--authority-repository", required=True, type=Path)
    parser.add_argument("--authority-commit", required=True)
    parser.add_argument("--development-path", required=True)
    parser.add_argument("--interface-path", required=True)
    parser.add_argument("--scenario-path", required=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cltav-runtime",
        description=(
            "Run, validate, or replay bounded synthetic CL-TAV engineering evidence; "
            "not a protocol verdict or IUT executor."
        ),
    )
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="run a finite Git-bound synthetic scenario and publish evidence")
    _add_authority_arguments(run)
    run.add_argument("--output", required=True, type=Path)
    checkpoint = commands.add_parser(
        "checkpoint",
        help="publish a validated open prefix for bounded formal continuation",
    )
    _add_authority_arguments(checkpoint)
    checkpoint.add_argument("--prefix-rounds", required=True, type=int)
    checkpoint.add_argument("--output", required=True, type=Path)
    validate = commands.add_parser("validate", help="validate an evidence file by rebuilding the Git-bound scenario")
    _add_authority_arguments(validate)
    validate.add_argument("--evidence", required=True, type=Path)
    replay = commands.add_parser("replay", help="validate then independently re-run a finite evidence scenario")
    _add_authority_arguments(replay)
    replay.add_argument("--evidence", required=True, type=Path)
    resume = commands.add_parser(
        "continue",
        help="validate a Git-bound checkpoint then execute only its remaining declared rounds",
    )
    _add_authority_arguments(resume)
    resume.add_argument("--checkpoint", required=True, type=Path)
    resume.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        sources = load_sources(
            repository=args.authority_repository,
            commit=args.authority_commit,
            development_path=args.development_path,
            interface_path=args.interface_path,
            scenario_path=args.scenario_path,
        )
        if args.command == "run":
            document = publish_run(run_scenario(sources), output=args.output)
            print(
                "cltav-runtime: wrote "
                f"{args.output.name}: {len(document['rounds'])} round(s), "
                f"{document['outcome']['stopReason'] or 'OPEN'}",
            )
            return 0
        if args.command == "checkpoint":
            checkpoint_run = create_checkpoint(sources, prefix_rounds=args.prefix_rounds)
            verified = publish_checkpoint(checkpoint_run, output=args.output)
            print(
                "cltav-runtime: wrote checkpoint "
                f"{args.output.name}: {verified.prefix_rounds} prefix round(s), OPEN-PREFIX",
            )
            return 0
        if args.command == "continue":
            try:
                checkpoint_raw = args.checkpoint.read_bytes()
            except OSError as exc:
                raise EvidenceError("CHECKPOINT-READ-ERROR", "checkpoint file cannot be read") from exc
            verified = validate_checkpoint_bytes(checkpoint_raw, sources=sources)
            continued = continue_checkpoint(verified)
            document = publish_run(continued, output=args.output)
            print(
                "cltav-runtime: continued "
                f"{args.checkpoint.name}: {len(document['rounds'])} round(s), "
                f"{document['outcome']['stopReason'] or 'OPEN'}",
            )
            return 0
        try:
            raw = args.evidence.read_bytes()
        except OSError as exc:
            raise EvidenceError("EVIDENCE-READ-ERROR", "evidence file cannot be read") from exc
        # ``validate`` is deliberately capable of checking a durable prefix
        # without continuing it.  The checkpoint parser remains canonical and
        # source-bound; no artifact field chooses a runtime branch.
        decoded = load_evidence_bytes(raw)
        if args.command == "validate":
            if decoded.get("artifactType") == CHECKPOINT_ARTIFACT_TYPE:
                verified = validate_checkpoint_bytes(raw, sources=sources)
                print(
                    "cltav-runtime: validated checkpoint "
                    f"{args.evidence.name}: {verified.prefix_rounds} prefix round(s)",
                )
                return 0
            expected = validate_evidence_bytes(raw, sources=sources)
            print(f"cltav-runtime: validated {args.evidence.name}: {len(expected['rounds'])} round(s)")
            return 0
        expected = validate_evidence_bytes(raw, sources=sources)
        # Validation already rebuilt the whole run from the exact same raw Git
        # sources.  Construct it once more for the explicit command result;
        # this does not read the evidence as an algorithm input.
        replayed = run_scenario(sources)
        print(
            "cltav-runtime: replayed "
            f"{args.evidence.name}: {len(replayed.result.state.evidence)} round(s), "
            f"{replayed.result.stop_reason or 'OPEN'}",
        )
        return 0
    except EvidenceError as exc:
        print(f"cltav-runtime: {exc.code}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
