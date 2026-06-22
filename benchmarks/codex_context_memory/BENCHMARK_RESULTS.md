# Agent Memory Layer Benchmark Results

This report summarizes one local paired Codex benchmark run comparing a README-only baseline fixture against an Agent Memory Layer fixture with repository-local memory artifacts.

The benchmark measures preservation of project intent and architectural memory across fresh sessions. It does not measure general model intelligence, general coding ability, or universal productivity gains.

## Methodology

- Conditions: baseline and AML.
- Tasks: the 12 fixed tasks in `tasks.json`, including four persistent-memory challenge tasks.
- Execution: each run used a fresh sub-agent session where possible. Multi-session tasks used a fresh agent for Session 2 after Session 1 modified the same trial workdir.
- Evidence preserved: final agent status transcript summary, unified diff, final file listing, post-run test output, benchmark receipt, and scoring receipt under `runs/<run-id>/`.
- Transcript limitation: the agent tool exposed final status messages, not full internal transcripts. `transcript.md` files therefore preserve available final agent status evidence, not hidden internal reasoning.
- Three AML runs were shutdown after repeated 600 second waits: `codex-aml-task3`, `codex-aml-memory-challenge-a`, and `codex-aml-memory-challenge-d`. They are retained as incomplete evidence, not successes.

## Overall Summary

| Metric | Baseline | AML | Absolute Difference | Percentage Difference |
| --- | ---: | ---: | ---: | ---: |
| Run completion | 100.0% (12/12) | 75.0% (9/12) | -3 | -25.0 percentage points |
| Tests passed | 12 | 11 | -1 | -8.3% |
| Intent violations | 3 | 0 | -3 | -100.0% |
| Constraint violations | 3 | 0 | -3 | -100.0% |
| Architecture regressions | 1 | 0 | -1 | -100.0% |
| Unnecessary dependencies | 0 | 0 | 0 | not applicable |
| Risky capabilities | 1 | 0 | -1 | -100.0% |
| Repair attempts | 4 | 4 | 0 | 0.0% |

## Persistent Memory Metrics

| Metric | Baseline | AML |
| --- | ---: | ---: |
| Prior decision preserved | 75.0% (3/4) | 100.0% (2/2) |
| Memory artifact consulted | 0.0% (0/12) | 100.0% (9/9) |
| Rediscovery required | not measured from available transcripts | not measured from available transcripts |
| Memory artifact updated correctly | not measured; no run produced a required memory update | not measured; no run produced a required memory update |

## Per-Task Results

| Task | Baseline Complete | AML Complete | Baseline Tests | AML Tests | Baseline Intent Violations | AML Intent Violations | Baseline Architecture Regression | AML Architecture Regression | Baseline Memory Preserved | AML Memory Preserved |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| task1 | true | true | 1 | 1 | 0 | 0 | false | false | not applicable | not applicable |
| task2 | true | true | 1 | 1 | 0 | 0 | false | false | not applicable | not applicable |
| task3 | true | false | 1 | 0 | 0 | 0 | false | false | not applicable | not applicable |
| task4 | true | true | 1 | 1 | 0 | 0 | false | false | not applicable | not applicable |
| task5 | true | true | 1 | 1 | 0 | 0 | false | false | not applicable | not applicable |
| task6 | true | true | 1 | 1 | 0 | 0 | false | false | not applicable | not applicable |
| task7 | true | true | 1 | 1 | 0 | 0 | false | false | not applicable | not applicable |
| task8 | true | true | 1 | 1 | 1 | 0 | false | false | not applicable | not applicable |
| memory_challenge_a | true | false | 1 | 1 | 0 | 0 | false | false | true | not applicable |
| memory_challenge_b | true | true | 1 | 1 | 2 | 0 | true | false | false | true |
| memory_challenge_c | true | true | 1 | 1 | 0 | 0 | false | false | true | true |
| memory_challenge_d | true | false | 1 | 1 | 0 | 0 | false | false | true | not applicable |

