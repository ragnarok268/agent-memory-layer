# Agent Memory Layer

Agent Memory Layer is an experimental, documentation-first workflow for making AI-assisted software work easier to review, repair, and continue later.

This repository is designed for AI-assisted engineering workflows. It provides repository-local memory, intent, decision, and evidence artifacts that can be read by both humans and AI coding agents such as Codex, Cursor, Claude Code, Gemini, or similar systems.

It is not intended to be a conventional Python library, package, SDK, framework, or end-user application. The included Python scripts are thin repo-local automation helpers for routing checks and writing artifacts.

It is built around three complementary capabilities:

- intent verification, represented by IA
- dependency and capability awareness, represented by DS2
- engineering memory, represented by SCP

This repository is not an industry standard. It is an open-source methodology and research direction that is currently evaluated with local automation and reproducible A/B trials.

## Start here

- For humans: start with [README.md](README.md), [WORKFLOW.md](WORKFLOW.md), and [EVIDENCE.md](EVIDENCE.md).
- For AI agents: start with [AGENT_BOOTSTRAP.md](AGENT_BOOTSTRAP.md), [AGENTS.md](AGENTS.md), and [ARTIFACT_MODEL.md](ARTIFACT_MODEL.md).

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

- AI-assisted developers who rely heavily on coding agents
- solo founders
- self-taught developers
- domain experts building internal tools
- engineering reviewers
- teams experimenting with AI coding agents
- junior and mid-level developers who want clearer intent, review, and context-preservation habits
- experienced engineers who want durable engineering memory and reproducible handoff

It is usually less useful for throwaway scripts, trivial prototypes, teams with little AI usage, or teams that already have strong durable engineering-memory practices.

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

## First 30 minutes

This repo is documentation-first and uses a thin local automation layer.

There is no package install step for the repo itself.

1. Read this README and [WORKFLOW.md](WORKFLOW.md).
2. If you are using Codex, Cursor, Claude Code, Gemini, or a similar agent, read [AGENT_BOOTSTRAP.md](AGENT_BOOTSTRAP.md).
3. Run the test suite:

```bash
python -m pytest
```

4. Make a small documentation or code change.
5. Run the guardrail runner on the changed files:

```bash
python automation/guardrail_runner.py --changed README.md automation/guardrail_runner.py
```

6. Review the generated artifacts under `artifacts/knowledge/`.

Required local validation for this repository is `python -m pytest`.

The intended operating model combines intent verification, dependency/capability awareness, and engineering memory. The implementation is modular, so lightweight use can omit or replace individual tools, but the complete methodology assumes these capabilities work together.

External tool installation is optional for repo-local validation:

- `ia` enables intent verification.
- `ds2` enables dependency and capability-surface scanning.
- SCP is represented here by local draft artifacts; the separate SCP project provides the broader decision-preservation reference implementation.

If `ia` or `ds2` are not installed, the runner reports them as skipped rather than failing. That means the repo-local proof of concept can still be tested without installing the full companion toolchain.

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

The next validation milestone is broader external use: more models, more developers, longer projects, and real-world case studies.

## Where to start

- Overview and first 30 minutes: [README.md](README.md)
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

## License

This project is licensed under the [MIT License](LICENSE).

## Feedback

Feedback is most useful when it is concrete:

- which part was unclear
- which claim feels overstated
- which artifact was useful or noisy
- which experiment step was not reproducible
- which additional validation would change your confidence

If you publish the repository on GitHub, the clearest feedback channel is an issue with a concrete reproduction, criticism, or suggested experiment improvement.

For now, the safest framing is: this repository shows a plausible agent-memory workflow with preliminary local evidence, not a proven standard.
