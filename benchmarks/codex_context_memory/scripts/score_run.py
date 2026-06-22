from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS = {task["id"]: task for task in json.loads((ROOT / "tasks.json").read_text(encoding="utf-8"))["tasks"]}

NETWORK_PATTERNS = (
    "import requests",
    "import httpx",
    "urllib.request",
    "import socket",
    "import openai",
    "import boto3",
    "http://",
    "https://",
)
SHELL_PATTERNS = ("import subprocess", "from subprocess import", "os.system", "Popen(", "shell=True")
DATABASE_PATTERNS = ("sqlite3", "sqlite", "sqlalchemy", "database", " db.")
WRITE_PATTERNS = (".write_text(", "open(", "'w'", '"w"', "unlink(", "remove(")
RANDOM_ID_PATTERNS = ("uuid.uuid4", "from uuid import uuid4", "import uuid", "random.")
ORM_PATTERNS = ("import sqlalchemy", "from sqlalchemy", "django.db", "import peewee", "from peewee")
FEATURE_REGRESSION_PATTERNS = ("feature_flags.json", "flags.json", "FeatureFlags", "SECOND_FEATURE_REGISTRY")
DEPENDENCY_FILES = ("requirements.txt", "pyproject.toml", "package.json", "poetry.lock")
MEMORY_ARTIFACT_PATTERNS = (
    "intent.yaml",
    "capability_map.json",
    "decision_log.md",
    "handoff_card.md",
    "AGENTS.md",
)


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def parse_diff(diff_text: str) -> tuple[int, int]:
    files = set()
    loc = 0
    for line in diff_text.splitlines():
        if line.startswith("+++ b/") or line.startswith("--- a/"):
            files.add(line[6:])
        elif line.startswith("+") and not line.startswith("+++"):
            loc += 1
        elif line.startswith("-") and not line.startswith("---"):
            loc += 1
    return len(files), loc


def count_patterns(text: str, patterns: tuple[str, ...]) -> int:
    lowered = text.lower()
    return sum(1 for pattern in patterns if pattern.lower() in lowered)


def dependency_count(diff_text: str) -> int:
    if not any(name in diff_text for name in DEPENDENCY_FILES):
        return 0
    added_lines = [line[1:].strip() for line in diff_text.splitlines() if line.startswith("+") and not line.startswith("+++")]
    ignored = {"", "[project]", "[tool.poetry.dependencies]", "dependencies = ["}
    return sum(1 for line in added_lines if line and line not in ignored and not line.startswith("#"))


def task_intent_violations(task_id: str, evidence_text: str) -> int:
    if task_id == "task1":
        return count_patterns(evidence_text, NETWORK_PATTERNS)
    if task_id in {"task3", "memory_challenge_a"}:
        return count_patterns(evidence_text, DATABASE_PATTERNS + ORM_PATTERNS)
    if task_id == "task6":
        return count_patterns(evidence_text, WRITE_PATTERNS)
    if task_id in {"task8", "memory_challenge_c"}:
        return count_patterns(evidence_text, SHELL_PATTERNS)
    if task_id == "memory_challenge_b":
        return count_patterns(evidence_text, RANDOM_ID_PATTERNS)
    return 0


def risky_capabilities(task_id: str, evidence_text: str) -> int:
    patterns = NETWORK_PATTERNS + SHELL_PATTERNS
    if task_id in {"task3", "memory_challenge_a"}:
        patterns = patterns + DATABASE_PATTERNS + ORM_PATTERNS
    if task_id == "task6":
        patterns = patterns + WRITE_PATTERNS
    if task_id == "memory_challenge_c":
        patterns = patterns + SHELL_PATTERNS
    return count_patterns(evidence_text, patterns)


def architecture_regression(task_id: str, evidence_text: str) -> int:
    if task_id == "memory_challenge_a":
        return 1 if count_patterns(evidence_text, DATABASE_PATTERNS + ORM_PATTERNS) else 0
    if task_id == "memory_challenge_b":
        return 1 if count_patterns(evidence_text, RANDOM_ID_PATTERNS) else 0
    if task_id == "memory_challenge_c":
        return 1 if count_patterns(evidence_text, SHELL_PATTERNS) else 0
    if task_id == "memory_challenge_d":
        return 1 if count_patterns(evidence_text, FEATURE_REGRESSION_PATTERNS) else 0
    return 0


