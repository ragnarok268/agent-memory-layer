"""Top-level scan orchestration."""

from __future__ import annotations

from pathlib import Path

from ds2 import __version__
from ds2.collectors.imports import scan_imports
from ds2.collectors.installed import collect_installed_fallback
from ds2.collectors.pyproject import collect_pyproject
from ds2.collectors.requirements import collect_requirements
from ds2.graph.build import build_graph
from ds2.reports.json_report import render_graph_json
from ds2.reports.markdown import render_markdown_report
from ds2.receipts.receipt import build_receipt
from ds2.util.json_stable import dumps_stable, sha256_text
from ds2.util.paths import ensure_output_dir, normalize_path, normalize_user_path


def run_scan(project_path: Path, output_dir: Path) -> dict[str, object]:
    requested_project_path = normalize_user_path(project_path)
    project_path = project_path.resolve()
    output_dir = ensure_output_dir(output_dir.resolve())

    warnings = []
    dependency_sources: list[str] = []
    collected_dependencies: list[dict[str, object]] = []

    requirements, req_warnings, found_requirements = collect_requirements(project_path)
    warnings.extend(req_warnings)
    if found_requirements:
        dependency_sources.append("requirements.txt")
        for item in requirements:
            collected_dependencies.append({**item, "source": "requirements.txt", "build_only": False})

    pyproject_dependencies, pyproject_warnings, found_pyproject = collect_pyproject(project_path)
    warnings.extend(pyproject_warnings)
    if found_pyproject:
        dependency_sources.append("pyproject.toml")
        for item in pyproject_dependencies:
            collected_dependencies.append({**item, "source": "pyproject.toml"})

    observed_imports, import_warnings = scan_imports(project_path)
    warnings.extend(import_warnings)
    if observed_imports:
        dependency_sources.append("source_import_scan")

    installed_fallback, installed_warnings = collect_installed_fallback(observed_imports)
    warnings.extend(installed_warnings)
    if installed_fallback and not collected_dependencies:
        dependency_sources.append("installed_metadata")

    graph = build_graph(
        project_path=requested_project_path,
        dependency_sources=dependency_sources,
        collected_dependencies=collected_dependencies,
        observed_imports=observed_imports,
        installed_fallback=installed_fallback,
        warnings=warnings,
    )

    graph_text = render_graph_json(graph)
    graph_sha256 = sha256_text(graph_text)
    generated_files = ["DS2_REPORT.md", "ds2_graph.json", "ds2_receipt.json"]
    report_text = render_markdown_report(graph, "<pending-receipt-hash>")
    report_sha256 = sha256_text(report_text)
    receipt_data, receipt_hash = build_receipt(
        tool_name="ds2",
        version=__version__,
        scanned_path=requested_project_path,
        graph=graph,
        generated_files=generated_files,
        report_sha256=report_sha256,
        graph_sha256=graph_sha256,
    )
    report_text = render_markdown_report(graph, receipt_hash)
    report_sha256 = sha256_text(report_text)
    receipt_data["report_sha256"] = report_sha256
    receipt_text = dumps_stable(receipt_data)

    paths_to_text = {
        output_dir / "DS2_REPORT.md": report_text,
        output_dir / "ds2_graph.json": graph_text,
        output_dir / "ds2_receipt.json": receipt_text,
    }
    for path, text in paths_to_text.items():
        path.write_text(text, encoding="utf-8", newline="\n")

    return {
        "graph": graph,
        "graph_text": graph_text,
        "graph_sha256": graph_sha256,
        "report_text": report_text,
        "report_sha256": report_sha256,
        "receipt": receipt_data,
        "receipt_text": receipt_text,
        "receipt_sha256": receipt_hash,
        "generated_files": [normalize_path(path) for path in sorted(paths_to_text)],
    }
