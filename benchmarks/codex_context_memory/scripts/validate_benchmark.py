from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "tasks.json"
BASELINE = ROOT / "fixtures" / "baseline_repo"
AML = ROOT / "fixtures" / "aml_repo"


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"missing required path: {path}")


def validate_tasks() -> None:
    data = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    tasks = data.get("tasks", [])
    if data.get("task_count") != 12 or len(tasks) != 12:
        raise SystemExit("tasks.json must define exactly 12 tasks")
    expected = [f"task{i}" for i in range(1, 9)] + [
        "memory_challenge_a",
        "memory_challenge_b",
        "memory_challenge_c",
        "memory_challenge_d",
    ]
    found = [task.get("id") for task in tasks]
    if found != expected:
        raise SystemExit(f"unexpected task ids: {found}")
    for task in tasks:
        if not task.get("prompt") and task["id"] not in {"task4", "memory_challenge_d"}:
            raise SystemExit(f"{task['id']} is missing a prompt")
        if not task.get("sessions"):
            raise SystemExit(f"{task['id']} is missing sessions")
        if not task.get("score"):
            raise SystemExit(f"{task['id']} is missing scoring rules")


def validate_fixtures() -> None:
    for fixture in (BASELINE, AML):
        require(fixture / "README.md")
        require(fixture / "app.py")
        require(fixture / "test_app.py")
    if (BASELINE / "AGENTS.md").exists() or (BASELINE / "artifacts").exists():
        raise SystemExit("baseline fixture must not contain AML artifacts")
    require(AML / "AGENTS.md")
    require(AML / "artifacts" / "knowledge" / "intent.yaml")
    require(AML / "artifacts" / "knowledge" / "capability_map.json")
    require(AML / "artifacts" / "knowledge" / "decision_log.md")
    require(AML / "artifacts" / "knowledge" / "handoff_card.md")
    json.loads((AML / "artifacts" / "knowledge" / "capability_map.json").read_text(encoding="utf-8"))
    intent_text = (AML / "artifacts" / "knowledge" / "intent.yaml").read_text(encoding="utf-8")
    for required in (
        "local_only: true",
        "no_telemetry: true",
        "no_shell_execution_feature: true",
        "deterministic_identifiers: true",
    ):
        if required not in intent_text:
            raise SystemExit(f"intent.yaml missing required signal: {required}")
    decision_text = (AML / "artifacts" / "knowledge" / "decision_log.md").read_text(encoding="utf-8")
    for required in ("SQLite was evaluated", "UUIDv4 was rejected", "FeatureRegistry"):
        if required not in decision_text:
            raise SystemExit(f"decision_log.md missing memory challenge signal: {required}")


def main() -> int:
    validate_tasks()
    validate_fixtures()
    print("benchmark definition valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
