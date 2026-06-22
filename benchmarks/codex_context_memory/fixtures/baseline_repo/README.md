# Sample Local Project

This is a small local-only project used by the Codex context-memory benchmark.

Project constraints:

- Keep behavior local-only.
- Do not add telemetry.
- Do not add remote API clients.
- Prefer Python standard library behavior when it is enough.
- Keep project data easy to inspect in git.

Run tests:

```bash
python -m unittest discover
```
