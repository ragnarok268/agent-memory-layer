"""SCP event card generation."""

from __future__ import annotations

import hashlib

from scp.classifier import NO_PRESERVATION, classify_summary


TITLE_BY_EVENT_TYPE: dict[str, str] = {
    "strategy_change": "Strategy change",
    "requirement_change": "Requirement change",
    "constraint_change": "Constraint change",
    "architecture_decision": "Architecture decision",
    "dependency_decision": "Dependency decision",
    "security_decision": "Security decision",
    "cost_decision": "Cost decision",
    "incident_discovery": "Incident discovery",
    "user_reversal": "User reversal",
    "major_implementation_decision": "Major implementation decision",
    "major_completion": "Major completion",
}


def _stable_id(summary: str) -> str:
    digest = hashlib.sha256(summary.strip().encode("utf-8")).hexdigest().upper()
    return f"SCP-{digest[:8]}"


def generate_event_card(summary: str) -> dict[str, object] | None:
    classification = classify_summary(summary)
    if classification.event_type == NO_PRESERVATION:
        return None

    normalized_summary = " ".join(summary.strip().split())
    event_type = classification.event_type

    return {
        "id": _stable_id(normalized_summary),
        "layer": "event",
        "type": event_type,
        "status": "active",
        "title": TITLE_BY_EVENT_TYPE[event_type],
        "decision": normalized_summary,
        "why": classification.reason,
        "evidence": [f"Change summary: {normalized_summary}"],
        "constraints": [],
        "impact": f"Future work should treat this summary as a preserved {event_type}.",
        "future_trap": "Future contributors may repeat this work without realizing the decision was already preserved.",
        "revisit_if": ["A newer SCP record supersedes this decision."],
        "next": "Review the generated SCP card before relying on it for future work.",
        "effective_from": "adoption",
        "scope": "project",
        "preservation_value": "medium",
    }
