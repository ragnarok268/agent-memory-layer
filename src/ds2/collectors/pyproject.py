"""pyproject.toml collector."""

from __future__ import annotations

from pathlib import Path

from ds2.collectors.requirements import parse_requirement_name
from ds2.graph.model import WarningRecord

import tomllib


def collect_pyproject(project_path: Path) -> tuple[list[dict[str, str | bool]], list[WarningRecord], bool]:
    pyproject_path = project_path / "pyproject.toml"
    if not pyproject_path.exists():
        return [], [], False

    warnings: list[WarningRecord] = []
    dependencies: list[dict[str, str | bool]] = []
    try:
        content = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except Exception as exc:
        warnings.append(WarningRecord(source="pyproject", message=f"Failed to parse pyproject.toml: {exc}"))
        return [], warnings, True

    project = content.get("project", {})
    for requirement in project.get("dependencies", []):
        name = parse_requirement_name(str(requirement))
        if name:
            dependencies.append({"name": name, "requirement": str(requirement), "build_only": False})

    build_system = content.get("build-system", {})
    for requirement in build_system.get("requires", []):
        name = parse_requirement_name(str(requirement))
        if name:
            dependencies.append({"name": name, "requirement": str(requirement), "build_only": True})

    optional = project.get("optional-dependencies", {})
    for group_name in sorted(optional):
        for requirement in optional[group_name]:
            name = parse_requirement_name(str(requirement))
            if name:
                dependencies.append(
                    {
                        "name": name,
                        "requirement": str(requirement),
                        "build_only": False,
                    }
                )
                warnings.append(
                    WarningRecord(
                        source="pyproject",
                        message=f"Optional dependency group '{group_name}' included as direct dependency for visibility.",
                    )
                )

    return dependencies, warnings, True
