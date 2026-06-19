# Workflow

## Overview

This workflow connects idea, generation, verification, dependency awareness, preserved rationale, and review evidence into one practical loop.

It is meant to be small enough for solo builders and structured enough for repeatable AI-assisted work.

## Core loop

Idea
→ AI generates code
→ IA verifies intent
→ DS2 maps dependency/capability surfaces
→ SCP preserves rationale
→ AI repairs or human reviews
→ ship with evidence

## Step 1: Start with an idea

An idea can be a feature request, bug fix, internal tool need, process improvement, or product experiment.

Before generation, capture the constraints that matter:

- local-first or networked
- read-only or write-capable
- security or compliance boundaries
- dependency preferences
- business or product requirements

This does not need to be heavy.

It needs to be clear enough that later verification means something.

## Step 2: AI generates code

A coding agent or assistant creates or edits code.

At this stage, speed is useful, but speed alone is not the goal.

The important question is whether the generated change matches the request and whether it quietly introduced new authority, dependencies, or assumptions.

## Step 3: IA verifies intent

IA compares the implementation to declared intent and constraints.

This helps answer:

- Did the AI stay within scope?
- Did it violate local-first or no-telemetry rules?
- Did it change unrelated areas?
- Is there implementation drift?

IA does not replace tests or human review.

It provides verification evidence about scope and constraint fidelity.

## Step 4: DS2 maps dependency and capability surfaces

DS2 maps declared dependencies, observed imports, and runtime exposure classes.

This helps answer:

- What capability already exists in the project?
- Did the AI add a package that was not necessary?
- What runtime authority comes with this dependency set?
- What deserves closer review before execution or shipping?

DS2 is especially useful when the agent wants to add a familiar package without first checking what the project already contains.

## Step 5: SCP preserves rationale

SCP captures the reasoning that would otherwise disappear:

- decisions
- constraints
- discoveries
- reversals
- important completions

SCP is not for every change.

It is for the decisions and lessons that would be expensive to rediscover later.

## Step 6: Repair or review

Once artifacts exist, either:

- the AI repairs the change and reruns checks, or
- a human reviewer evaluates the evidence and decides what to do next

This creates a tighter loop than "generate code and hope."

## Step 7: Ship with evidence

A change is stronger when it ships with reviewable artifacts, such as:

- intent definition
- IA receipt
- DS2 report
- SCP record when preservation is warranted
- tests or validation output

That package of evidence makes handoff, audit, review, and future modification easier.

## What makes this workflow useful

- It works with humans and AI agents.
- It reduces repeated explanation.
- It helps future sessions start from artifacts instead of guesswork.
- It supports repair loops instead of one-shot code generation.
- It encourages smaller, more reviewable changes.

## Common failure modes this workflow tries to reduce

- AI drifting from the original request
- unnecessary dependency additions
- hidden capability expansion
- repeated rejection of the same bad path
- lost rationale after a session ends
- fragile review based only on memory and intuition
