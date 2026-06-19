# Automation README

## Purpose

This directory contains a thin automation proof of concept for the IA + DS2 + SCP workflow.

It is install-free and uses the Python standard library only.

## Files

- `event_classifier.py`
- `guardrail_runner.py`
- `intent_bootstrap.py`
- `scp_draft.py`

## What it does

The runner:

- inspects changed paths
- optionally inspects a diff file
- classifies the event
- decides whether IA, DS2, or SCP draft behavior is relevant
- creates an intent draft automatically when IA is needed but `intent.yaml` is missing
- tries to call `ia check` and `ds2 scan .` only if those tools are installed
- writes summaries under `artifacts/knowledge/`

## Example usage

```bash
python automation/guardrail_runner.py --changed README.md src/app.py
python automation/guardrail_runner.py --changed pyproject.toml src/app.py
python automation/guardrail_runner.py --changed docs/ARCHITECTURE.md --diff-file sample.diff
```

## Expected outputs

- `artifacts/knowledge/guardrail_summary.json`
- `artifacts/knowledge/guardrail_summary.md`
- `artifacts/knowledge/intent_draft.yaml` when intent bootstrap is needed
- `artifacts/knowledge/intent_draft.md` when intent bootstrap is needed
- `artifacts/knowledge/scp_drafts/` when a decision-worthy draft is generated

## How to test

```bash
python -m pytest
```

If `pytest` is not installed, install it locally first or run the workflow in CI where the test dependency is installed.

## Notes

- missing IA or DS2 is reported as skipped
- missing `intent.yaml` is treated as a bootstrap opportunity, not a workflow failure
- SCP drafting is local to this repo and does not approve memory automatically
- outputs are meant to be both human-readable and machine-readable
