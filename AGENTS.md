# Agent Guidance

Before work:

1. Read `README.md`.
2. Read `AGENT_BOOTSTRAP.md`.
3. If present, read `intent.yaml`.
4. If present, read `artifacts/knowledge/guardrail_summary.md`.
5. If present, read recent files under `artifacts/knowledge/scp_drafts/`.

During work:

1. Make small deterministic changes.
2. Keep artifacts human-readable and machine-readable.
3. Do not present this methodology as a formal standard.

After meaningful changes:

1. Run `python automation/guardrail_runner.py --changed <changed files>`.
2. Read `artifacts/knowledge/guardrail_summary.md`.
3. If IA is blocked because `intent.yaml` is missing, review `artifacts/knowledge/intent_draft.yaml`.
4. If IA fails and the fix is clear, repair and rerun the guardrails.
5. If DS2 shows new capability surface, summarize it for human review.
6. If an SCP draft is generated, leave it as a draft unless explicitly approved.
7. If relevant, run `python -m pytest`.

Reference:

- `WORKFLOW.md`
- `AUTOMATION_ARCHITECTURE.md`
- `EVENT_MODEL.md`
- `AGENT_BOOTSTRAP.md`
