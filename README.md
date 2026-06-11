# SCP

SCP is a free, open-source, AI-maintained decision preservation system.

It helps humans and AI preserve important project decisions as work happens.

The goal is not to preserve everything.

The goal is to preserve decisions that would be expensive to rediscover later.

The human remains the reviewer and decision maker.

The AI acts as the maintainer of the reasoning layer.

## Why do I need this?

Code survives by default.

Reasoning usually does not.

SCP preserves important project decisions from the point it is adopted forward, helping humans and AI avoid wasting time and resources rediscovering them later.

SCP does not reconstruct the past. It starts preserving reasoning from the moment you adopt it.

## What does it do?

SCP creates and maintains lightweight decision records for preservation-worthy project events.

It uses a small embedded Canon so humans and AI can understand what each record means without guessing.

## How does it help?

- Helps future humans understand why decisions were made.
- Helps future AI sessions avoid repeating rejected or expensive decisions.
- Reduces repeated explanation across sessions.
- Preserves constraints, evidence, and decision rationale.
- Makes project reasoning easier to carry forward over time.

## What it does not do

- It does not reconstruct old project history automatically.
- It does not preserve every change.
- It does not replace tests.
- It does not replace documentation.
- It does not guarantee AI-generated reasoning is correct.
- It does not let AI invent missing history.

## How SCP decides what to preserve

SCP uses predefined preservation-worthy event types.

The AI should not guess what counts as preservation-worthy.

It must classify events using the embedded Canon definitions.

If no Canon event applies, no SCP record should be created by default.

## The Canon

The Canon is a small project-local vocabulary that travels with the repository.

It defines SCP event types, lifecycle states, card layers, and field meanings.

The Canon exists so humans and AI can read SCP records with less ambiguity.

See [docs/SCP_CANON.md](docs/SCP_CANON.md), [docs/SCP_SCHEMA.md](docs/SCP_SCHEMA.md), and [examples/scp/SCP-0007.yaml](examples/scp/SCP-0007.yaml).

## Start here

SCP works from adoption forward.

`scp init` creates the starting Origin Card at `.scp/origin.yaml`.

Future SCP records preserve decisions after adoption.

SCP does not reconstruct old history.

AI should read the Canon and Origin Card before generating or consuming SCP records.

## How AI should use SCP

- Read the Canon.
- Read the Origin Card.
- Classify changes using Canon event definitions.
- Create a card only when a Canon event applies.
- Do not invent missing history.
- Do not create records for trivial changes.

## What SCP Is

SCP is a free, open-source, AI-maintained decision preservation system.

It helps humans and AI preserve important project decisions as work happens.

The goal is not to preserve everything.

The goal is to preserve decisions that would be expensive to rediscover later.

The human remains the reviewer and decision maker.

The AI acts as the maintainer of the reasoning layer.

## What SCP Is Not

SCP is not:

- a retroactive project-history reconstruction tool
- a replacement for tests
- a replacement for documentation
- a replacement for ADRs
- a guarantee that AI reasoning is correct
- a system that preserves every change
- a system that lets AI invent project history

## Documentation Map

- Canon definitions: [docs/SCP_CANON.md](docs/SCP_CANON.md)
- Record schema guidance: [docs/SCP_SCHEMA.md](docs/SCP_SCHEMA.md)
- Required example card: [examples/scp/SCP-0007.yaml](examples/scp/SCP-0007.yaml)
- Verification summary: [README_POSITIONING_UPDATE_REPORT.md](README_POSITIONING_UPDATE_REPORT.md)
