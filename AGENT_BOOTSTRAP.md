# Agent Bootstrap

## Read this first

Before modifying this repository, an AI agent should read:

1. `README.md`
2. `WORKFLOW.md`
3. `AGENTS.md`
4. the latest files under `artifacts/knowledge/` if they exist

The goal is to load existing workflow memory before making new changes.

## Minimal working loop

1. Read the current task and repo instructions.
2. Inspect existing knowledge artifacts if present.
3. Make a small deterministic change.
4. Run `python automation/guardrail_runner.py --changed <files>`.
5. If tests exist, run `python -m pytest`.
6. Review the generated summaries before finishing.

## When to run checks

Run the guardrail runner after meaningful code or docs changes.

The runner decides which checks are relevant:

- IA for code changes
- DS2 for dependency or import surface changes
- SCP draft generation for decision-worthy changes
- intent draft generation when IA is requested but `intent.yaml` is missing

The agent should not guess which one to run first.

The runner is the router.

## How to repair after IA failure

If IA is requested but `intent.yaml` is missing:

1. review `artifacts/knowledge/intent_draft.yaml`
2. review `artifacts/knowledge/intent_draft.md`
3. confirm or correct the draft
4. promote it to `intent.yaml` when approved
5. rerun the guardrail runner

If IA is installed and returns a failing result after `intent.yaml` exists:

1. read the IA output
2. identify the drift or constraint violation
3. repair the code
4. rerun the guardrail runner
5. rerun tests if needed

Do not claim IA proves correctness.

Treat it as verification evidence about intent alignment.

## How to react to DS2 findings

If DS2 runs and shows capability or dependency expansion:

1. check whether the change was actually necessary
2. prefer reusing existing capability when possible
3. explain the reason for the dependency or import change
4. leave the evidence in the summary for human review

Do not treat DS2 as a safety guarantee.

## How to use SCP drafts

If the runner generates an SCP-style draft:

1. read the draft
2. keep it as a draft summary unless a human or project process approves preservation
3. use it to explain the suspected decision, constraint, or tradeoff

Do not auto-promote the draft to approved project memory.

## Why this bootstrap is small

Agents should not need a long custom ritual to work in this repo.

The point is to make future work easier with minimal prompting and minimal context bloat.
