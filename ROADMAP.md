# Roadmap

## v1: Thin automation layer

Goal:

Make good workflow behavior happen automatically with minimal setup.

Scope:

- deterministic event classification
- optional IA execution for code changes
- automatic intent bootstrap when IA is requested but intent is missing
- optional DS2 execution for dependency and import surface changes
- SCP-style draft generation for decision-worthy changes
- local JSON and Markdown summaries
- basic CI validation
- concise agent bootstrap guidance

Why it matters:

This proves automation-first adoption without building a large framework.

## v2: Better event detection and review UX

Goal:

Reduce noise and improve usefulness for both humans and agents.

Scope:

- better change classification
- stronger architecture and constraint detection
- clearer review summaries
- richer evidence snippets
- optional local hook helpers
- better artifact loading for future sessions

Why it matters:

This is where the workflow starts to feel helpful instead of merely possible.

## v3: Agent-native memory infrastructure

Goal:

Turn the artifacts into durable background memory for AI-assisted repos.

Scope:

- stronger cross-session artifact loading
- more reliable SCP drafting and review routing
- policy-aware approval checkpoints
- artifact freshness validation across CI and local runs
- reusable patterns across multiple repositories

Why it matters:

At this stage the system starts to resemble quiet engineering infrastructure instead of a set of utilities.
