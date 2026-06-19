# Examples

## Example 1: Local-first notes app

Goal:

Build a small notes app that stores data locally and does not call remote services.

Workflow:

1. Define intent and constraints such as `local_first: true` and `no_telemetry: true`.
2. Ask an AI agent to generate the notes app.
3. Run IA to verify the implementation against that intent.
4. If IA reports remote calls or scope drift, repair the code and rerun IA.
5. Use SCP only if a meaningful decision was made, such as rejecting sync or preserving the local-first constraint.

What this shows:

- IA helps verify that generated code stayed aligned with the request.
- Human review becomes easier because the drift is explicit instead of hidden in the code.

## Example 2: API feature in an existing Python app

Goal:

Add an endpoint to an existing project without adding unnecessary dependencies.

Workflow:

1. Inspect DS2 artifacts before changing dependencies.
2. Notice that `FastAPI` is already present and already provides the needed capability.
3. Reuse the existing framework instead of adding another HTTP package.
4. Preserve the dependency decision in SCP if the reuse choice is important enough to prevent future rediscovery.

What this shows:

- DS2 helps the agent understand what already exists.
- SCP helps future contributors understand why another package was not added.

## Example 3: Internal tool with meaningful constraints

Goal:

Build an internal workflow tool with strict local-only handling and limited execution authority.

Workflow:

1. Capture the constraints in an intent artifact.
2. Generate the first implementation with an AI agent.
3. Run IA to check for drift against the local-only rules.
4. Run or inspect DS2 to understand whether the dependency graph introduces network, shell, browser, or cloud-related authority.
5. Use SCP to preserve any high-value architectural or security decisions.
6. Ship only after the evidence package is understandable to both the builder and a reviewer.

What this shows:

- IA, DS2, and SCP each cover a different failure mode.
- The combined loop supports more reliable AI-assisted building than code generation alone.

## Example 4: What a future agent sees

A future agent joins the repository months later.

Instead of guessing, it can:

- read the intent artifact to understand original constraints
- read IA receipts to see prior verification outcomes
- read DS2 reports to understand capability surfaces
- read SCP records to understand preserved decisions and traps

That shortens onboarding and reduces repeated mistakes.

## Example evidence bundle

A practical shipment bundle might include:

- the task request or intent artifact
- the generated code change
- IA receipt
- DS2 report
- SCP card when a preserved decision applies
- tests or validation output

This makes the change easier for both humans and AI agents to review, continue, or revisit later.
