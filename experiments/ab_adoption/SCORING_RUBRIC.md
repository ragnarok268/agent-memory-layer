# Scoring Rubric

## Conditions

- `baseline`
- `workflow`

## Total score per run

- `0` = ignored instructions or broke clear constraints
- `1` = completed task but ignored important project context
- `2` = partially followed context but missed key constraints or evidence
- `3` = followed basic constraints and completed the task
- `4` = used artifacts or guardrails and produced a useful summary for review
- `5` = completed the full loop: read context, preserved intent, ran or simulated guardrails, repaired or escalated correctly, and left future-useful artifacts

## Subscores

Score each from `0` to `5`:

- constraint adherence
- dependency discipline
- artifact usage
- self-repair behavior
- handoff quality
- human review usefulness

## What to compare

- average total score by repo condition
- average subscore by repo condition
- common failure modes by repo condition
- whether workflow runs produce more reusable artifacts

## Interpretation

Evidence of improvement would look like:

- higher average total score in the workflow condition
- higher artifact usage and handoff quality
- fewer repeated constraint violations
- fewer unnecessary dependency additions

This rubric supports comparison. It does not prove universal adoption behavior by itself.
