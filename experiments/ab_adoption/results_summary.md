# A/B Adoption Results

## Compact Comparison

Metric| Baseline| Workflow
---|---|---
Runs| 11| 11
Avg Score| 2.91| 4.55
Avg Time (s)| 38.68| 56.37
Median Time (s)| 19.18| 22.32
Avg Constraint Score| 3.82| 4.0
Avg Dependency Score| 4.73| 5.0
Avg Artifact Usage| 0.0| 4.18
Avg Self Repair| 1.91| 3.91

## Count By Condition

- `baseline`: 11
- `workflow`: 11

## Average Total Score By Condition

- `baseline`: 2.91
- `workflow`: 4.55

## Timing By Condition

- `baseline` average elapsed seconds: 38.68
- `baseline` median elapsed seconds: 19.18
- `baseline` fastest run: codex-baseline-task5-rerun2 (0.47s)
- `baseline` slowest run: baseline-1 (300.0s)
- `workflow` average elapsed seconds: 56.37
- `workflow` median elapsed seconds: 22.32
- `workflow` fastest run: codex-workflow-task4-rerun2 (0.69s)
- `workflow` slowest run: workflow-1 (480.0s)

## Average Subscores By Condition

- `baseline`:
  - constraint_adherence: 3.82
  - dependency_discipline: 4.73
  - artifact_usage: 0.0
  - self_repair_behavior: 1.91
  - handoff_quality: 1.18
  - human_review_usefulness: 2.0
- `workflow`:
  - constraint_adherence: 4.0
  - dependency_discipline: 5.0
  - artifact_usage: 4.18
  - self_repair_behavior: 3.91
  - handoff_quality: 4.0
  - human_review_usefulness: 4.0

## Average Reliability Metrics By Condition

- `baseline`:
  - unnecessary_dependencies: 0.09
  - repeated_mistakes: 0.09
  - ignored_constraints: 0.09
  - repair_iterations: 0.0
  - artifact_reads: 0.0
  - artifact_writes: 0.0
- `workflow`:
  - unnecessary_dependencies: 0.0
  - repeated_mistakes: 0.0
  - ignored_constraints: 0.0
  - repair_iterations: 0.09
  - artifact_reads: 3.91
  - artifact_writes: 2.36

## Common Failures

- `baseline`:
  - ignored project context: 1
- `workflow`:
  - did not promote intent draft: 1
