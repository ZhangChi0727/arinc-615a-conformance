"""CLI entry point — expand as milestones C1+ land."""

from __future__ import annotations

import argparse

from a615a_sim import __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="a615a-sim",
        description="ARINC 615A dual-role conformance simulator (skeleton).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--role",
        choices=("dls", "thw"),
        help="Protocol role (wired up in later milestones).",
    )
    args = parser.parse_args(argv)
    if args.role:
        print(f"Role selected: {args.role} (not implemented yet — see PROJECT_PLAN.md)")
    else:
        print(f"a615a-sim {__version__} — skeleton OK. See PROJECT_PLAN.md for milestones.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
