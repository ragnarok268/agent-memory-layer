"""DS2 CLI."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from ds2 import __version__
from ds2.graph.explain import explain_package
from ds2.scan import run_scan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ds2")
    parser.add_argument("--version", action="version", version=f"ds2 {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan a Python project for dependency topology and runtime exposure.")
    scan_parser.add_argument("path", help="Project path to scan.")
    scan_parser.add_argument("--out", default=".ds2", help="Output directory for report artifacts.")
    scan_parser.add_argument("--json", action="store_true", help="Also emit the graph JSON to stdout.")

    explain_parser = subparsers.add_parser("explain", help="Explain a package from a fresh scan of the current directory.")
    explain_parser.add_argument("package", help="Package name to explain.")
    explain_parser.add_argument("--path", default=".", help="Project path to scan before explaining.")
    explain_parser.add_argument("--out", default=".ds2", help="Output directory for scan artifacts.")

    subparsers.add_parser("version", help="Print the DS2 version.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        result = run_scan(Path(args.path), Path(args.out))
        if args.json:
            sys.stdout.write(result["graph_text"])
        else:
            output_root = Path(args.out).resolve().as_posix()
            sys.stdout.write(f"DS2 report generated: {output_root}/DS2_REPORT.md\n")
            sys.stdout.write(f"DS2 receipt generated: {output_root}/ds2_receipt.json\n")
        return 0

    if args.command == "explain":
        result = run_scan(Path(args.path), Path(args.out))
        sys.stdout.write(explain_package(args.package, result["graph"].direct_dependencies) + "\n")
        return 0

    if args.command == "version":
        sys.stdout.write(f"{__version__}\n")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
