"""SCP schema validation."""

from __future__ import annotations

from pathlib import Path

from scp.canon import (
    APPROVED_CARD_LAYERS,
    APPROVED_EVENT_TYPES,
    APPROVED_FIELDS,
    APPROVED_LIFECYCLE_STATES,
    APPROVED_PRESERVATION_VALUES,
    EVENT_REQUIRED_FIELDS,
    NON_EVENT_REQUIRED_FIELDS,
)
from scp.yamlio import load_yaml_file


class SchemaError(ValueError):
    """Raised when an SCP card fails validation."""


def _expect_string_list(card: dict[str, object], field: str) -> None:
    value = card[field]
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise SchemaError(f"Field '{field}' must be a list of strings.")


def _expect_string(card: dict[str, object], field: str) -> None:
    value = card[field]
    if not isinstance(value, str) or value == "":
        raise SchemaError(f"Field '{field}' must be a non-empty string.")


def validate_card(card: dict[str, object]) -> None:
    unknown_fields = sorted(key for key in card.keys() if key not in APPROVED_FIELDS)
    if unknown_fields:
        raise SchemaError(f"Unknown field(s): {', '.join(unknown_fields)}")

    layer = card.get("layer")
    if layer not in APPROVED_CARD_LAYERS:
        raise SchemaError(f"Unknown layer: {layer}")

    status = card.get("status")
    if status not in APPROVED_LIFECYCLE_STATES:
        raise SchemaError(f"Unknown lifecycle state: {status}")

    required_fields = EVENT_REQUIRED_FIELDS if layer == "event" else NON_EVENT_REQUIRED_FIELDS
    missing_fields = [field for field in required_fields if field not in card]
    if missing_fields:
        raise SchemaError(f"Missing required field(s): {', '.join(missing_fields)}")

    if layer == "event":
        event_type = card.get("type")
        if event_type not in APPROVED_EVENT_TYPES:
            raise SchemaError(f"Unknown event type: {event_type}")
    elif "type" in card:
        raise SchemaError("Field 'type' is only valid for event cards.")

    preservation_value = card.get("preservation_value")
    if preservation_value not in APPROVED_PRESERVATION_VALUES:
        raise SchemaError(f"Invalid preservation_value: {preservation_value}")

    for field in required_fields:
        if field in {"evidence", "constraints", "revisit_if"}:
            _expect_string_list(card, field)
        else:
            _expect_string(card, field)

    if "supersedes" in card:
        _expect_string(card, "supersedes")


def validate_path(path: Path) -> list[Path]:
    validated_paths: list[Path] = []
    if path.is_dir():
        candidates = sorted(
            candidate
            for candidate in path.rglob("*")
            if candidate.is_file() and candidate.suffix.lower() in {".yaml", ".yml"}
        )
    else:
        candidates = [path]

    if not candidates:
        raise SchemaError(f"No YAML files found at {path}")

    for candidate in candidates:
        validate_card(load_yaml_file(candidate))
        validated_paths.append(candidate)

    return validated_paths
