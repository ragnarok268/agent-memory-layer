# Agent Memory Layer

Agent Memory Layer is an experimental, documentation-first workflow for making AI-assisted software work easier to review, repair, and continue later.

It combines three open-source ideas:

- IA for intent verification
- DS2 for dependency and capability visibility
- SCP for preserved decisions and rationale

This repository is not a framework or an industry standard. It is an open-source methodology and research direction that is currently evaluated with local automation and reproducible A/B trials.

## What problem it solves

AI can generate code quickly, but repositories often lose the surrounding engineering memory:

- what was intended
- what constraints mattered
- what capability surface changed
- why a decision was made
- what evidence supports shipping the change

When that memory is missing, every future human or AI agent has to rediscover it.

## Who should use it

This project is most relevant to:

- AI-assisted builders
- solo founders
- self-taught developers
- domain experts building internal tools
- engineering reviewers
- teams experimenting with AI coding agents

## How it works

High-level loop:

Idea
-> AI generates code
-> IA verifies intent
-> DS2 maps dependency and capability surfaces
-> SCP preserves rationale when it matters
-> AI repairs or a human reviews
-> ship with evidence

The goal is to make preserved engineering context feel more like quiet infrastructure than manual ceremony.

## Quick start

This repo is documentation-first and uses a thin local automation layer.

There is no package install step for the repo itself.

1. Read [WORKFLOW.md](WORKFLOW.md).
2. Read [AGENT_BOOTSTRAP.md](AGENT_BOOTSTRAP.md).
3. Run the test suite:

```bash
python -m pytest
```

4. Try the guardrail runner:

```bash
python automation/guardrail_runner.py --changed README.md automation/guardrail_runner.py
```

If `ia` or `ds2` are not installed, the runner reports them as skipped rather than failing.

## What evidence currently exists

Current evidence in this repo is preliminary and local.

Observed in the Codex A/B trials so far:

- better artifact usage in the workflow-enabled condition
- better handoff quality
- better repair-loop behavior

The strongest current summary is [EVIDENCE.md](EVIDENCE.md). The reproducible experiment harness lives in [experiments/ab_adoption](experiments/ab_adoption/README.md).

## What limitations remain

Not yet established:

- broad productivity gains
- universal quality improvements
- cross-model generalization
- enterprise-scale validation

Known threats to validity include small task sets, local-only runs, and mixed timing methodologies across the project history.

## Where to start

- Quick start and overview: [README.md](README.md)
- Core workflow: [WORKFLOW.md](WORKFLOW.md)
- Automation design: [AUTOMATION_ARCHITECTURE.md](AUTOMATION_ARCHITECTURE.md)
- Agent operating instructions: [AGENTS.md](AGENTS.md)
- Artifact model: [ARTIFACT_MODEL.md](ARTIFACT_MODEL.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Experiment methodology: [experiments/ab_adoption/README.md](experiments/ab_adoption/README.md)
- Contribution guidance: [CONTRIBUTING.md](CONTRIBUTING.md)

## Source repositories

- IA: [github.com/ragnarok268/ia](https://github.com/ragnarok268/ia)
- DS2: [github.com/ragnarok268/DS2](https://github.com/ragnarok268/DS2)
- SCP: [github.com/ragnarok268/scp](https://github.com/ragnarok268/scp)

## Feedback

Feedback is most useful when it is concrete:

- which part was unclear
- which claim feels overstated
- which artifact was useful or noisy
- which experiment step was not reproducible
- which additional validation would change your confidence

If you publish the repository on GitHub, the clearest feedback channel is an issue with a concrete reproduction, criticism, or suggested experiment improvement.

For now, the safest framing is: this repository shows a plausible agent-memory workflow with preliminary local evidence, not a proven standard.
