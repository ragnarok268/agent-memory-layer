"""JSON report writer."""

from __future__ import annotations

from ds2.graph.model import ScanGraph
from ds2.util.json_stable import dumps_stable


def render_graph_json(graph: ScanGraph) -> str:
    return dumps_stable(graph.to_dict())
