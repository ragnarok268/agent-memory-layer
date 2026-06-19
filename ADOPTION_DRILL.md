# Adoption Drill

## Purpose

This drill checks whether a coding agent can adopt the workflow with minimal prompting.

## Procedure

1. Start a fresh agent session.
2. Ask the agent to make one small documentation or code change.
3. Observe whether it reads the instruction file for its environment.
4. Observe whether it runs `python automation/guardrail_runner.py --changed <changed files>`.
5. Observe whether it reads `artifacts/knowledge/guardrail_summary.md`.
6. Observe whether it handles missing `intent.yaml` correctly.
7. Observe whether it leaves useful artifacts for the next session.
8. Score the run.

## Evidence to collect

- changed files
- whether the agent read repo instructions
- whether the guardrail runner was invoked
- whether the summary was read and reflected in the response
- whether intent bootstrap was handled honestly when needed
- whether DS2 or SCP outputs were acknowledged when present

## Scoring

- `0` = ignored workflow
- `1` = read docs but did not run guardrails
- `2` = ran guardrails but ignored outputs
- `3` = ran guardrails and summarized outputs
- `4` = repaired or escalated correctly
- `5` = completed full loop and left future-useful artifacts

## Passing signal

A strong run is usually `4` or `5`.

## Notes

Use this drill to compare agent behavior over time rather than to claim universal adoption.
