# Agent Guidance

Before work:

1. Read `README.md`.
2. Read `intent.yaml`.
3. Read `artifacts/knowledge/guardrail_summary.md` if present.
4. Read recent files under `artifacts/knowledge/scp_drafts/` if present.

After meaningful changes:

1. Run `python automation/guardrail_runner.py --changed <changed files>`.
2. Read `artifacts/knowledge/guardrail_summary.md`.
3. If IA fails and the issue is clear, repair and rerun.
4. Leave SCP outputs as drafts unless explicitly approved.
5. Run `python -m pytest`.
