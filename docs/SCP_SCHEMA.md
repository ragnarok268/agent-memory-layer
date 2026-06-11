# SCP Schema

This document defines the approved SCP record fields for documentation and examples in this repository.

Use only these core fields unless existing repository code already has a stricter schema.

## Approved Core Fields

### `id`

Meaning: Stable identifier for the SCP record.

### `layer`

Meaning: One of `origin`, `event`, `milestone`, `closure`.

### `type`

Meaning: Canon event type for event cards.

### `status`

Meaning: Lifecycle state of the decision.

### `title`

Meaning: Short human-readable label.

### `decision`

Meaning: The decision, outcome, or preserved conclusion.

### `why`

Meaning: The reason the decision was made.

### `evidence`

Meaning: Artifacts, reports, tests, commits, user instructions, or observations supporting the decision.

### `constraints`

Meaning: Boundaries or conditions that shaped the decision.

### `impact`

Meaning: What changed or what future effect the decision has.

### `future_trap`

Meaning: Likely future rediscovery, repeated mistake, or tempting wrong path this record is meant to prevent.

### `revisit_if`

Meaning: Conditions that should trigger reconsideration of the decision.

### `next`

Meaning: Recommended next action or follow-up.

### `supersedes`

Meaning: Previous SCP record replaced by this record.

### `effective_from`

Meaning: Point at which the decision became active.

### `scope`

Meaning: Area of the project affected by the decision.

### `preservation_value`

Meaning: Estimated rediscovery cost if this reasoning is lost.

Allowed values:

- `low`
- `medium`
- `high`

## Required Example Card

```yaml
id: SCP-0007
layer: event
type: dependency_decision
status: active
title: Continue using FastAPI
decision: Continue using FastAPI instead of adding another HTTP framework.
why: Existing FastAPI usage already satisfies the endpoint requirements.
evidence:
  - Dependency analysis showed FastAPI is already present.
constraints:
  - Minimize dependency growth.
impact: Avoided unnecessary dependency addition and reduced maintenance burden.
future_trap: Future contributors may attempt to add another package without realizing equivalent capability already exists.
revisit_if:
  - FastAPI becomes unsupported.
  - Requirements materially change.
next: Implement the feature using the existing framework.
effective_from: adoption
scope: api
preservation_value: medium
```

See [../examples/scp/SCP-0007.yaml](../examples/scp/SCP-0007.yaml).
