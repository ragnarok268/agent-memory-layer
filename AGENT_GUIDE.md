# Agent Guide

## Purpose

This guide explains how an AI coding agent can follow the IA + DS2 + SCP workflow with minimal supervision.

It is written for agents, but humans can use the same loop as a review checklist.

## Operating principle

Do not treat code generation as the end of the task.

Treat code generation as one step inside a larger evidence loop.

## Recommended agent loop

1. Read the task request and repository instructions.
2. Identify the declared intent, constraints, and non-goals.
3. Generate or modify code.
4. Run IA if intent verification is available.
5. Inspect DS2 artifacts or generate fresh DS2 output before dependency changes.
6. Check whether an SCP-worthy decision or discovery occurred.
7. Repair drift, justify dependency changes, or hand off to human review.
8. Summarize the work with evidence.

## What agents should learn from each tool

### From IA

Learn whether the implementation drifted from scope or violated explicit constraints.

If IA fails:

- stop
- inspect the receipt
- repair the drift
- rerun verification

### From DS2

Learn what capabilities already exist before adding new dependencies.

Use DS2 to avoid changes driven by agent familiarity instead of project reality.

If a dependency change is still needed, explain why existing capabilities were not enough.

### From SCP

Learn what the project already decided and preserve only what is worth preserving.

Use SCP when a meaningful decision, reversal, discovery, or constraint change happened.

Do not create preserved rationale records for trivial edits.

## What an agent can do with low human intervention

An agent can usually:

- read existing artifacts
- generate code
- run IA
- inspect DS2
- detect whether a decision seems preservation-worthy
- draft SCP records
- repair straightforward drift
- prepare evidence for review

## Where humans are still important

Humans are still needed for:

- deciding tradeoffs
- accepting risk
- resolving ambiguous requirements
- approving strategy shifts
- reviewing high-impact dependency or architecture changes

## Good agent behavior in this workflow

- read before changing
- prefer existing capability over new additions
- show evidence, not just conclusions
- preserve rationale when rediscovery cost is high
- avoid overclaiming what any one tool proves

## Minimal adoption rule

If the repository only adopts one part of this methodology, the agent should still preserve the same mindset:

- if IA exists, verify intent
- if DS2 exists, inspect capability surface
- if SCP exists, preserve high-value reasoning

The workflow becomes stronger when all three are present, but each tool still improves the review loop on its own.
