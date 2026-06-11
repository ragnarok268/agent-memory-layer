"""Core graph models for DS2."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum


class ExposureClass(StrEnum):
    NETWORK_SERVER = "NETWORK_SERVER"
    NETWORK_CLIENT = "NETWORK_CLIENT"
    ASYNC_RUNTIME = "ASYNC_RUNTIME"
    PROCESS_EXECUTION = "PROCESS_EXECUTION"
    BROWSER_AUTOMATION = "BROWSER_AUTOMATION"
    DATABASE_PERSISTENCE = "DATABASE_PERSISTENCE"
    CACHE_OR_QUEUE = "CACHE_OR_QUEUE"
    FILESYSTEM_ACCESS = "FILESYSTEM_ACCESS"
    CLOUD_API = "CLOUD_API"
    SERIALIZATION_PARSER = "SERIALIZATION_PARSER"
    PLUGIN_OR_EXTENSION = "PLUGIN_OR_EXTENSION"
    BUILD_ONLY = "BUILD_ONLY"
    UNKNOWN = "UNKNOWN"


class AuthorityState(StrEnum):
    OBSERVED = "OBSERVED"
    RUNTIME_EXPOSED = "RUNTIME_EXPOSED"
    REVIEW_RECOMMENDED = "REVIEW_RECOMMENDED"
    HIGH_ATTENTION = "HIGH_ATTENTION"


@dataclass(slots=True)
class WarningRecord:
    source: str
    message: str


@dataclass(slots=True)
class DependencyRecord:
    name: str
    requirement: str | None = None
    source: str = "unknown"
    direct: bool = False
    imported: bool = False
    installed: bool = False
    import_names: list[str] = field(default_factory=list)
    exposures: list[ExposureClass] = field(default_factory=list)
    authority_state: AuthorityState = AuthorityState.OBSERVED
    build_only: bool = False
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["authority_state"] = self.authority_state.value
        data["exposures"] = [item.value for item in self.exposures]
        return data


@dataclass(slots=True)
class EdgeRecord:
    source: str
    target: str
    relation: str

    def to_dict(self) -> dict[str, str]:
        return {"source": self.source, "target": self.target, "relation": self.relation}


@dataclass(slots=True)
class ScanGraph:
    project_path: str
    dependency_sources: list[str]
    direct_dependencies: list[DependencyRecord]
    observed_imports: list[str]
    dependency_chains: list[list[str]]
    edges: list[EdgeRecord]
    warnings: list[WarningRecord]
    transitive_partial: bool
    manual_review_notes: list[str]
    build_runtime_notes: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "project_path": self.project_path,
            "dependency_sources": self.dependency_sources,
            "direct_dependencies": [item.to_dict() for item in self.direct_dependencies],
            "observed_imports": self.observed_imports,
            "dependency_chains": self.dependency_chains,
            "edges": [item.to_dict() for item in self.edges],
            "warnings": [asdict(item) for item in self.warnings],
            "transitive_partial": self.transitive_partial,
            "manual_review_notes": self.manual_review_notes,
            "build_runtime_notes": self.build_runtime_notes,
        }
