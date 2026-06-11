"""Approved SCP Canon constants."""

from __future__ import annotations

from dataclasses import dataclass


APPROVED_EVENT_TYPES: tuple[str, ...] = (
    "strategy_change",
    "requirement_change",
    "constraint_change",
    "architecture_decision",
    "dependency_decision",
    "security_decision",
    "cost_decision",
    "incident_discovery",
    "user_reversal",
    "major_implementation_decision",
    "major_completion",
)

APPROVED_LIFECYCLE_STATES: tuple[str, ...] = (
    "active",
    "superseded",
    "deprecated",
    "experimental",
    "rejected",
)

APPROVED_CARD_LAYERS: tuple[str, ...] = (
    "origin",
    "event",
    "milestone",
    "closure",
)

APPROVED_FIELDS: tuple[str, ...] = (
    "id",
    "layer",
    "type",
    "status",
    "title",
    "decision",
    "why",
    "evidence",
    "constraints",
    "impact",
    "future_trap",
    "revisit_if",
    "next",
    "supersedes",
    "effective_from",
    "scope",
    "preservation_value",
)

APPROVED_PRESERVATION_VALUES: tuple[str, ...] = (
    "low",
    "medium",
    "high",
)

EVENT_REQUIRED_FIELDS: tuple[str, ...] = (
    "id",
    "layer",
    "type",
    "status",
    "title",
    "decision",
    "why",
    "evidence",
    "constraints",
    "impact",
    "future_trap",
    "revisit_if",
    "next",
    "effective_from",
    "scope",
    "preservation_value",
)

NON_EVENT_REQUIRED_FIELDS: tuple[str, ...] = (
    "id",
    "layer",
    "status",
    "title",
    "decision",
    "why",
    "evidence",
    "constraints",
    "impact",
    "future_trap",
    "revisit_if",
    "next",
    "effective_from",
    "scope",
    "preservation_value",
)


@dataclass(frozen=True)
class Canon:
    event_types: tuple[str, ...]
    lifecycle_states: tuple[str, ...]
    card_layers: tuple[str, ...]
    field_names: tuple[str, ...]
    preservation_values: tuple[str, ...]


def load_canon() -> Canon:
    """Load the approved in-repo Canon constants."""
    return Canon(
        event_types=APPROVED_EVENT_TYPES,
        lifecycle_states=APPROVED_LIFECYCLE_STATES,
        card_layers=APPROVED_CARD_LAYERS,
        field_names=APPROVED_FIELDS,
        preservation_values=APPROVED_PRESERVATION_VALUES,
    )
