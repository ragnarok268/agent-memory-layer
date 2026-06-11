"""Receipt generation for deterministic scan outputs."""

from __future__ import annotations

from collections import Counter

from ds2.graph.model import ScanGraph
from ds2.util.json_stable import dumps_stable, sha256_text


def build_receipt(
    *,
    tool_name: str,
    version: str,
    scanned_path: str,
    graph: ScanGraph,
    generated_files: list[str],
    report_sha256: str,
    graph_sha256: str,
) -> tuple[dict[str, object], str]:
    exposure_counts = Counter(exposure.value for record in graph.direct_dependencies for exposure in record.exposures)
    receipt = {
        "tool_name": tool_name,
        "version": version,
        "scanned_path": scanned_path,
        "dependency_count": len(graph.direct_dependencies),
        "exposure_counts": {name: exposure_counts[name] for name in sorted(exposure_counts)},
        "warning_count": len(graph.warnings),
        "generated_files": sorted(generated_files),
        "report_sha256": report_sha256,
        "graph_sha256": graph_sha256,
    }
    hash_payload = {key: value for key, value in receipt.items() if key != "report_sha256"}
    return receipt, sha256_text(dumps_stable(hash_payload))
