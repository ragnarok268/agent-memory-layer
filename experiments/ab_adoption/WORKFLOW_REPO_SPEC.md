# Workflow Repo Spec

## Purpose

Define a comparison repo with the same core app as the baseline condition but with AI-native workflow support added.

## Condition name

`workflow`

## Repo contents

- `README.md`
- one source file
- one test file
- concise `AGENTS.md`
- `intent.yaml` or `artifacts/knowledge/intent_draft.yaml`
- existing `artifacts/knowledge/guardrail_summary.md`
- one sample SCP-style draft or decision note
- instructions to run `python automation/guardrail_runner.py --changed <files>`

Example shape:

```text
workflow-app/
  README.md
  AGENTS.md
  app.py
  test_app.py
  automation/guardrail_runner.py
  artifacts/knowledge/guardrail_summary.md
  artifacts/knowledge/intent_draft.yaml
  artifacts/knowledge/scp_drafts/SCP-DRAFT-0001.md
```

## Guidance style

Short operational agent guidance plus artifact-aware workflow context.

## Required workflow signals

- explicit instruction to read repo artifacts before work
- explicit instruction to run the guardrail runner after meaningful changes
- explicit handling for missing `intent.yaml`
- explicit instruction to leave SCP outputs as drafts unless approved

## Intent note

The workflow fixture should separate application constraints from approved local workflow orchestration.

The application should avoid shell execution unless truly required.

The guardrail automation may invoke local verification commands.

That is approved orchestration and should not be treated as application-level shell execution drift.

If the verification tool cannot distinguish those layers cleanly, the fixture should document the limitation and avoid creating a false failure loop.

## Suggested app

Use the same app as the baseline condition so the main difference is workflow support, not domain complexity.

## Why this condition exists

This condition checks whether artifact-aware workflow scaffolding helps an agent preserve intent, use context better, and leave stronger handoff evidence.
