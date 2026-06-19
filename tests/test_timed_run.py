import json
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
EXPERIMENT_DIR = ROOT_DIR / "experiments" / "ab_adoption"
RESULTS_DIR = EXPERIMENT_DIR / "results"
SCRIPT_PATH = EXPERIMENT_DIR / "timed_run.py"


def remove_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()


def test_timed_run_file_exists():
    assert SCRIPT_PATH.exists()


def test_timed_run_wraps_successful_command_and_writes_json():
    timing_path = RESULTS_DIR / "timed-success.timing.json"
    run_log_path = RESULTS_DIR / "timed-success.json"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    remove_if_exists(timing_path)
    remove_if_exists(run_log_path)
    run_log_path.write_text(
        json.dumps(
            {
                "run_id": "timed-success",
                "repo_condition": "baseline",
                "agent_name": "Codex",
                "task_id": "task_smoke",
                "total_score": 3,
                "subscores": {},
                "notes": "",
                "failures": [],
                "artifacts_created": [],
                "guardrail_ran": False,
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    try:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--condition",
                "baseline",
                "--agent",
                "Codex",
                "--task",
                "task_smoke",
                "--run-id",
                "timed-success",
                "--command",
                "python -c \"print('ok')\"",
                "--merge-into",
                str(run_log_path),
            ],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=False,
        )

        assert completed.returncode == 0
        assert timing_path.exists()
        payload = json.loads(timing_path.read_text(encoding="utf-8"))
        assert payload["run_start_timestamp"].endswith("Z")
        assert payload["run_end_timestamp"].endswith("Z")
        assert payload["elapsed_seconds"] >= 0
        assert payload["exit_code"] == 0
        assert payload["command"] == "python -c \"print('ok')\""

        merged = json.loads(run_log_path.read_text(encoding="utf-8"))
        assert merged["run_start_timestamp"] == payload["run_start_timestamp"]
        assert merged["run_end_timestamp"] == payload["run_end_timestamp"]
        assert merged["elapsed_seconds"] == payload["elapsed_seconds"]
        assert merged["total_score"] == 3
    finally:
        remove_if_exists(timing_path)
        remove_if_exists(run_log_path)


def test_timed_run_records_failure_honestly():
    timing_path = RESULTS_DIR / "timed-failure.timing.json"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    remove_if_exists(timing_path)
    try:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--condition",
                "workflow",
                "--agent",
                "Codex",
                "--task",
                "task_failure",
                "--run-id",
                "timed-failure",
                "--command",
                "python -c \"import sys; sys.exit(3)\"",
            ],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=False,
        )

        assert completed.returncode == 3
        payload = json.loads(timing_path.read_text(encoding="utf-8"))
        assert payload["exit_code"] == 3
        assert payload["elapsed_seconds"] >= 0
    finally:
        remove_if_exists(timing_path)
