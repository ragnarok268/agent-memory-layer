# SCP v0.1 Release Summary

## What SCP Is

SCP is a free, open-source, AI-maintained decision preservation system.

It preserves important project decisions from adoption forward so humans and AI do not have to rediscover them later.

## What SCP Does

SCP provides an embedded Canon, deterministic card validation, deterministic event classification, onboarding through an Origin Card, and example decision records that future humans and AI can read directly from the repository.

## Major v0.1 Capabilities

- Embedded Canon definitions for event types, lifecycle states, card layers, and field meanings.
- Deterministic YAML validation for SCP records.
- Deterministic classification for preservation-worthy changes and approved non-preservation cases.
- SCP card generation for approved event records.
- `scp init` onboarding that creates the starting Origin Card.
- Documentation-only consumption tests for single-decision and multi-decision reuse.
- Local-first, dependency-light implementation with no cloud, telemetry, or LLM requirements.

## Validation Completed

- Full repository test suite.
- SCP-focused test suite.
- SCP example validation through the CLI.
- Diff whitespace and formatting checks.
- Documentation consumption validation for single-decision and multi-decision scenarios.

## Known Limitations

- YAML support is intentionally limited to the subset used by SCP records in this repository.
- Classification is deterministic summary matching, not source-history inference.
- The system preserves reasoning from adoption forward and does not reconstruct old project history.
- Generated cards are valid but can be less informative than hand-authored project-specific records.

## Future Work

- Evaluate whether optional local retrieval improves record discoverability without changing v0.1 local-first constraints.
- Expand practical examples of Origin, event, and milestone card usage.
- Continue testing whether SCP records reduce rediscovery across more project scenarios.
