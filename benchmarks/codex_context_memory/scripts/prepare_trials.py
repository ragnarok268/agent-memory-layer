from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "tasks.json"
TRIALS = ROOT / "trial_workdirs"
FIXTURES = {
    "baseline": ROOT / "fixtures" / "baseline_repo",
    "aml": ROOT / "fixtures" / "aml_repo",
}


def copy_fixture(task_id: str, condition: str, overwrite: bool) -> None:
    destination = TRIALS / task_id / condition
    if destination.exists():
        if not overwrite:
            return
        shutil.rmtree(destination)
    shutil.copytree(FIXTURES[condition], destination)
    if task_id == "task5":
        test_path = destination / "test_app.py"
        text = test_path.read_text(encoding="utf-8")
        text = text.replace(
            'self.assertEqual(app.normalize_status(" OK "), "ok")',
            'self.assertEqual(app.normalize_status(" OK "), "OK")',
        )
        test_path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare clean paired benchmark trial workdirs.")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing trial workdirs.")
    args = parser.parse_args()

    tasks = json.loads(TASKS_PATH.read_text(encoding="utf-8"))["tasks"]
    for task in tasks:
        for condition in FIXTURES:
            copy_fixture(task["id"], condition, args.overwrite)
    print(f"prepared trial workdirs under {TRIALS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
