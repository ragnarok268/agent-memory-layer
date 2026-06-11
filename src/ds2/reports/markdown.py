"""Markdown report writer."""

from __future__ import annotations

from collections import Counter

from ds2.graph.model import DependencyRecord, ExposureClass, ScanGraph


def render_markdown_report(graph: ScanGraph, receipt_hash: str) -> str:
    lines: list[str] = [
        "# DS2 Report",
        "",
        "DS2 is `ps + netstat + tree for dependency/runtime authority`.",
        "",
        "## 1. Project path",
        "",
        f"- `{graph.project_path}`",
        "",
        "## 2. Detected dependency sources",
        "",
    ]
    lines.extend(_list_or_none(graph.dependency_sources))
    lines.extend(
        [
            "",
            "## 3. Direct dependencies",
            "",
        ]
    )
    direct_records = [record for record in graph.direct_dependencies if record.direct]
    if direct_records:
        lines.extend(_dependency_table(direct_records))
    else:
        lines.append("- None detected.")

    lines.extend(
        [
            "",
            "## 4. Import-observed packages",
            "",
        ]
    )
    lines.extend(_list_or_none(graph.observed_imports))
    lines.extend(
        [
            "",
            "## 5. Runtime exposure classifications",
            "",
        ]
    )
    lines.extend(_exposure_lines(graph.direct_dependencies))
    lines.extend(
        [
            "",
            "## 6. Authority expansion notes",
            "",
        ]
    )
    authority_lines = 0
    for record in graph.direct_dependencies:
        if record.authority_state.value != "OBSERVED" or record.notes:
            authority_lines += 1
            lines.append(
                f"- `{record.name}`: {record.authority_state.value}; "
                f"exposures={', '.join(exposure.value for exposure in record.exposures)}."
            )
    if authority_lines == 0:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "## 7. Build-time vs runtime exposure",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in graph.build_runtime_notes)
    lines.extend(
        [
            "",
            "## 8. Dependency chains if available",
            "",
        ]
    )
    if graph.dependency_chains:
        lines.extend(f"- `{' -> '.join(chain)}`" for chain in graph.dependency_chains)
    else:
        lines.append("- No dependency chains available.")
    lines.extend(
        [
            "",
            "## 9. Manual review notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in graph.manual_review_notes)
    if graph.warnings:
        for warning in graph.warnings:
            lines.append(f"- Warning [{warning.source}]: {warning.message}")
    lines.extend(
        [
            "",
            "## 10. Deterministic receipt hash",
            "",
            f"- `{receipt_hash}`",
        ]
    )
    return "\n".join(lines) + "\n"


def _list_or_none(items: list[str]) -> list[str]:
    return [f"- `{item}`" for item in items] or ["- None detected."]


def _dependency_table(records: list[DependencyRecord]) -> list[str]:
    lines = [
        "| Package | Source | Imported | Exposures | Authority |",
        "| --- | --- | --- | --- | --- |",
    ]
    for record in records:
        exposures = ", ".join(exposure.value for exposure in record.exposures)
        lines.append(
            f"| `{record.name}` | `{record.source}` | `{str(record.imported).lower()}` | `{exposures}` | `{record.authority_state.value}` |"
        )
    return lines


def _exposure_lines(records: list[DependencyRecord]) -> list[str]:
    counts = Counter(exposure.value for record in records for exposure in record.exposures)
    lines = [f"- `{name}`: {counts[name]}" for name in sorted(counts)]
    if not lines:
        return ["- No exposures classified."]
    high_signal = [
        f"- `{record.name}` -> {', '.join(exposure.value for exposure in record.exposures)}"
        for record in records
        if record.exposures != [ExposureClass.UNKNOWN]
    ]
    return lines + high_signal
