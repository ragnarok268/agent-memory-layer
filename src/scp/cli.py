"""SCP CLI."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from scp import __version__
from scp.classifier import NO_PRESERVATION, classify_summary
from scp.generator import generate_event_card
from scp.onboarding import DEFAULT_ORIGIN_PATH, prompt_and_write_origin
from scp.schema import SchemaError, validate_path
from scp.yamlio import write_yaml_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="scp")
    parser.add_argument("--version", action="version", version=f"scp {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate an SCP YAML record or directory of records.")
    validate_parser.add_argument("path", help="YAML file or directory to validate.")

    classify_parser = subparsers.add_parser("classify", help="Classify a change summary using the approved Canon.")
    classify_parser.add_argument("summary", help="Change summary to classify.")

    generate_parser = subparsers.add_parser("generate", help="Generate an SCP event card from a change summary.")
    generate_parser.add_argument("--summary", required=True, help="Change summary to convert into an SCP event card.")
    generate_parser.add_argument("--out", required=True, help="Output YAML path.")

    init_parser = subparsers.add_parser("init", help="Create the starting SCP Origin Card.")
    init_parser.add_argument("--out", default=str(DEFAULT_ORIGIN_PATH), help="Output YAML path for the Origin Card.")

    subparsers.add_parser("version", help="Print the SCP version.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        try:
            validated_paths = validate_path(Path(args.path))
        except SchemaError as exc:
            sys.stderr.write(f"{exc}\n")
            return 1
        sys.stdout.write(f"Validated {len(validated_paths)} file(s).\n")
        return 0

    if args.command == "classify":
        classification = classify_summary(args.summary)
        sys.stdout.write(f"{classification.event_type}\n")
        return 0

    if args.command == "generate":
        card = generate_event_card(args.summary)
        if card is None:
            sys.stdout.write(f"{NO_PRESERVATION}\n")
            return 0
        output_path = Path(args.out)
        write_yaml_file(output_path, card)
        sys.stdout.write(f"Generated {output_path.as_posix()}\n")
        return 0

    if args.command == "init":
        output_path = prompt_and_write_origin(Path(args.out))
        sys.stdout.write(f"Generated {output_path.as_posix()}\n")
        return 0

    if args.command == "version":
        sys.stdout.write(f"{__version__}\n")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
