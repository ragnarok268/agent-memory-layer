"""Installed distribution fallback collector."""

from __future__ import annotations

from collections import defaultdict
from importlib import metadata

from ds2.collectors.requirements import parse_requirement_name
from ds2.graph.model import WarningRecord


def collect_installed_fallback(observed_imports: dict[str, list[str]]) -> tuple[list[dict[str, object]], list[WarningRecord]]:
    warnings: list[WarningRecord] = []
    if not observed_imports:
        return [], warnings

    try:
        packages_to_distributions = metadata.packages_distributions()
    except Exception as exc:
        warnings.append(WarningRecord(source="installed", message=f"Installed metadata unavailable: {exc}"))
        return [], warnings

    dependencies: list[dict[str, object]] = []
    for package_name, import_names in sorted(observed_imports.items()):
        distribution_names: set[str] = set()
        for import_name in import_names:
            distribution_names.update(packages_to_distributions.get(import_name, []))

        if not distribution_names:
            distribution_names.add(package_name)

        for distribution_name in sorted(distribution_names):
            requires: list[str] = []
            try:
                dist = metadata.distribution(distribution_name)
                for item in dist.requires or []:
                    parsed = parse_requirement_name(item)
                    if parsed:
                        requires.append(parsed)
            except Exception:
                pass

            dependencies.append(
                {
                    "name": distribution_name,
                    "import_names": list(import_names),
                    "requires_dist": sorted(set(requires)),
                }
            )

    return dependencies, warnings
