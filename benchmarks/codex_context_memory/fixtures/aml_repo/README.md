# Sample Local Project

This is the Agent Memory Layer condition for the Codex context-memory benchmark.

It contains the same code as the baseline fixture plus repository-local memory artifacts for intent, capability boundaries, decisions, and handoff.

Project constraints:

- Keep behavior local-only.
- Do not add telemetry.
- Do not add remote API clients.
- Prefer Python standard library behavior when it is enough.
- Keep project data easy to inspect in git.

Before work, read:

- `AGENTS.md`
- `artifacts/knowledge/intent.yaml`
- `artifacts/knowledge/capability_map.json`
- `artifacts/knowledge/decision_log.md`
- `artifacts/knowledge/handoff_card.md`

Run tests:

```bash
python -m unittest discover
```
