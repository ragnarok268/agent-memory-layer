# Benchmark Result Report Template

## Summary

Date:

Agent:

Model/version:

Repository commit:

Number of paired tasks completed:

## Result Table

Paste the generated table from `results/results_table.md`.

## Observations

- Context reuse:
- Prior decision preservation:
- Rediscovery events:
- Architecture regressions:
- Intent/capability drift:
- Dependency discipline:
- Repair behavior:
- Handoff quality:

## Limitations

- This is a small paired benchmark.
- Results apply only to the tested agent, prompts, fixtures, and repository state.
- Human judgment may still affect rediscovery and artifact-use scoring when transcripts do not provide direct evidence.
- Timing and completion quality may vary across runs.

## Conservative Claim Boundary

Allowed:

> In a small paired Codex evaluation, Agent Memory Layer improved context reuse and reduced intent/capability drift versus a no-memory baseline.

Also allowed when directly supported by receipts:

> Repository-local memory improved preservation of prior decisions and reduced context rediscovery in this benchmark.

Not allowed:

> Agent Memory Layer makes Codex better overall.
