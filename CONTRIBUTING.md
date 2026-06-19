# Contributing

## Scope

This repository is a documentation-first experimental workflow project.

Good contributions include:

- clearer explanations
- smaller and more reproducible automation
- better experiment hygiene
- stronger threats-to-validity notes
- cross-agent or cross-model evaluation improvements

## Before opening a change

1. Read [README.md](README.md).
2. Read [WORKFLOW.md](WORKFLOW.md).
3. Read [AGENT_BOOTSTRAP.md](AGENT_BOOTSTRAP.md).
4. If you are working on the experiment harness, read [experiments/ab_adoption/README.md](experiments/ab_adoption/README.md).

## Local validation

Run:

```bash
python -m pytest
```

If you change the experiment harness, also run:

```bash
python experiments/ab_adoption/analyze_results.py
```

## Feedback

The most helpful feedback is specific and falsifiable:

- what part was unclear
- what evidence feels weak
- what assumption seems wrong
- what workflow step created friction
- what experiment design change would improve trust

If you publish issues or review notes, prefer concrete observations over broad claims.
