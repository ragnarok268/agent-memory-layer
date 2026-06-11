"""Graph assembly for DS2 scan results."""

from __future__ import annotations

from collections import Counter

from ds2.classify.authority import classify_authority
from ds2.classify.exposure import classify_package
from ds2.graph.model import DependencyRecord, EdgeRecord, ExposureClass, ScanGraph, WarningRecord


def build_graph(
    *,
    project_path: str,
    dependency_sources: list[str],
    collected_dependencies: list[dict[str, object]],
    observed_imports: dict[str, list[str]],
    installed_fallback: list[dict[str, object]],
    warnings: list[WarningRecord],
) -> ScanGraph:
    records: dict[str, DependencyRecord] = {}
    edges: list[EdgeRecord] = []
    dependency_chains: list[list[str]] = []
    transitive_partial = True

    def get_record(name: str) -> DependencyRecord:
        key = name.lower()
        if key not in records:
            records[key] = DependencyRecord(name=name)
        return records[key]

    for item in collected_dependencies:
        name = str(item["name"])
        record = get_record(name)
        record.name = name
        record.requirement = str(item.get("requirement") or "") or None
        record.source = str(item.get("source") or record.source)
        record.direct = True
        record.build_only = bool(item.get("build_only", False))

    for package_name, import_names in observed_imports.items():
        record = get_record(package_name)
        record.imported = True
        record.import_names = sorted(set(record.import_names + import_names))
        if record.source == "unknown":
            record.source = "imports"

    if not collected_dependencies and installed_fallback:
        for item in installed_fallback:
            name = str(item["name"])
            record = get_record(name)
            record.installed = True
            record.source = "installed"
            record.imported = True
            record.import_names = sorted(set(record.import_names + list(item.get("import_names", []))))
            requires_dist = list(item.get("requires_dist", []))
            if requires_dist:
                transitive_partial = False
                for dep_name in requires_dist:
                    edges.append(EdgeRecord(source=name, target=dep_name, relation="requires_dist"))
                    dependency_chains.append([name, dep_name])
    elif installed_fallback:
        for item in installed_fallback:
            name = str(item["name"])
            requires_dist = list(item.get("requires_dist", []))
            if requires_dist:
                transitive_partial = False
                for dep_name in requires_dist:
                    edges.append(EdgeRecord(source=name, target=dep_name, relation="requires_dist"))
                    dependency_chains.append([name, dep_name])

    direct_dependencies = sorted(records.values(), key=lambda item: item.name.lower())
    for record in direct_dependencies:
        record.exposures = classify_package(record.name, build_only=record.build_only)
        if record.import_names:
            import_exposures: list[ExposureClass] = []
            for import_name in record.import_names:
                import_exposures.extend(classify_package(import_name))
            record.exposures = sorted(set(record.exposures + import_exposures), key=lambda item: item.value)
        record.authority_state = classify_authority(record.exposures, imported=record.imported)
        if record.imported and ExposureClass.UNKNOWN in record.exposures and len(record.exposures) == 1:
            record.notes.append("Imported in source but not mapped to a specialized exposure class.")
        if record.build_only:
            record.notes.append("Observed in build-system requirements; runtime use not confirmed.")
        if record.imported and record.direct:
            record.notes.append("Direct dependency is also observed in source imports.")

    exposure_counts = Counter(
        exposure.value
        for record in direct_dependencies
        for exposure in record.exposures
    )
    manual_review_notes = build_manual_review_notes(direct_dependencies, warnings)
    build_runtime_notes = build_build_runtime_notes(direct_dependencies, exposure_counts, transitive_partial)
    return ScanGraph(
        project_path=project_path,
        dependency_sources=sorted(set(dependency_sources)),
        direct_dependencies=direct_dependencies,
        observed_imports=sorted(observed_imports),
        dependency_chains=sorted(dependency_chains),
        edges=sorted(edges, key=lambda item: (item.source.lower(), item.target.lower(), item.relation)),
        warnings=sorted(warnings, key=lambda item: (item.source, item.message)),
        transitive_partial=transitive_partial,
        manual_review_notes=manual_review_notes,
        build_runtime_notes=build_runtime_notes,
    )


def build_manual_review_notes(records: list[DependencyRecord], warnings: list[WarningRecord]) -> list[str]:
    notes: list[str] = []
    if warnings:
        notes.append("Warnings were emitted during scanning; validate malformed files and partial graph coverage.")
    if any(record.authority_state.value == "HIGH_ATTENTION" for record in records):
        notes.append("High-attention packages expand execution authority and should be reviewed for actual runtime reachability.")
    if any(record.exposures == [ExposureClass.UNKNOWN] for record in records if record.imported):
        notes.append("Some imported packages were not mapped to a specialized exposure class and need human triage.")
    if not notes:
        notes.append("No immediate manual-review blockers were detected, but runtime paths should still be spot-checked.")
    return notes


def build_build_runtime_notes(
    records: list[DependencyRecord], exposure_counts: Counter[str], transitive_partial: bool
) -> list[str]:
    build_only = sorted(record.name for record in records if record.build_only)
    runtime = sorted(record.name for record in records if record.imported)
    notes = [
        f"Build-only dependencies: {', '.join(build_only) if build_only else 'none detected'}.",
        f"Runtime-observed packages: {', '.join(runtime) if runtime else 'none detected'}.",
        f"Transitive dependency graph is {'partial' if transitive_partial else 'best-effort via installed metadata'}.",
        f"Exposure classes observed: {', '.join(sorted(name for name, count in exposure_counts.items() if count)) or 'UNKNOWN only'}.",
    ]
    return notes
