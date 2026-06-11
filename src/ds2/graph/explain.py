"""Explanation helpers for package-level inspection."""

from __future__ import annotations

from ds2.graph.model import DependencyRecord


def explain_package(package_name: str, records: list[DependencyRecord]) -> str:
    for record in records:
        if record.name.lower() == package_name.lower():
            exposure_names = ", ".join(exposure.value for exposure in record.exposures)
            import_names = ", ".join(record.import_names) or "none"
            notes = "; ".join(record.notes) or "No extra notes."
            return (
                f"{record.name}: authority={record.authority_state.value}, "
                f"exposures=[{exposure_names}], imported={record.imported}, "
                f"source={record.source}, imports=[{import_names}]. {notes}"
            )
    return f"{package_name}: not found in the last scan graph."
