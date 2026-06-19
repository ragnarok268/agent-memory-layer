# Event Model

## Purpose

The automation layer needs a small event model so it can react consistently without a human deciding every step.

This repository uses a narrow set of deterministic event labels.

## Event types

### `code_change`

Meaning:

At least one non-doc, non-dependency file changed.

Typical trigger:

- `src/app.py`
- `automation/guardrail_runner.py`
- `tests/test_guardrail_runner.py`

Expected action:

- IA should run if available.
- If `intent.yaml` is missing, draft intent should be created and IA should be marked blocked until intent is approved.

Expected artifacts:

- `artifacts/knowledge/guardrail_summary.json`
- `artifacts/knowledge/guardrail_summary.md`
- `artifacts/knowledge/intent_draft.yaml` when intent is missing
- `artifacts/knowledge/intent_draft.md` when intent is missing

### `dependency_change`

Meaning:

A known dependency manifest or lockfile changed.

Trigger paths:

- `requirements.txt`
- `pyproject.toml`
- `package.json`
- `package-lock.json`
- `pnpm-lock.yaml`
- `yarn.lock`
- `poetry.lock`

Expected action:

- DS2 should run if available.
- the change is also treated as decision-worthy.

Expected artifacts:

- guardrail summary
- SCP draft when relevant

### `import_surface_change`

Meaning:

The diff adds imports associated with meaningful capability expansion.

Trigger examples:

- `import requests`
- `from subprocess import Popen`
- `import subprocess`
- `import socket`
- `import boto3`
- `import openai`
- `import os`

Expected action:

- DS2 should run if available.

Expected artifacts:

- guardrail summary

### `decision_worthy_change`

Meaning:

The change appears important enough to preserve as draft project memory.

Trigger examples:

- dependency files changed
- files under `docs/decisions/` changed
- architecture docs changed
- diff includes phrases such as `decided to`, `rejected`, `tradeoff`, `migration`, `architecture`, `constraint`, `security`, or `local-first`

Expected action:

- generate an SCP-style draft note

Expected artifacts:

- guardrail summary
- `artifacts/knowledge/scp_drafts/*.md`

### `docs_only_change`

Meaning:

All changed files are docs-like files and no decision-worthy signal was found.

Typical trigger:

- `README.md`
- `docs/guide.md`

Expected action:

- no IA
- no DS2
- no SCP draft

Expected artifacts:

- guardrail summary

## Trigger priority

This model allows more than one label at once.

Examples:

- `pyproject.toml` plus `src/app.py` can trigger `dependency_change`, `decision_worthy_change`, and `code_change`
- a Python diff with `import requests` can trigger `code_change` and `import_surface_change`

`docs_only_change` is exclusive in practice and is used only when no stronger signal exists.

## Tradeoffs

### False positives

This thin model may over-classify some changes as decision-worthy.

That is acceptable in v1 because the SCP output is only a draft.

### False negatives

The model may miss subtle architectural or product decisions that are not obvious from paths or simple phrases.

That is also acceptable in v1 because the goal is lightweight automation, not perfect semantic understanding.

## Why deterministic rules first

Deterministic routing is easy to test, easy to explain, and easy for future agents to trust.

This keeps the thin automation layer small and inspectable before trying more advanced detection.
