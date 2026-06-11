"""SCP first-run onboarding."""

from __future__ import annotations

from pathlib import Path

from scp.schema import validate_card
from scp.yamlio import write_yaml_file


DEFAULT_ORIGIN_PATH = Path(".scp/origin.yaml")


def _normalize_answer(value: str) -> str:
    normalized = " ".join(value.strip().split())
    if normalized:
        return normalized
    return "Unspecified at adoption."


def build_origin_card(
    *,
    project_goal: str,
    intended_users: str,
    important_constraints: str,
    non_goals: str,
    success_criteria: str,
    next_known_step: str,
) -> dict[str, object]:
    card = {
        "id": "SCP-ORIGIN",
        "layer": "origin",
        "status": "active",
        "title": "Project origin",
        "decision": _normalize_answer(project_goal),
        "why": "Created by scp init to preserve adoption-forward project context.",
        "evidence": [
            f"Intended users: {_normalize_answer(intended_users)}",
            f"Success criteria: {_normalize_answer(success_criteria)}",
            f"Non-goals: {_normalize_answer(non_goals)}",
        ],
        "constraints": [
            _normalize_answer(important_constraints),
        ],
        "impact": "SCP has a starting project context card for future decision preservation from adoption forward.",
        "future_trap": "Future contributors or AI sessions may assume SCP can infer project origin context from scattered history if this card is missing.",
        "revisit_if": [
            "Project goals materially change.",
            "Success criteria materially change.",
        ],
        "next": _normalize_answer(next_known_step),
        "effective_from": "adoption",
        "scope": "project",
        "preservation_value": "high",
    }
    validate_card(card)
    return card


def prompt_and_write_origin(path: Path = DEFAULT_ORIGIN_PATH) -> Path:
    prompts = (
        ("project goal", "Project goal"),
        ("intended users", "Intended users"),
        ("important constraints", "Important constraints"),
        ("non-goals / things to avoid", "Non-goals / things to avoid"),
        ("success criteria", "Success criteria"),
        ("next known step", "Next known step"),
    )
    answers: dict[str, str] = {}
    for key, label in prompts:
        answers[key] = input(f"{label}: ")

    card = build_origin_card(
        project_goal=answers["project goal"],
        intended_users=answers["intended users"],
        important_constraints=answers["important constraints"],
        non_goals=answers["non-goals / things to avoid"],
        success_criteria=answers["success criteria"],
        next_known_step=answers["next known step"],
    )
    write_yaml_file(path, card)
    return path
