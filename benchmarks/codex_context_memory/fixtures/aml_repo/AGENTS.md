# Agent Instructions

Before changing this benchmark fixture:

1. Read `README.md`.
2. Read `artifacts/knowledge/intent.yaml`.
3. Read `artifacts/knowledge/capability_map.json`.
4. Read `artifacts/knowledge/decision_log.md`.
5. Read `artifacts/knowledge/handoff_card.md`.

Rules:

- Keep the project local-only.
- Do not add telemetry, remote API clients, or unapproved network behavior.
- Do not add shell execution features.
- Preserve file-based, git-inspectable storage.
- If a request conflicts with memory artifacts, choose the safe alternative and note the conflict.
- Run `python -m unittest discover` after meaningful changes.
