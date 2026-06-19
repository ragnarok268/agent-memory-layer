from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ROOT_DIR / "results"


def elapsed_seconds(start: datetime, end: datetime) -> float:
    return round((end - start).total_seconds(), 2)


def timing_log_path(run_id: str, results_dir: Path = RESULTS_DIR) -> Path:
    return results_dir / f"{run_id}.timing.json"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture timing evidence for A/B adoption trials.")
    parser.add_argument("--condition", required=True, choices=("baseline", "workflow"))
    parser.add_argument("--agent", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--command", help="Command string to run and time.")
    parser.add_argument("--manual", action="store_true", help="Wait for Enter to stop timing.")
    parser.add_argument("--merge-into", help="Existing scored run log JSON file to update.")
    return parser.parse_args(argv)


def validate_args(args: argparse.Namespace) -> None:
    if args.manual == bool(args.command):
        raise ValueError("Choose exactly one of --manual or --command.")


def utc_timestamp(value: datetime) -> str:
    return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_timing_record(
    *,
    run_id: str,
    condition: str,
    agent_name: str,
    task_id: str,
    run_start_timestamp: str,
    run_end_timestamp: str,
    elapsed: float,
    command: str | None,
    exit_code: int,
) -> dict:
    return {
        "run_id": run_id,
        "repo_condition": condition,
        "agent_name": agent_name,
        "task_id": task_id,
        "run_start_timestamp": run_start_timestamp,
        "run_end_timestamp": run_end_timestamp,
        "elapsed_seconds": elapsed,
        "command": command,
        "exit_code": exit_code,
    }


def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def merge_timing_fields(target_path: Path, timing_record: dict) -> Path:
    existing = json.loads(target_path.read_text(encoding="utf-8-sig"))
    existing["run_start_timestamp"] = timing_record["run_start_timestamp"]
    existing["run_end_timestamp"] = timing_record["run_end_timestamp"]
    existing["elapsed_seconds"] = timing_record["elapsed_seconds"]
    write_json(target_path, existing)
    return target_path


def run_wrapped_command(command: str) -> int:
    return subprocess.run(shlex.split(command), check=False).returncode


def execute(args: argparse.Namespace) -> tuple[dict, Path]:
    validate_args(args)
    start_dt = datetime.now(UTC)
    start_ts = utc_timestamp(start_dt)

    if args.manual:
        print(f"Timing started at {start_ts}")
        input("Press Enter to stop timing...")
        exit_code = 0
        command = None
    else:
        exit_code = run_wrapped_command(args.command)
        command = args.command

    end_dt = datetime.now(UTC)
    end_ts = utc_timestamp(end_dt)
    record = build_timing_record(
        run_id=args.run_id,
        condition=args.condition,
        agent_name=args.agent,
        task_id=args.task,
        run_start_timestamp=start_ts,
        run_end_timestamp=end_ts,
        elapsed=elapsed_seconds(start_dt, end_dt),
        command=command,
        exit_code=exit_code,
    )
    timing_path = write_json(timing_log_path(args.run_id), record)

    if args.merge_into:
        merge_timing_fields(Path(args.merge_into), record)

    return record, timing_path


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        record, timing_path = execute(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(timing_path.as_posix())
    if args.merge_into:
        print(Path(args.merge_into).as_posix())
    return record["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