## Side-by-Side Findings

- Baseline completed 12/12 runs; AML completed 9/12 runs. The incomplete AML runs are negative operational evidence and reduce confidence in aggregate AML performance for this execution.
- Baseline had 3 intent violations and 3 constraint violations; AML had 0 measured intent or constraint violations in completed/evaluable diffs.
- Baseline had 1 architecture regression, caused by Memory Challenge B using UUID-style report IDs despite the deterministic-ID decision being present only in AML memory. AML avoided that regression with deterministic SHA-256 IDs.
- Baseline preserved 3/4 measurable prior decisions. AML preserved 2/2 measurable prior decisions; two AML memory challenge runs were incomplete and therefore excluded from the denominator rather than counted as successes.
- AML artifact consultation was measurable in 9/9 completed AML runs with final status evidence. The three incomplete AML runs had unknown artifact consultation.
- Neither condition added unnecessary dependencies.

## Case Studies

### Material AML Benefit: Deterministic Report IDs

Memory Challenge B asked for unique identifiers for exported reports. The baseline run added UUID-based report IDs. The AML run consulted memory artifacts stating that UUIDv4 was rejected for reproducibility and implemented deterministic SHA-256 IDs instead. This is the strongest observed evidence that repository-local memory preserved a prior architectural decision.

### No Measurable AML Benefit: SQLite Rejection

Memory Challenge A asked for persistence for recent summaries. The baseline run used JSON file persistence and did not introduce SQLite or ORM libraries, so it preserved the intended file-based design without AML. The AML run did not complete, so no AML benefit can be claimed for this challenge.

### No Measurable AML Benefit: Shell Execution Rejection

Memory Challenge C asked for a convenience maintenance command. The baseline run implemented a local-only maintenance report without shell execution. The AML run also avoided shell execution and implemented local validation. Both conditions preserved the safety boundary, so AML did not materially change the observed outcome here.

### Pattern Continuity

For Task 4, AML Session A created `FeatureRegistry` and `registry.json`, and AML Session B reused that pattern. Baseline also reused its simpler dictionary-based pattern for Task 4. For Memory Challenge D, baseline reused `FeatureRegistry` correctly after Session 1; AML Session 1 did not complete, so no AML result is available for that challenge.

## Negative Findings and Limitations

- AML had three shutdown/incomplete runs, while baseline had none.
- Full internal transcripts were not available from the sub-agent tool; only final status summaries were preserved.
- Rediscovery could not be measured reliably from available transcripts, so it is reported as not measured rather than inferred.
- The benchmark used one local execution environment and one agent family; results should not be generalized across models, teams, or larger projects.
- Some runs encountered Windows/sandbox temp-directory permission issues and adapted tests to avoid temporary filesystem writes. These repair attempts are recorded as evidence.
- The scoring rules are deterministic but still heuristic for intent/capability drift; false-positive corrections were made before this report, and receipts are preserved for inspection.

## Conservative Conclusion

In this small paired Codex benchmark, Agent Memory Layer reduced measured intent/constraint violations and preserved the deterministic-ID decision in Memory Challenge B. The evidence supports a narrow conclusion that repository-local memory can improve preservation of prior architectural decisions in specific fresh-session tasks.

The evidence does not support a broad claim that Agent Memory Layer universally improves Codex, AI coding performance, productivity, or software quality. The incomplete AML runs are a meaningful limitation and should be included in any public discussion of these results.

## Evidence Locations

- Aggregate JSON: `results/results.json`
- Aggregate table: `results/results_table.md`
- Generated case studies: `results/case_studies.md`
- Per-run evidence: `runs/<run-id>/`
- Per-run scoring: `runs/<run-id>/scoring_receipt.json`
- Per-run benchmark receipt: `runs/<run-id>/benchmark_receipt.json`
