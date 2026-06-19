# Evidence Summary

## Status

This repository is experimental.

Its current evidence is based on local Codex-only A/B trials comparing:

- a baseline repo with normal README-only guidance
- a workflow-enabled repo with guardrails, intent handling, and preserved artifacts

The current evidence should be treated as preliminary.

## What has been observed

Across the local Codex trials collected in this repository, the workflow-enabled condition consistently improved:

- artifact usage
- handoff quality
- repair-loop behavior

These observations remained visible after:

- fixing the workflow fixture so the guardrail runner did not falsely fail IA
- improving experiment isolation
- adding per-run timing support

## What the current evidence does not establish

The repository does not currently establish:

- broad productivity gains
- universal quality improvements
- cross-model generalization
- cross-team or enterprise-scale validation
- robust time-to-completion advantages in real interactive use

## Batch notes

### Original contaminated batch

Observed:

- higher workflow artifact usage
- higher workflow handoff quality
- higher workflow self-repair behavior

Threat:

- the workflow fixture falsely penalized itself because the copied guardrail runner used local subprocess calls while the trial intent treated shell execution too strictly

### Fixture-fixed rerun

Observed:

- the workflow improvements in artifact usage, handoff quality, and repair behavior remained
- the time gap became much smaller than in the contaminated batch

This is the strongest current behavioral evidence in the repo.

### Final timed rerun

Observed:

- the same behavioral score differences remained
- timing became more consistent mechanically

Threat:

- the final timed rerun used a deterministic local executor to keep timing automatic and repeatable, so its elapsed times are not directly comparable to an interactive human-plus-agent session

## Known threats to validity

- single primary agent condition so far: Codex
- local machine and local environment only
- small task set
- scoring still involves evaluator judgment
- two timing modes were used across the project history
- the final timed rerun is useful for consistency but weaker for real productivity interpretation

## Current interpretation

Strongest currently supported claim:

- preserving and reusing structured workflow artifacts helped Codex behave more like a context-aware maintainer and leave better future-useful handoff context

Weaker claim:

- the workflow improves elapsed completion time or overall productivity

That claim needs more interactive trials and more than one model.