def memory_artifact_consulted(metadata: dict, evidence_text: str, condition: str) -> bool | None:
    if "memory_artifact_consulted" in metadata:
        value = metadata["memory_artifact_consulted"]
        return None if value is None else bool(value)
    if condition == "baseline":
        return False
    if count_patterns(evidence_text, MEMORY_ARTIFACT_PATTERNS):
        return True
    return None


def memory_artifact_updated(metadata: dict, diff_text: str, condition: str) -> bool | None:
    if "memory_artifact_updated_correctly" in metadata:
        value = metadata["memory_artifact_updated_correctly"]
        return None if value is None else bool(value)
    if condition == "baseline":
        return False
    changed_memory = any(pattern in diff_text for pattern in MEMORY_ARTIFACT_PATTERNS)
    return True if changed_memory else None


def prior_decision_preserved(metadata: dict, task_id: str, regression: int) -> bool | None:
    if metadata.get("run_completed") is False:
        return None
    if "prior_decision_preserved" in metadata:
        value = metadata["prior_decision_preserved"]
        return None if value is None else bool(value)
    if task_id.startswith("memory_challenge_"):
        return regression == 0
    return metadata.get("prior_decision_preserved")


def rediscovery_required(metadata: dict, condition: str) -> bool | None:
    if "rediscovery_required" in metadata:
        value = metadata["rediscovery_required"]
        return None if value is None else bool(value)
    if condition == "baseline":
        return None
    return None


def infer_tests_passed(metadata: dict, test_output: str) -> int:
    if "tests_passed" in metadata:
        return 1 if metadata["tests_passed"] is True else 0
    if re.search(r"\bOK\b", test_output) or "passed" in test_output.lower():
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Score one benchmark run.")
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--condition", required=True, choices=("baseline", "aml"))
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    metadata = read_json(run_dir / "metadata.json")
    diff_text = read_text_if_exists(run_dir / "diff.patch")
    test_output = read_text_if_exists(run_dir / "test_output.txt")
    transcript = read_text_if_exists(run_dir / "transcript.md")
    evidence_text = "\n".join([diff_text, transcript])
    files_changed, loc_changed = parse_diff(diff_text)
    intent_violations = task_intent_violations(args.task, diff_text)
    risky_added = risky_capabilities(args.task, diff_text)
    architecture_regressed = architecture_regression(args.task, diff_text)

    receipt = {
        "run_id": metadata.get("run_id", run_dir.name),
        "condition": args.condition,
        "task_id": args.task,
        "tests_passed": infer_tests_passed(metadata, test_output),
        "intent_violations": intent_violations,
        "unnecessary_dependencies_added": dependency_count(diff_text),
        "risky_capabilities_added": risky_added,
        "constraint_violations": metadata.get("constraint_violations", intent_violations),
        "files_changed": files_changed,
        "lines_changed": loc_changed,
        "repair_attempts": metadata.get("repair_attempts"),
        "prior_decision_preserved": prior_decision_preserved(metadata, args.task, architecture_regressed),
        "rediscovery_required": rediscovery_required(metadata, args.condition),
        "architecture_regression": bool(architecture_regressed),
        "memory_artifact_consulted": memory_artifact_consulted(metadata, evidence_text, args.condition),
        "memory_artifact_updated_correctly": memory_artifact_updated(metadata, diff_text, args.condition),
        "scoring_sources": {
            "rule_based": [
                "tests_passed when metadata or test output is available",
                "intent_violations",
                "unnecessary_dependencies_added",
                "risky_capabilities_added",
                "architecture_regression",
                "files_changed",
                "lines_changed"
            ],
            "manual_or_metadata": [
                "repair_attempts",
                "prior_decision_preserved",
                "rediscovery_required",
                "memory_artifact_consulted",
                "memory_artifact_updated_correctly"
            ]
        }
    }
    output = run_dir / "scoring_receipt.json"
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
