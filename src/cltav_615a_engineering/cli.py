"""Installed command ``cltav-615a-engineering`` for run / verify / replay.

Exit code 0 means a valid engineering record or verification completed under
the D-stage contract.  It is not an IUT PASS, protocol conformance, or
scientific result.  Named EngineeringError values return 1.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .errors import EngineeringError
from .publish import publish_run
from .runner import CASE_IDS, run_case
from .verify import compare_semantic, load_evidence_directory, verify_document


def _add_authority(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--authority-repository", required=True, type=Path)
    parser.add_argument("--authority-commit", required=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cltav-615a-engineering",
        description=(
            "Run, verify, or replay bounded 615A UPLOAD control-slice engineering "
            "evidence. Exit 0 is a valid engineering record, not an IUT PASS."
        ),
    )
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="execute one named case and publish a closed evidence directory")
    _add_authority(run)
    run.add_argument("--case-id", required=True, choices=CASE_IDS)
    run.add_argument("--resource-mode", default="ROUNDS", choices=("ROUNDS", "BUDGET"))
    run.add_argument("--resource-remaining", default=8, type=int)
    run.add_argument("--output", required=True, type=Path)
    verify = commands.add_parser("verify", help="recompute identities, fingerprint, journal and cost relations")
    _add_authority(verify)
    verify.add_argument("--evidence", required=True, type=Path)
    replay = commands.add_parser("replay", help="re-execute the same case and compare semantic fields")
    _add_authority(replay)
    replay.add_argument("--evidence", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "run":
            executed = run_case(
                repository=args.authority_repository,
                authority_commit=args.authority_commit,
                case_id=args.case_id,
                resource_mode=args.resource_mode,
                resource_remaining=args.resource_remaining,
            )
            publish_run(executed.document, output=args.output, repository=executed.repository)
            stop = executed.document["algorithmVisible"]["stop"]["reason"]
            print(
                "cltav-615a-engineering: wrote "
                f"{args.output.name}: {executed.case_id}, stop={stop or 'OPEN'}; "
                "exit 0 is a valid engineering record, not an IUT PASS",
            )
            return 0
        document = load_evidence_directory(args.evidence)
        verified = verify_document(
            document,
            repository=args.authority_repository,
            authority_commit=args.authority_commit,
        )
        if args.command == "verify":
            print(
                "cltav-615a-engineering: verified "
                f"{args.evidence.name}: {verified['algorithmVisible']['identities']['caseId']}; "
                "exit 0 is a valid engineering record, not an IUT PASS",
            )
            return 0
        replayed = run_case(
            repository=args.authority_repository,
            authority_commit=args.authority_commit,
            case_id=verified["algorithmVisible"]["identities"]["caseId"],
            resource_mode=verified["algorithmVisible"]["configuration"]["resourceMode"],
            resource_remaining=verified["algorithmVisible"]["configuration"]["resourceRemainingInitial"],
        )
        compare_semantic(verified, replayed.document)
        print(
            "cltav-615a-engineering: replayed "
            f"{args.evidence.name}: {replayed.case_id}, stop={replayed.document['algorithmVisible']['stop']['reason']}; "
            "exit 0 is a valid engineering record, not an IUT PASS",
        )
        return 0
    except EngineeringError as exc:
        print(f"cltav-615a-engineering: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
