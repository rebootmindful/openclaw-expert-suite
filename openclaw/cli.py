"""
Command-line interface for the openclaw expert system.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from openclaw import __version__
from openclaw.rules import Fact, FactBase


def _print_facts(fb: FactBase) -> None:
    if not fb.all_facts():
        print("  (no facts)")
        return
    for fact in fb.all_facts():
        print(f"  {fact.name} = {fact.value!r}")


def _cmd_version(args: argparse.Namespace) -> int:  # noqa: ARG001
    print(f"openclaw-expert-suite {__version__}")
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    """Load facts from a JSON file and evaluate a simple rule set."""
    path = Path(args.facts_file)
    if not path.exists():
        print(f"Error: facts file not found: {path}", file=sys.stderr)
        return 1

    try:
        raw = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {path}: {exc}", file=sys.stderr)
        return 1

    if not isinstance(raw, dict):
        print("Error: facts file must be a JSON object (key→value map)", file=sys.stderr)
        return 1

    fb = FactBase()
    for name, value in raw.items():
        fb.declare(Fact(name, value))

    print(f"Loaded {len(fb)} fact(s) from '{path}':")
    _print_facts(fb)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openclaw",
        description="openclaw-expert-suite: open-source expert system toolkit",
    )
    parser.add_argument(
        "--version", action="store_true", help="Print version and exit"
    )

    sub = parser.add_subparsers(dest="command")

    # run sub-command
    run_p = sub.add_parser("run", help="Load facts and run the inference engine")
    run_p.add_argument(
        "facts_file",
        metavar="FACTS",
        help="Path to a JSON file containing fact name→value pairs",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version or args.command is None:
        if args.version:
            return _cmd_version(args)
        parser.print_help()
        return 0

    if args.command == "run":
        return _cmd_run(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
