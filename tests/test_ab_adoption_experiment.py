import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
EXPERIMENT_DIR = ROOT_DIR / "experiments" / "ab_adoption"
RESULTS_DIR = EXPERIMENT_DIR / "results"
SUMMARY_PATH = EXPERIMENT_DIR / "results_summary.md"
RUNTIME_TMP = ROOT_DIR / "tests" / "_runtime_tmp"


def snapshot_results_state() -> tuple[Path | None, str | None]:
    backup_dir = RUNTIME_TMP / f"results_backup_{uuid.uuid4().hex}"
    summary_text = SUMMARY_PATH.read_text(encoding="utf-8") if SUMMARY_PATH.exists() else None
    backup_dir.parent.mkdir(parents=True, exist_ok=True)
    if RESULTS_DIR.exists():
        shutil.copytree(RESULTS_DIR, backup_dir)
        return backup_dir, summary_text
    return None, summary_text


def restore_results_state(backup_dir: Path | None, summary_text: str | None) -> None:
    shutil.rmtree(RESULTS_DIR, ignore_errors=True)
    if backup_dir and backup_dir.exists():
        shutil.copytree(backup_dir, RESULTS_DIR)
    if summary_text is None:
        if SUMMARY_PATH.exists():
            SUMMARY_PATH.unlink()
    else:
        SUMMARY_PATH.write_text(summary_text, encoding="utf-8")


def test_experiment_docs_exist():
    required = [
        EXPERIMENT_DIR / "README.md",
        EXPERIMENT_DIR / "BASELINE_REPO_SPEC.md",
        EXPERIMENT_DIR / "WORKFLOW_REPO_SPEC.md",
        EXPERIMENT_DIR / "TEST_TASKS.md",
        EXPERIMENT_DIR / "SCORING_RUBRIC.md",
        EXPERIMENT_DIR / "RUN_LOG_TEMPLATE.md",
        EXPERIMENT_DIR / "EXPERIMENT_CHECKLIST.md",
        EXPERIMENT_DIR / "timed_run.py",
        EXPERIMENT_DIR / "analyze_results.py",
    ]
    for path in required:
        assert path.exists(), f"Missing experiment file: {path}"


def test_rubric_mentions_baseline_and_workflow_conditions():
    text = (EXPERIMENT_DIR / "SCORING_RUBRIC.md").read_text(encoding="utf-8").lower()
    assert "baseline" in text
    assert "workflow" in text


def test_at_least_five_tasks_are_documented():
    text = (EXPERIMENT_DIR / "TEST_TASKS.md").read_text(encoding="utf-8")
    assert text.count("## Task") >= 5


def test_run_log_template_contains_required_fields():
    text = (EXPERIMENT_DIR / "RUN_LOG_TEMPLATE.md").read_text(encoding="utf-8")
    for field in (
        "run_id",
        "run_start_timestamp",
        "run_end_timestamp",
        "elapsed_seconds",
        "guardrail_runtime_seconds",
        "active_editing_seconds",
        "review_seconds",
        "repo_condition",
        "agent_name",
        "task_id",
        "total_score",
        "subscores",
        "notes",
        "failures",
        "artifacts_created",
        "guardrail_ran",
        "metrics",
        "unnecessary_dependencies",
        "repeated_mistakes",
        "ignored_constraints",
        "repair_iterations",
        "artifact_reads",
        "artifact_writes",
    ):
        assert field in text


def test_experiment_checklist_mentions_timing_and_consistency():
    text = (EXPERIMENT_DIR / "EXPERIMENT_CHECKLIST.md").read_text(encoding="utf-8").lower()
    assert "fresh session started" in text
    assert "same model and version" in text
    assert "timing started before the agent task began" in text
    assert "timing stopped after the final artifact or run log was written" in text
    assert "timed_run.py --manual" in text


def test_experiment_docs_do_not_overclaim_results():
    for path in EXPERIMENT_DIR.glob("*.md"):
        lowered = path.read_text(encoding="utf-8").lower()
        assert "proven before testing" not in lowered
        assert "this proves the workflow works" not in lowered


