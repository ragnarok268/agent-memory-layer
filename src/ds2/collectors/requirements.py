"""requirements.txt collector."""

from __future__ import annotations

from pathlib import Path
import re

from ds2.graph.model import WarningRecord

try:
    from packaging.requirements import Requirement
except Exception:  # pragma: no cover - optional dependency
    Requirement = None


REQ_SPLIT = re.compile(r"[<>=!~\[\]; ]")


def parse_requirement_name(line: str) -> str | None:
    raw = line.strip()
    if not raw or raw.startswith("#") or raw.startswith(("-r ", "--requirement ")):
        return None
    candidate = raw.split("#", 1)[0].strip()
    if not candidate:
        return None
    if Requirement is not None:
        try:
            return Requirement(candidate).name
        except Exception:
            pass
    parts = REQ_SPLIT.split(candidate, maxsplit=1)
    return parts[0] if parts and parts[0] else None


def collect_requirements(project_path: Path) -> tuple[list[dict[str, str]], list[WarningRecord], bool]:
    requirements_path = project_path / "requirements.txt"
    if not requirements_path.exists():
        return [], [], False

    dependencies: list[dict[str, str]] = []
    warnings: list[WarningRecord] = []
    try:
        for line_number, line in enumerate(requirements_path.read_text(encoding="utf-8").splitlines(), start=1):
            name = parse_requirement_name(line)
            if name is None:
                continue
            dependencies.append({"name": name, "requirement": line.strip()})
    except Exception as exc:
        warnings.append(WarningRecord(source="requirements", message=f"Failed to read requirements.txt: {exc}"))

    return dependencies, warnings, True
