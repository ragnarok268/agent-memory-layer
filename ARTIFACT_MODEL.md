# Artifact Model

## Why artifacts matter

This methodology treats artifacts as working memory for engineering.

The point is not to create paperwork.

The point is to preserve the minimum useful evidence that helps both humans and AI agents understand what happened and what should happen next.

## The four artifact layers

### 1. Intent artifacts

Purpose:

Define what the change is supposed to do and what constraints it must respect.

Typical examples:

- `intent.yaml`
- task constraints
- repository agent instructions

Main question answered:

What was requested?

### 2. Verification artifacts

Purpose:

Show whether the implementation stayed aligned with the declared intent.

Typical examples:

- `audit_receipt.md`
- `audit_receipt.json`
- test output

Main question answered:

Did the change stay within scope and constraints?

### 3. Capability visibility artifacts

Purpose:

Show what dependencies, imports, and runtime authority surfaces exist or changed.

Typical examples:

- `DS2_REPORT.md`
- `ds2_graph.json`
- `ds2_receipt.json`

Main question answered:

What capability surface already exists, and what did this change rely on or introduce?

### 4. Preserved rationale artifacts

Purpose:

Keep the decisions, discoveries, and constraints that would be expensive to rediscover later.

Typical examples:

- `.scp/origin.yaml`
- `.scp/SCP-xxxx.yaml`
- milestone or closure cards

Main question answered:

Why was this path chosen, rejected, or preserved?

## Shared design properties

Across IA, DS2, and SCP, the useful artifact pattern is:

- local and reviewable
- plain enough for humans to read
- structured enough for AI agents to consume
- durable across sessions
- narrow in scope
- explicit about limits

## Human-readable and machine-readable

The workflow works best when artifacts support both forms:

- human-readable summaries for reviewers
- machine-readable structures for automation and agent reuse

That dual format makes it easier for an AI agent to continue work without forcing a human to read raw JSON only.

## Artifact flow

```text
request or idea
  -> intent artifact
  -> generated code
  -> verification artifact
  -> capability artifact
  -> preserved rationale artifact
  -> review and shipment evidence
```

## Compounding effect

When these artifacts accumulate over time, the repository becomes easier to work in because future humans and AI agents can answer questions from preserved evidence instead of starting from zero.
