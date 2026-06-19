# CI And Hooks

## Purpose

The thin automation layer should run quietly in normal development flow.

That means local hooks should stay lightweight and CI should provide the stronger shared enforcement.

## GitHub Actions

This repository includes a simple workflow:

- runs on `push`
- runs on `pull_request`
- installs Python
- installs `pytest`
- runs tests
- runs the guardrail runner in a safe demo mode

The workflow does not require IA, DS2, or SCP to be installed.

If those tools are missing, the runner records that they were skipped.

## Why hooks should stay lightweight

Heavy hooks become workflow tax.

For v1, local hooks should do small routing work, not expensive analysis.

Good local hook behavior:

- detect changed paths
- run the guardrail runner
- write local summaries

Less good hook behavior:

- blocking every commit for slow scans
- requiring network access
- assuming optional tools are installed everywhere

## Optional local hook example

Example `pre-commit` hook:

```bash
#!/usr/bin/env bash
set -euo pipefail

changed_files="$(git diff --cached --name-only)"
if [ -n "$changed_files" ]; then
  python automation/guardrail_runner.py --changed $changed_files
fi
```

PowerShell example:

```powershell
$changed = git diff --cached --name-only
if ($changed) {
    python automation/guardrail_runner.py --changed $changed
}
```

These examples are intentionally small.

## When CI should be stricter

CI is the better place for stronger shared checks because it is:

- consistent
- reviewable
- easier to standardize across contributors

As the workflow matures, CI can enforce:

- test passing
- artifact generation
- SCP schema validation
- artifact freshness

## Practical recommendation

Start with:

- lightweight local hooks
- stronger CI
- clear summaries

That gives users the benefit of automation without making local development fragile or annoying.
