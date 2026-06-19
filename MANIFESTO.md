# Manifesto

## The problem

AI-generated code can be fast, useful, and productive.

It can also be hard to trust.

The code may look plausible while drifting from the original request, introducing unnecessary dependencies, expanding runtime authority, or hiding the reasons behind important decisions.

Most software repositories preserve code by default.

They do not preserve intent, verification context, dependency meaning, or decision rationale by default.

That gap becomes more expensive when future work is done by new humans, new reviewers, or new AI agents with no memory of the original session.

## The position

AI-assisted engineering needs more than generated code.

It needs supporting artifacts that answer four basic questions:

1. What was intended?
2. What was actually produced?
3. What capability surface does it rely on or introduce?
4. Why was this decision made?

IA, DS2, and SCP can be read as three answers to those questions.

## The philosophy

Knowledge compounds when discoveries, decisions, constraints, and verification results are preserved in structured artifacts instead of being rediscovered by every future human or AI agent.

## The methodology

Use lightweight artifacts to reduce avoidable uncertainty:

- intent artifacts to define scope and constraints
- verification artifacts to detect drift
- dependency and capability artifacts to show what already exists and what changed
- rationale artifacts to preserve decisions worth remembering

The goal is not bureaucracy.

The goal is to make future work cheaper, safer, and easier to review.

## Human and AI roles

Humans remain decision makers, reviewers, and owners of tradeoffs.

AI agents can generate code, run checks, consume artifacts, repair drift, and maintain the reasoning layer.

This is not about replacing human review.

It is about making both human review and AI repair loops less blind.

## What this research direction suggests

An AI-native engineering workflow becomes more reliable when:

- intent is explicit
- verification is routine
- capability expansion is visible
- rationale is preserved
- evidence is easy for both humans and agents to consume

## What this is not

This is not an industry standard.

It is an open-source methodology and research direction.

It should be tested, criticized, simplified, and improved through real use.
