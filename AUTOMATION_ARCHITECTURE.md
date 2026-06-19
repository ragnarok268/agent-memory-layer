# Automation Architecture

## Purpose

This repository does not try to turn IA, DS2, and SCP into a new framework.

It shows how a thin automation layer can make the workflow happen by default:

- capture intent
- verify generated work
- inspect capability changes when relevant
- draft decision memory when relevant
- leave humans mostly responsible for review and approval

## Core design idea

The automation should feel like quiet infrastructure, not a new ritual.

The user asks an AI assistant to build or modify software.

The workflow then reacts to change events and writes artifacts automatically.

That means the process remembers for the user instead of requiring the user to remember extra steps.

## Thin architecture

```text
user request
  -> agent edits code or docs
  -> guardrail runner inspects changed paths and optional diff
  -> event classifier labels the change
  -> IA runs when code changed
  -> DS2 runs when dependency or import surface changed
  -> SCP draft is generated when the change appears decision-worthy
  -> summaries are written to artifacts/knowledge/
  -> future agents read those artifacts before the next task
```

## Components

### Event classifier

A deterministic classifier that looks at changed paths and optional diff text.

It decides whether the change is:

- `code_change`
- `dependency_change`
- `import_surface_change`
- `decision_worthy_change`
- `docs_only_change`

### Guardrail runner

A small orchestration script that:

- accepts changed paths from the command line
- loads optional diff text
- classifies the event
- decides which checks should run
- attempts to call external tools if they are installed
- writes JSON and Markdown summaries locally

### SCP draft generator

A local draft writer that creates a reviewable SCP-style Markdown note when the event looks important enough to preserve.

It does not auto-approve project memory.

It only drafts it.

## What is automatic

Automatic today in this proof of concept:

- event classification
- routing to IA and DS2 when relevant
- writing local summaries
- drafting SCP-style memory
- producing human-readable and machine-readable outputs

## What still needs human judgment

Humans should still decide:

- whether intent is correct when the user request is ambiguous
- whether a DS2 finding is acceptable
- whether a drafted SCP note is worth keeping
- whether a higher-risk change is ready to ship

## Why this avoids workflow tax

The user should not need to remember:

- when to run IA
- when to run DS2
- when to draft reasoning
- where to write summaries

The automation handles that routing from simple repo events.

The human only needs to step in when the result matters.

## Local-first posture

This thin layer is designed to stay local-first where practical:

- standard library Python
- local file outputs
- no secrets
- no telemetry
- optional external tool usage only when already installed

## Why this matters

If this pattern works, IA, DS2, and SCP start to behave less like standalone tools and more like quiet workflow infrastructure that supports both humans and AI agents in the background.
