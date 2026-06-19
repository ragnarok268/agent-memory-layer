# Baseline Repo Spec

## Purpose

Define a small comparison repo that does not include workflow-aware agent support.

## Condition name

`baseline`

## Repo contents

- `README.md`
- one source file
- one test file

Example shape:

```text
baseline-app/
  README.md
  app.py
  test_app.py
```

## Guidance style

Normal human-facing README guidance only.

No:

- `AGENTS.md`
- guardrail runner
- intent artifact
- guardrail summary
- SCP draft
- prior decision artifact

## Suggested app

A tiny local note formatter or task list app with one or two simple functions.

## Constraints to mention in README

- keep the app local-first
- avoid unnecessary dependencies
- keep behavior easy to test

## Why this condition exists

This condition checks how an agent behaves when useful project context exists only as ordinary documentation and not as workflow-aware artifacts.
