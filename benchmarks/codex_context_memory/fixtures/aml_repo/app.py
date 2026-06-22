"""Small local-only project used by the benchmark fixtures."""

from __future__ import annotations

import json
from pathlib import Path


DEFAULT_CONFIG = {
    "project_name": "sample-local-project",
    "local_only": True,
}


def load_config(path: str | Path = "project_config.json") -> dict:
    config_path = Path(path)
    if not config_path.exists():
        return dict(DEFAULT_CONFIG)
    return json.loads(config_path.read_text(encoding="utf-8"))


def is_configured(config: dict | None = None) -> bool:
    active_config = config or load_config()
    return bool(active_config.get("project_name")) and active_config.get("local_only") is True


def summarize_project(name: str, completed_tasks: int = 0, open_tasks: int = 0) -> dict:
    return {
        "name": name,
        "completed_tasks": int(completed_tasks),
        "open_tasks": int(open_tasks),
    }


def format_summary(summary: dict) -> str:
    return (
        f"{summary['name']}: "
        f"{summary['completed_tasks']} completed, "
        f"{summary['open_tasks']} open"
    )


FEATURE_FLAGS = {
    "experimental_summary_view": False,
}


def is_feature_enabled(flag_name: str, flags: dict | None = None) -> bool:
    active_flags = flags or FEATURE_FLAGS
    return bool(active_flags.get(flag_name, False))


def normalize_status(value: str) -> str:
    return value.strip().lower()
