# SCP Build Report

## Files Changed

- `pyproject.toml`
- `src/scp/__init__.py`
- `src/scp/canon.py`
- `src/scp/yamlio.py`
- `src/scp/schema.py`
- `src/scp/classifier.py`
- `src/scp/generator.py`
- `src/scp/cli.py`
- `tests/conftest.py`
- `tests/helpers.py`
- `tests/test_scp.py`
- `tests/test_scp_cli.py`
- `examples/scp/generated_dependency_decision.yaml`
- `SCP_BUILD_REPORT.md`

## Commands Added

- `scp validate <path>`
- `scp classify "<change summary>"`
- `scp generate --summary "<change summary>" --out <path>`
- `scp version`

## Tests Added

- Valid example card passes validation.
- Unknown event type fails validation.
- Unknown field fails validation.
- Invalid lifecycle state fails validation.
- Missing required field fails validation.
- Formatting change returns `no_preservation`.
- Dependency decision returns `dependency_decision`.
- Cost-driven change returns `cost_decision`.
- User reversal language returns `user_reversal`.
- Generated card serializes as YAML and validates.
- Checked-in generated example remains valid.
- CLI validate command succeeds on the example card.
- CLI classify returns `no_preservation` for formatting-only changes.
- CLI generate writes YAML that validates.

## Validation Results

- `python -m pytest tests\test_scp.py tests\test_scp_cli.py` passed: 14 tests.
- `python -m pytest` passed: 58 tests.
- `$env:PYTHONPATH=(Resolve-Path src); python -m scp.cli validate examples\scp` passed: validated 2 files.
- `git diff --check` passed.

## Examples Validated

- `examples/scp/SCP-0007.yaml`
- `examples/scp/generated_dependency_decision.yaml`

## Confirmation

- No Canon meanings were inferred.
- No unapproved event types or fields were added.
- No LLM, API, cloud, or telemetry behavior was added.
