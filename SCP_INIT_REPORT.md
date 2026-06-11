# SCP Init Report

## Files Changed

- `README.md`
- `src/scp/onboarding.py`
- `src/scp/cli.py`
- `tests/test_scp.py`
- `tests/test_scp_cli.py`
- `SCP_INIT_REPORT.md`

## Init Command Behavior

`scp init` prompts for:

- project goal
- intended users
- important constraints
- non-goals / things to avoid
- success criteria
- next known step

It writes a deterministic Origin Card to `.scp/origin.yaml` by default, or to a user-provided path with `--out`.

Empty answers are handled deterministically as `Unspecified at adoption.`

## Generated Origin Card Path

Default path: `.scp/origin.yaml`

## Tests Added

- init creates valid origin card
- init handles empty answers deterministically
- generated origin card validates
- existing examples still validate
- origin card uses only approved fields and no event type

## Validation Results

- `python -m pytest` passed: 62 tests.
- `python -m pytest tests\test_scp.py tests\test_scp_cli.py` passed: 18 tests.
- `$env:PYTHONPATH=(Resolve-Path src); python -m scp.cli validate examples\scp` passed: validated 5 files.
- `git diff --check` passed.

## Confirmation

- Canon definitions unchanged.
- No source behavior changed outside SCP init.

## Limitations

- The Origin Card uses only already-approved fields, so user-provided intended users, non-goals, and success criteria are preserved within existing field meanings rather than dedicated origin-only fields.
- `scp init` is interactive and line-oriented.
