# Codex Context Memory Benchmark

This benchmark measures whether repository-local memory improves Codex behavior across fresh sessions on context-sensitive coding tasks compared with a no-memory baseline.

It is a controlled paired evaluation, not a claim of general model improvement.

Allowed interpretation after real runs:

> In a small paired Codex evaluation, Agent Memory Layer improved context reuse and reduced intent/capability drift versus a no-memory baseline.

Do not use this benchmark to claim that Agent Memory Layer makes Codex better overall.

## Conditions

Baseline condition:

- Same sample codebase.
- Normal `README.md` guidance only.
- No Agent Memory Layer artifacts.

AML condition:

- Same sample codebase.
- Repository-local memory artifacts:
- `AGENTS.md`
- `artifacts/knowledge/intent.yaml`
- `artifacts/knowledge/capability_map.json`
- `artifacts/knowledge/decision_log.md`
- `artifacts/knowledge/handoff_card.md`

Task prompts must be identical between conditions except for the presence of AML artifacts.

The benchmark emphasizes persistence of prior decisions, intent preservation, architectural consistency, and reduction of rediscovery. It does not measure broad model intelligence or general coding ability.

## Directory Map

- `tasks.json`: the fixed benchmark tasks, including persistent-memory challenge tasks.
- `SCORING.md`: metric definitions and rule-based scoring guidance.
- `fixtures/baseline_repo/`: no-memory sample repo.
- `fixtures/aml_repo/`: same sample repo with AML artifacts.
- `scripts/prepare_trials.py`: creates clean paired trial workdirs.
- `scripts/run_fixture_tests.py`: validates the fixture repos.
- `scripts/score_run.py`: creates a rule-based scoring receipt for one run.
- `scripts/collect_metrics.py`: aggregates receipts into result tables.
- `runs/`: place transcripts, diffs, test output, and scoring receipts here.
- `results/`: generated aggregate tables and JSON summaries.
- `REPORT_TEMPLATE.md`: template for a human-readable result report.

## How To Run

From the repository root:

```bash
python benchmarks/codex_context_memory/scripts/validate_benchmark.py
python benchmarks/codex_context_memory/scripts/run_fixture_tests.py
python benchmarks/codex_context_memory/scripts/prepare_trials.py
```

Then run each task in both conditions using fresh agent context:

```text
benchmarks/codex_context_memory/trial_workdirs/task1/baseline
benchmarks/codex_context_memory/trial_workdirs/task1/aml
```

Preserve evidence for each run under:

```text
benchmarks/codex_context_memory/runs/<run-id>/
```

Recommended evidence files:

- `transcript.md`
- `diff.patch`
- `test_output.txt`
- `metadata.json`
- `scoring_receipt.json`

After a run, score it:

```bash
python benchmarks/codex_context_memory/scripts/score_run.py --task task1 --condition baseline --run-dir benchmarks/codex_context_memory/runs/codex-baseline-task1
```

Then aggregate:

```bash
python benchmarks/codex_context_memory/scripts/collect_metrics.py
```

## What The Benchmark Measures

The metrics are intentionally narrow:

- tests passed
- intent violations
- unnecessary dependencies added
- risky capabilities added
- constraint violations
- files changed
- lines changed
- repair attempts
- prior decision preserved
- rediscovery required
- architecture regression
- memory artifact consulted
- memory artifact updated correctly

The benchmark does not measure general productivity, model intelligence, or enterprise readiness.

## Memory Challenge Tasks

The benchmark includes four tasks where the correct behavior depends on information that is not obvious from source code alone:

- Memory Challenge A: preserve the rejected SQLite architecture decision.
- Memory Challenge B: preserve the deterministic ID requirement and avoid UUIDv4.
- Memory Challenge C: preserve the rejected shell-execution safety boundary.
- Memory Challenge D: preserve the `FeatureRegistry` and `registry.json` feature-flag pattern across fresh sessions.

These tasks should be run in fresh sessions so the AML condition can only benefit from repository-local artifacts, not conversational carryover.

## Repeatability Notes

- Use fresh agent context for every condition.
- Do not reuse transcripts or memory across baseline and AML runs.
- Do not change the task prompts between conditions.
- Do not alter the task set during a run.
- Record uncertainty in `metadata.json` rather than inventing measurements.
