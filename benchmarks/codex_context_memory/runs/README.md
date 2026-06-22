# Run Evidence

Store benchmark run evidence here.

Recommended structure:

```text
runs/
  codex-baseline-task1/
    transcript.md
    diff.patch
    test_output.txt
    metadata.json
    scoring_receipt.json
```

`metadata.json` may include:

```json
{
  "run_id": "codex-baseline-task1",
  "condition": "baseline",
  "task_id": "task1",
  "tests_passed": true,
  "constraint_violations": 0,
  "repair_attempts": 0,
  "prior_decision_preserved": null,
  "rediscovery_required": null,
  "memory_artifact_consulted": false,
  "memory_artifact_updated_correctly": false,
  "notes": ""
}
```

Do not invent missing evidence. Use `null` when a value is unknown.
