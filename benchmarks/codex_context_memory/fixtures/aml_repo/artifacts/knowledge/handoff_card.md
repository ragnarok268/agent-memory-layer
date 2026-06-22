# Handoff Card

Current safe direction:

- Keep the fixture small and local-only.
- Prefer standard library behavior.
- Preserve tests and repair implementation when tests fail.
- Reuse the existing feature flag pattern for new experimental behavior.
- For feature flag tasks, use default-off flags, `FeatureRegistry`, and `registry.json`.
- For exported reports, use deterministic identifiers rather than UUIDv4.
- For the next safe implementation step, inspect current tests and existing helpers before changing code.

Known traps:

- Do not add SQLite for persistence.
- Do not add subprocess or shell command execution.
- Do not add network checks for status reporting.
- Do not auto-edit TODO comments in scanner behavior.
