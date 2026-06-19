# Run Log Template

Store each run as JSON under `experiments/ab_adoption/results/`.

You can capture timing automatically with:

```text
python experiments/ab_adoption/timed_run.py --condition workflow --agent Codex --task task1 --run-id codex-workflow-task1-rerun2 --manual --merge-into experiments/ab_adoption/results/codex-workflow-task1-rerun2.json
```

Or for a single wrapped command:

```text
python experiments/ab_adoption/timed_run.py --condition baseline --agent Codex --task smoke --run-id smoke-test --command "python -c \"print('ok')\""
```

Required fields:

```json
{
  "run_id": "2026-06-17-codex-task1-workflow",
  "run_start_timestamp": "2026-06-17T12:00:00Z",
  "run_end_timestamp": "2026-06-17T12:08:30Z",
  "elapsed_seconds": 510,
  "guardrail_runtime_seconds": null,
  "active_editing_seconds": null,
  "review_seconds": null,
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
    "human_review_usefulness": 4
  },
  "notes": "Agent read the workflow files and ran the guardrail runner.",
  "failures": [
    "Did not promote the intent draft."
  ],
  "artifacts_created": [
    "artifacts/knowledge/guardrail_summary.md"
  ],
  "guardrail_ran": true,
  "metrics": {
    "unnecessary_dependencies": 0,
    "repeated_mistakes": 0,
    "ignored_constraints": 0,
    "repair_iterations": 1,
    "artifact_reads": 3,
    "artifact_writes": 2
  }
}
```

Notes:

- `run_start_timestamp` and `run_end_timestamp` should be UTC timestamps when available
- `elapsed_seconds` should reflect total run duration when measured, preferably from `timed_run.py`
- `guardrail_runtime_seconds`, `active_editing_seconds`, and `review_seconds` are optional and can be `null`
- `repo_condition` should be `baseline` or `workflow`
- `guardrail_ran` can be `false` for baseline runs
- `failures` can be empty
- `artifacts_created` can be empty
- `metrics` is optional; include only counters you actually measured
- timing-only evidence files may also exist as `results/<run-id>.timing.json`; the analyzer ignores those unless timing is merged into the scored run log
