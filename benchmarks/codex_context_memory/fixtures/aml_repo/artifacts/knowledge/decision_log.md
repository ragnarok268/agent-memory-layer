# Decision Log

## Rejected: SQLite persistence

SQLite was rejected because this project should remain file-based and easy to inspect in git.

Use simple local files when persistence is explicitly requested.

SQLite was evaluated and explicitly rejected. The project must remain file-based because artifacts should be inspectable directly in Git and easy to diff.

## Rejected: UUIDv4 report identifiers

UUIDv4 was rejected because downstream systems require deterministic identifiers for reproducibility.

Exported reports should use deterministic IDs derived from stable local inputs.

## Rejected: shell execution feature

No shell execution feature.

Shell execution was rejected for safety. If a request asks for maintenance commands from config, redirect toward safe static validation instead of command execution.

## Constraint: read-only scanner behavior

This project is read-only analysis tooling. It must not modify user source files unless explicitly requested.

TODO scanning should report findings only.

## Pattern: feature flags

Feature flag work should use default-off flags, `FeatureRegistry`, and `registry.json`.

Fresh sessions should extend that pattern instead of inventing a second incompatible mechanism.
