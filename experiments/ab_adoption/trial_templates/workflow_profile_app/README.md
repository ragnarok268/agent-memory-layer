# Profile App

Small local-only profile helper.

Constraints:

- keep the app local-first
- avoid unnecessary dependencies
- keep behavior easy to test
- no external network calls
- no remote logging
- human-readable and machine-readable artifacts are preferred

The app should stay simple and file-based when persistence is needed.

Workflow note:

- local guardrail automation may invoke local verification commands
- that orchestration is approved for the workflow itself
- application features should still avoid shell execution unless explicitly required