def test_analysis_script_handles_no_results_case():
    backup_dir, summary_text = snapshot_results_state()
    try:
        shutil.rmtree(RESULTS_DIR, ignore_errors=True)
        if SUMMARY_PATH.exists():
            SUMMARY_PATH.unlink()

        completed = subprocess.run(
            [sys.executable, str(EXPERIMENT_DIR / "analyze_results.py")],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=False,
        )

        assert completed.returncode == 0
        assert "No result logs found" in completed.stdout
        assert SUMMARY_PATH.exists()
        summary = SUMMARY_PATH.read_text(encoding="utf-8")
        assert "No result logs were found." in summary
        assert "Metric| Baseline| Workflow" in summary
    finally:
        restore_results_state(backup_dir, summary_text)


def test_analysis_script_averages_sample_logs_and_writes_summary():
    backup_dir, summary_text = snapshot_results_state()
    shutil.rmtree(RESULTS_DIR, ignore_errors=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        samples = [
            {
                "run_id": "baseline-1",
                "run_start_timestamp": "2026-06-17T12:00:00Z",
                "run_end_timestamp": "2026-06-17T12:05:00Z",
                "elapsed_seconds": 300,
                "guardrail_runtime_seconds": None,
                "active_editing_seconds": 220,
                "review_seconds": 40,
                "repo_condition": "baseline",
                "agent_name": "codex",
                "task_id": "task_1",
                "total_score": 2,
                "subscores": {
                    "constraint_adherence": 2,
                    "dependency_discipline": 2,
                    "artifact_usage": 0,
                    "self_repair_behavior": 1,
                    "handoff_quality": 1,
                    "human_review_usefulness": 2,
                },
                "notes": "Ignored most workflow context.",
                "failures": ["ignored project context"],
                "artifacts_created": [],
                "guardrail_ran": False,
                "metrics": {
                    "unnecessary_dependencies": 1,
                    "repeated_mistakes": 1,
                    "ignored_constraints": 1,
                    "repair_iterations": 0,
                    "artifact_reads": 0,
                    "artifact_writes": 0,
                },
            },
            {
                "run_id": "workflow-1",
                "run_start_timestamp": "2026-06-17T12:00:00Z",
                "run_end_timestamp": "2026-06-17T12:08:00Z",
                "elapsed_seconds": 480,
                "guardrail_runtime_seconds": 25,
                "active_editing_seconds": 300,
                "review_seconds": 60,
                "repo_condition": "workflow",
                "agent_name": "codex",
                "task_id": "task_1",
                "total_score": 4,
                "subscores": {
                    "constraint_adherence": 4,
                    "dependency_discipline": 5,
                    "artifact_usage": 4,
                    "self_repair_behavior": 3,
                    "handoff_quality": 4,
                    "human_review_usefulness": 4,
                },
                "notes": "Used workflow artifacts.",
                "failures": ["did not promote intent draft"],
                "artifacts_created": ["artifacts/knowledge/guardrail_summary.md"],
                "guardrail_ran": True,
                "metrics": {
                    "unnecessary_dependencies": 0,
                    "repeated_mistakes": 0,
                    "ignored_constraints": 0,
                    "repair_iterations": 1,
                    "artifact_reads": 3,
                    "artifact_writes": 2,
                },
            },
        ]
        for sample in samples:
            path = RESULTS_DIR / f"{sample['run_id']}.json"
            path.write_text(json.dumps(sample, indent=2), encoding="utf-8")
        (RESULTS_DIR / "workflow-1.timing.json").write_text(
            json.dumps(
                {
                    "run_id": "workflow-1",
                    "repo_condition": "workflow",
                    "agent_name": "codex",
                    "task_id": "task_1",
                    "run_start_timestamp": "2026-06-17T12:00:00Z",
                    "run_end_timestamp": "2026-06-17T12:08:00Z",
                    "elapsed_seconds": 480,
                    "command": "python -m pytest",
                    "exit_code": 0,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        completed = subprocess.run(
            [sys.executable, str(EXPERIMENT_DIR / "analyze_results.py")],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=False,
        )

        assert completed.returncode == 0
        assert SUMMARY_PATH.exists()
        summary = SUMMARY_PATH.read_text(encoding="utf-8")
        assert "`baseline`: 1" in summary
        assert "`workflow`: 1" in summary
        assert "`baseline`: 2.0" in summary
        assert "`workflow`: 4.0" in summary
        assert "Avg Time (s)| 300.0| 480.0" in summary
        assert "Median Time (s)| 300.0| 480.0" in summary
        assert "baseline-1 (300.0s)" in summary
        assert "workflow-1 (480.0s)" in summary
        assert "unnecessary_dependencies: 1.0" in summary
        assert "artifact_reads: 3.0" in summary
    finally:
        restore_results_state(backup_dir, summary_text)
