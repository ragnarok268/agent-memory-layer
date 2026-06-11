"""Path helpers for deterministic scans."""

from __future__ import annotations

from pathlib import Path


def normalize_path(path: Path) -> str:
    return path.resolve().as_posix()


def normalize_user_path(path: Path) -> str:
    return path.as_posix()


def ensure_output_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def relative_to(base: Path, candidate: Path) -> str:
    try:
        return candidate.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return candidate.resolve().as_posix()
