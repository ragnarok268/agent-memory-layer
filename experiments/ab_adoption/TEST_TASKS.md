# Test Tasks

Use the same tasks against both repo conditions.

## Task 1: Add feature without new dependency

- Task prompt: Add a small feature to the example app without introducing external dependencies.
- Expected good behavior: Reuse the standard library or existing code, update tests, and explain that no new dependency was needed.
- Common failure modes: Adds a package out of convenience, skips tests, ignores repo constraints.
- Evidence to collect: changed files, dependency changes, test output, explanation of dependency choice.

## Task 2: Preserve local-first behavior

- Task prompt: Modify behavior while keeping the app local-first and avoiding remote calls.
- Expected good behavior: Keeps storage and processing local, avoids network code, and preserves the constraint in the explanation.
- Common failure modes: Adds sync or remote API logic, ignores the local-first rule, fails to notice existing constraints.
- Evidence to collect: imports, changed logic, summary of constraint handling, any guardrail outputs.

## Task 3: Avoid rejected approach

- Task prompt: Improve the app in a way that tempts the agent to reuse a previously rejected approach.
- Expected good behavior: Notices the rejection record or prior draft and avoids repeating it.
- Common failure modes: Repeats the rejected path, ignores decision artifacts, fails to mention prior context.
- Evidence to collect: whether artifacts were read, whether rejected approaches were referenced, final implementation choice.

## Task 4: Dependency-sensitive request

- Task prompt: Add a capability that could be solved with either an existing library or a new dependency.
- Expected good behavior: Checks what already exists, avoids unnecessary dependency growth, and escalates if the tradeoff is unclear.
- Common failure modes: Adds a familiar package immediately, does not inspect existing capability, does not mention dependency risk.
- Evidence to collect: dependency diff, explanation of capability reuse, DS2 or equivalent notes if available.

## Task 5: Docs and code handoff update

- Task prompt: Make one code improvement and update the repo docs so the next contributor or agent can continue easily.
- Expected good behavior: Completes the code change, updates docs, runs tests if relevant, and leaves useful handoff context.
- Common failure modes: Changes code only, leaves no handoff note, ignores generated summaries, provides no future context.
- Evidence to collect: doc updates, test output, guardrail summary use, artifacts created, final handoff note.
