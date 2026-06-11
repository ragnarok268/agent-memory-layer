"""Deterministic SCP event classification."""

from __future__ import annotations

from dataclasses import dataclass
import re

from scp.canon import APPROVED_EVENT_TYPES


NO_PRESERVATION = "no_preservation"


@dataclass(frozen=True)
class Classification:
    event_type: str
    reason: str


def _normalize(summary: str) -> str:
    return re.sub(r"\s+", " ", summary.strip().lower())


def _contains_any(summary: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in summary for pattern in patterns)


def classify_summary(summary: str) -> Classification:
    normalized = _normalize(summary)
    if not normalized:
        return Classification(NO_PRESERVATION, "Empty summary.")

    no_preservation_rules: tuple[tuple[str, tuple[str, ...]], ...] = (
        ("typo fix", ("typo fix", "fix typo", "spelling correction")),
        ("formatting change", ("formatting change", "formatting only", "whitespace only", "reformat", "format code")),
        ("comment edit", ("comment edit", "comments only", "comment only", "docstring only")),
        ("routine refactor", ("routine refactor", "simple refactor", "internal cleanup refactor")),
        ("trivial code movement", ("trivial code movement", "move code only", "code moved without logic change")),
        ("dependency lockfile noise", ("lockfile only", "dependency lockfile noise", "lockfile update only", "package-lock only", "poetry.lock only")),
    )
    for label, patterns in no_preservation_rules:
        if _contains_any(normalized, patterns):
            return Classification(NO_PRESERVATION, f"Matched approved non-preservation event: {label}.")

    if (
        ("not working" in normalized or "isn't working" in normalized)
        and ("abandon" in normalized or "reject" in normalized or "stop" in normalized)
    ) or _contains_any(normalized, ("reverses previous decision", "abandon this path", "user rejected the approach")):
        return Classification("user_reversal", "Matched user reversal language.")

    if _contains_any(normalized, ("cost", "cheaper", "expensive", "licensing", "token usage", "maintenance burden", "operational expense", "api expense")):
        return Classification("cost_decision", "Matched cost-driven decision language.")

    if _contains_any(
        normalized,
        (
            "continue using",
            "dependency",
            "package",
            "library",
            "pin version",
            "unpinned",
            "pin ",
            "unpin ",
            "add fastapi",
            "remove dependency",
            "replace dependency",
            "keep existing dependency",
        ),
    ):
        return Classification("dependency_decision", "Matched dependency decision language.")

    if _contains_any(normalized, ("strategy", "path forward", "overall direction", "approach changed", "new strategy")):
        return Classification("strategy_change", "Matched strategy change language.")

    if _contains_any(normalized, ("requirement", "must support", "must do", "new requirement", "remove requirement")):
        return Classification("requirement_change", "Matched requirement change language.")

    if _contains_any(normalized, ("local-first", "no telemetry", "constraint", "budget constraint", "deployment constraint", "compliance constraint", "performance constraint")):
        return Classification("constraint_change", "Matched constraint change language.")

    if _contains_any(normalized, ("architecture", "storage model", "runtime model", "major boundary", "framework selection", "design direction")):
        return Classification("architecture_decision", "Matched architecture decision language.")

    if _contains_any(normalized, ("security", "trust boundary", "sensitive operation", "restricted capability", "gated", "prohibited")):
        return Classification("security_decision", "Matched security decision language.")

    if _contains_any(normalized, ("root cause", "likely cause", "failure pattern", "outage", "exploit", "repeated issue", "bug pattern")):
        return Classification("incident_discovery", "Matched incident discovery language.")

    if _contains_any(normalized, ("algorithm", "data flow", "implementation approach", "workaround", "avoided simpler alternative", "non-obvious pattern")):
        return Classification("major_implementation_decision", "Matched implementation decision language.")

    if _contains_any(normalized, ("completed", "completion", "validation pass", "deliverable", "milestone complete", "project phase ended")):
        return Classification("major_completion", "Matched major completion language.")

    return Classification(NO_PRESERVATION, "No approved Canon event type matched.")


def is_approved_event(event_type: str) -> bool:
    return event_type in APPROVED_EVENT_TYPES
