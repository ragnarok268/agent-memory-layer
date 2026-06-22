# AML Interrupted Run Rerun Report

This report reruns only AML benchmark runs that were originally classified as incomplete because of timeout, shutdown, or missing completion. It preserves the raw initial execution and writes rerun evidence to separate run directories.

## Interrupted AML Runs Identified

| Original Run | Task | Eligibility Reason | Original Evidence | Rerun Evidence | Rerun Completed | Tests Passed | Intent Violations | Constraint Violations | Classification |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `codex-aml-task3` | `task3` | Original transcript/receipt records shutdown after repeated 600000 ms waits; no completed final agent status. | `benchmarks/codex_context_memory/runs/codex-aml-task3/` | `benchmarks/codex_context_memory/runs/codex-aml-task3-rerun1/` | true | true | 0 | 0 | `success` |
| `codex-aml-memory-challenge-a` | `memory_challenge_a` | Original transcript/receipt records shutdown after repeated 600000 ms waits; no completed final agent status. | `benchmarks/codex_context_memory/runs/codex-aml-memory-challenge-a/` | `benchmarks/codex_context_memory/runs/codex-aml-memory-challenge-a-rerun1/` | false | false | 0 | 0 | `infrastructure_interruption` |
| `codex-aml-memory-challenge-d` | `memory_challenge_d` | Original transcript/receipt records shutdown after repeated 600000 ms waits; no completed final agent status. | `benchmarks/codex_context_memory/runs/codex-aml-memory-challenge-d/` | `benchmarks/codex_context_memory/runs/codex-aml-memory-challenge-d-rerun1/` | true | true | 0 | 0 | `success` |

## Raw Initial Execution

Raw initial results are preserved unchanged in `benchmarks/codex_context_memory/results/results.json`, `benchmarks/codex_context_memory/results/results_table.md`, and original `runs/codex-aml-*` directories.

- Raw AML runs: 12 total, 9 completed according to `BENCHMARK_RESULTS.md`.
- Raw AML tests passed: 11.
- Raw AML intent violations: 0.
- Raw AML prior decision preserved: 100.0% (2/2).

## Completion-Adjusted Execution

Completion-adjusted results are written separately and substitute rerun evidence only for objectively interrupted AML runs.

- Adjusted JSON: `benchmarks/codex_context_memory/results/results_rerun_adjusted.json`
- Adjusted table: `benchmarks/codex_context_memory/results/results_table_rerun_adjusted.md`
- Adjusted AML completed runs: 11/12.
- Adjusted AML tests passed: 11.
- Adjusted AML intent violations: 0.
- Adjusted AML prior decision preserved: 100.0% (3/3).
- Adjusted AML memory artifact consulted: 100.0% (11/11).

## Rerun Outcomes

- `codex-aml-task3-rerun1` completed successfully and passed tests. It implemented local JSON persistence for recent task summaries without recorded intent or constraint violations.
- `codex-aml-memory-challenge-d-rerun1` completed both sessions and passed tests. It reused `FeatureRegistry` and `registry.json`, preserving the existing design pattern without recorded intent or constraint violations.
- `codex-aml-memory-challenge-a-rerun1` did not complete and was shut down again. Its rerun remains classified as `infrastructure_interruption`; it should not be counted as a completed AML success.

## Aggregate Changes

- AML completion changed from 9/12 raw to 11/12 completion-adjusted.
- AML tests passed remained 11 because the still-interrupted Memory Challenge A rerun did not pass post-run tests.
- AML intent and constraint violations remained 0.
- AML prior decision preservation changed from 100.0% (2/2) raw to 100.0% (3/3) adjusted because Memory Challenge D completed and preserved the pattern.
- AML memory artifact consultation changed from 100.0% (9/9) raw to 100.0% (11/11) adjusted among completed AML runs.

## Limitations

- Rerun evidence still uses final agent status summaries; full internal transcripts were not exposed.
- One rerun repeated the interruption, so the adjusted view is still not a fully complete 12/12 AML run set.
- These reruns distinguish some infrastructure interruptions from task failures, but they do not prove general AML superiority.
- Original interrupted evidence remains part of the record and should be reported alongside adjusted metrics.
