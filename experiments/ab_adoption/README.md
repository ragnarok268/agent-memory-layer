# A/B Adoption Experiment

This folder defines a repeatable baseline-versus-workflow experiment for testing whether AI coding agents behave better when a repository includes AI-native engineering knowledge artifacts.

Conditions:

- Repo A: baseline repo with only normal project files and README guidance
- Repo B: workflow-enabled repo with minimal agent instructions, guardrail automation, intent handling, and preserved artifacts

This is an experiment, not proof.

Timing matters here because one of the open questions is whether workflow artifacts improve behavior enough to justify any extra overhead. Timing helps compare conditions, but it does not prove quality by itself.

Use this folder to:

1. create two small comparable repos
2. run the same tasks against both conditions
3. score the runs with the same rubric
4. compare the results with `analyze_results.py`

Key files:

- `BASELINE_REPO_SPEC.md`
- `WORKFLOW_REPO_SPEC.md`
- `TEST_TASKS.md`
- `SCORING_RUBRIC.md`
- `RUN_LOG_TEMPLATE.md`
- `timed_run.py`
- `analyze_results.py`

Expected results storage:

- `experiments/ab_adoption/results/*.json`
- `experiments/ab_adoption/results_summary.md`

Generated workspaces:

- `trial_templates/` contains the durable fixture specs used to create clean trial repos
- `trial_runs*` directories are disposable generated workspaces and should not be treated as source documentation

Timing helper:

- `timed_run.py` writes per-run timing evidence to `results/<run-id>.timing.json`
- use `--command` when the run can be wrapped as one local command
- use `--manual` for interactive Codex sessions
- use `--merge-into` to update an existing scored run log with the captured timing fields

Suggested workflow:

1. Build the baseline repo from `BASELINE_REPO_SPEC.md`.
2. Build the workflow repo from `WORKFLOW_REPO_SPEC.md`.
3. Run the task set in `TEST_TASKS.md` with the same agent and comparable prompts.
4. Start timing with `python experiments/ab_adoption/timed_run.py`.
5. Record each run with `RUN_LOG_TEMPLATE.md`.
6. Stop timing after the final artifact or run log is written.
7. Convert or save scored run logs as JSON in `results/`.
8. Run `python experiments/ab_adoption/analyze_results.py`.

Timing logs and scored run logs answer different questions:

- timing logs capture how long a run took and whether the wrapped command exited cleanly
- scored run logs capture quality, constraint adherence, artifact use, and handoff value
- merge timing into scored logs when you want the analyzer to compare time and score together

Reset guidance:

- regenerate trial workspaces from `trial_templates/` before a fresh batch
- avoid reusing dirty task repos across conditions
- keep old result logs by moving them to an archive folder when you want the analyzer to focus on a rerun batch
