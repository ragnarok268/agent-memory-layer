"""Deterministic YAML reader and writer for SCP cards."""

from __future__ import annotations

import json
from pathlib import Path


LIST_FIELDS = {"evidence", "constraints", "revisit_if"}
ORDERED_FIELDS = (
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


def _parse_scalar(token: str) -> str:
    token = token.strip()
    if token == "[]":
        raise ValueError("Empty list literal is only valid for list fields.")
    if token.startswith('"'):
        value = json.loads(token)
        if not isinstance(value, str):
            raise ValueError("Only string scalar values are supported.")
        return value
    return token


def parse_yaml_text(text: str) -> dict[str, object]:
    """Parse the narrow YAML subset used by SCP examples and generated cards."""
    data: dict[str, object] = {}
    current_list_key: str | None = None

    for line_number, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            if current_list_key is None:
                raise ValueError(f"Line {line_number}: list item without active list field.")
            current_value = data[current_list_key]
            assert isinstance(current_value, list)
            current_value.append(_parse_scalar(line[4:]))
            continue
        if line.startswith("  "):
            raise ValueError(f"Line {line_number}: unsupported indentation.")
        if ":" not in line:
            raise ValueError(f"Line {line_number}: expected key:value entry.")

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.lstrip()

        if value == "[]":
            data[key] = []
            current_list_key = None
            continue
        if value == "":
            data[key] = []
            current_list_key = key
            continue

        data[key] = _parse_scalar(value)
        current_list_key = None

    return data


def load_yaml_file(path: Path) -> dict[str, object]:
    return parse_yaml_text(path.read_text(encoding="utf-8"))


def _dump_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def dump_yaml_text(data: dict[str, object]) -> str:
    lines: list[str] = []
    seen_keys = set()
    for key in ORDERED_FIELDS:
        if key not in data:
            continue
        seen_keys.add(key)
        value = data[key]
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
                continue
            lines.append(f"{key}:")
            for item in value:
                if not isinstance(item, str):
                    raise TypeError(f"List field {key} supports only string items.")
                lines.append(f"  - {_dump_scalar(item)}")
            continue
        if not isinstance(value, str):
            raise TypeError(f"Field {key} supports only string values.")
        lines.append(f"{key}: {_dump_scalar(value)}")

    unexpected = [key for key in data.keys() if key not in seen_keys]
    if unexpected:
        raise ValueError(f"Unexpected keys for YAML output: {', '.join(unexpected)}")

    return "\n".join(lines) + "\n"


def write_yaml_file(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml_text(data), encoding="utf-8")
