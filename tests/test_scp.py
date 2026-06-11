from pathlib import Path

import pytest

from scp.canon import APPROVED_EVENT_TYPES, APPROVED_FIELDS
from scp.classifier import NO_PRESERVATION, classify_summary
from scp.generator import generate_event_card
from scp.onboarding import build_origin_card
from scp.schema import SchemaError, validate_card
from scp.yamlio import dump_yaml_text, load_yaml_file, parse_yaml_text


def test_valid_example_card_passes() -> None:
    card = load_yaml_file(Path("examples/scp/SCP-0007.yaml"))
    validate_card(card)


def test_unknown_event_fails() -> None:
    card = load_yaml_file(Path("examples/scp/SCP-0007.yaml"))
    card["type"] = "invented_event"

    with pytest.raises(SchemaError, match="Unknown event type"):
        validate_card(card)


def test_unknown_field_fails() -> None:
    card = load_yaml_file(Path("examples/scp/SCP-0007.yaml"))
    card["extra_field"] = "nope"

    with pytest.raises(SchemaError, match="Unknown field"):
        validate_card(card)


def test_invalid_status_fails() -> None:
    card = load_yaml_file(Path("examples/scp/SCP-0007.yaml"))
    card["status"] = "pending"

    with pytest.raises(SchemaError, match="Unknown lifecycle state"):
        validate_card(card)


def test_missing_required_field_fails() -> None:
    card = load_yaml_file(Path("examples/scp/SCP-0007.yaml"))
    del card["decision"]

    with pytest.raises(SchemaError, match="Missing required field"):
        validate_card(card)


def test_formatting_change_returns_no_preservation() -> None:
    result = classify_summary("Formatting change only to normalize whitespace.")
    assert result.event_type == NO_PRESERVATION


def test_dependency_decision_returns_dependency_decision() -> None:
    result = classify_summary("Continue using FastAPI instead of adding another package.")
    assert result.event_type == "dependency_decision"


def test_cost_driven_change_returns_cost_decision() -> None:
    result = classify_summary("Choose the cheaper provider to reduce token usage and maintenance burden.")
    assert result.event_type == "cost_decision"


def test_user_reversal_summary_returns_user_reversal() -> None:
    result = classify_summary("This approach is not working, abandon it.")
    assert result.event_type == "user_reversal"


def test_generated_card_parses_as_yaml_and_validates() -> None:
    card = generate_event_card("Continue using FastAPI instead of adding another package.")
    assert card is not None

    yaml_text = dump_yaml_text(card)
    parsed = parse_yaml_text(yaml_text)
    validate_card(parsed)
    assert parsed["type"] == "dependency_decision"


def test_generated_example_remains_valid() -> None:
    card = load_yaml_file(Path("examples/scp/generated_dependency_decision.yaml"))
    validate_card(card)


def test_built_origin_card_validates() -> None:
    card = build_origin_card(
        project_goal="Preserve important project decisions from adoption forward.",
        intended_users="Humans and AI maintainers.",
        important_constraints="Local-first and deterministic.",
        non_goals="Do not reconstruct old history.",
        success_criteria="Future sessions reuse preserved decisions.",
        next_known_step="Adopt SCP for the repository.",
    )
    validate_card(card)
    assert card["layer"] == "origin"
    assert "type" not in card


def test_origin_card_uses_only_approved_fields() -> None:
    card = build_origin_card(
        project_goal="Goal",
        intended_users="Users",
        important_constraints="Constraints",
        non_goals="Non-goals",
        success_criteria="Success criteria",
        next_known_step="Next step",
    )

    assert set(card.keys()).issubset(set(APPROVED_FIELDS))
    assert card.get("type") not in APPROVED_EVENT_TYPES
