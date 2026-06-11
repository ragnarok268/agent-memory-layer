# SCP Canon

Every SCP-enabled project contains an embedded Canon.

The Canon is a small project-local reasoning vocabulary that travels with the repository.

Humans and AI do not need prior SCP knowledge.

They learn the project's SCP vocabulary by reading the embedded Canon.

The Canon defines:

- preservation-worthy event types
- lifecycle states
- field meanings
- reasoning semantics

The Canon exists to reduce ambiguity across humans, AI systems, sessions, and time.

## Approved Canon Event Types

Use only these event types.

### `strategy_change`

Definition: A change in the overall project direction or approach.

Preserve when:

- A previous strategy is abandoned.
- A new strategy is selected.
- The user or team changes the intended path forward.

Do not preserve when:

- The change is only wording, formatting, or routine cleanup.

### `requirement_change`

Definition: A change to what the project must do or support.

Preserve when:

- A new requirement is added.
- An existing requirement is removed.
- An existing requirement materially changes.

Do not preserve when:

- The change only clarifies wording without changing expected behavior.

### `constraint_change`

Definition: A change to a rule, boundary, limitation, or operating condition that affects future work.

Preserve when:

- A local-first rule is added or removed.
- A no-telemetry rule is added or removed.
- A performance, compliance, security, budget, or deployment constraint changes.

Do not preserve when:

- The constraint is restated but not changed.

### `architecture_decision`

Definition: A decision that affects project structure, major components, boundaries, or long-term design.

Preserve when:

- A framework, architecture, storage model, runtime model, or major boundary is selected.
- An architecture path is rejected.
- A major design direction is replaced.

Do not preserve when:

- The change is a routine internal refactor with no meaningful design impact.

### `dependency_decision`

Definition: A decision to add, reject, remove, replace, pin, unpin, or continue using a dependency.

Preserve when:

- A dependency is added.
- A dependency is rejected.
- A dependency is removed.
- A dependency is replaced.
- A dependency is kept specifically to avoid unnecessary additions.
- A dependency version is pinned or unpinned for a reason.

Do not preserve when:

- A lockfile changes only as a routine install/update side effect with no decision.

### `security_decision`

Definition: A decision that affects permissions, trust boundaries, sensitive data, execution authority, abuse resistance, or risk exposure.

Preserve when:

- A capability is blocked, restricted, removed, or allowed for a security reason.
- A trust boundary changes.
- A sensitive operation is gated or prohibited.

Do not preserve when:

- The change is purely cosmetic or unrelated to risk.

### `cost_decision`

Definition: A decision primarily driven by cost, licensing, token usage, infrastructure expense, API expense, operational expense, or maintenance burden.

Preserve when:

- A model, dependency, service, provider, architecture, or workflow is selected or rejected because of cost.
- A cheaper or lower-maintenance approach is selected.
- A more expensive approach is accepted intentionally.

Do not preserve when:

- Cost is mentioned casually but does not drive the decision.

### `incident_discovery`

Definition: A discovered failure, bug pattern, outage, exploit, repeated error, or operational issue that should not be rediscovered from scratch later.

Preserve when:

- A root cause or likely cause is identified.
- A failure pattern is found.
- A bug, exploit, outage, or repeated issue changes future work.

Do not preserve when:

- The issue is a trivial one-off fix with no reusable lesson.

### `user_reversal`

Definition: A previously accepted or attempted solution is rejected by the user or stakeholder.

Preserve when:

- The user says the current approach is not working.
- The user tells the AI to abandon a path.
- The user reverses a previous decision.
- The user changes preference after seeing an implementation.

Do not preserve when:

- The user makes a minor wording or formatting correction.

### `major_implementation_decision`

Definition: A significant implementation choice that future humans or AI would likely need to understand before modifying the system.

Preserve when:

- A non-obvious algorithm, pattern, data flow, or implementation approach is selected.
- A simpler-looking alternative is intentionally avoided.
- A workaround is introduced for a specific reason.

Do not preserve when:

- The implementation is straightforward and obvious from the code.

### `major_completion`

Definition: Completion of a meaningful project phase, milestone, validation, or deliverable.

Preserve when:

- A major feature is completed.
- A validation pass is completed.
- A project phase ends.
- A deliverable is produced.

Do not preserve when:

- A small routine task is completed.

## Approved Non-Preservation Events

Do not create SCP records for these by default:

- `typo_fix`
- `formatting_change`
- `comment_edit`
- `routine_refactor`
- `routine_bug_fix`
- `trivial_code_movement`
- `dependency_lockfile_noise`

A `routine_bug_fix` may become `incident_discovery` only if it reveals a reusable failure pattern, root cause, security issue, or future trap.

## Approved Lifecycle States

Use only these lifecycle states.

### `active`

Definition: The decision is currently in effect.

### `superseded`

Definition: The decision has been replaced by a newer SCP record.

### `deprecated`

Definition: The decision should no longer guide new work, but remains historically relevant.

### `experimental`

Definition: The decision is temporary or under evaluation.

### `rejected`

Definition: The option was considered and intentionally not chosen.

## Approved Card Layers

Use only these SCP card layers.

### `origin`

Purpose: Captures why the project exists, its goals, constraints, success criteria, and non-goals.

Created when: When SCP is adopted or when a new project begins.

### `event`

Purpose: Captures a preservation-worthy decision or discovery.

Created when: A Canon event type occurs.

### `milestone`

Purpose: Captures current project state at a meaningful checkpoint.

Created when: A major phase, validation, or deliverable is completed.

### `closure`

Purpose: Captures final outcome, lessons, and future work when a project or major effort ends.

Created when: A project or major effort concludes.
