"""Authority classification derived from exposure observations."""

from __future__ import annotations

from ds2.graph.model import AuthorityState, ExposureClass


HIGH_ATTENTION = {
    ExposureClass.NETWORK_SERVER,
    ExposureClass.PROCESS_EXECUTION,
    ExposureClass.BROWSER_AUTOMATION,
    ExposureClass.CLOUD_API,
}

REVIEW_RECOMMENDED = {
    ExposureClass.DATABASE_PERSISTENCE,
    ExposureClass.CACHE_OR_QUEUE,
    ExposureClass.NETWORK_CLIENT,
    ExposureClass.SERIALIZATION_PARSER,
    ExposureClass.PLUGIN_OR_EXTENSION,
}


def classify_authority(exposures: list[ExposureClass], *, imported: bool) -> AuthorityState:
    unique = set(exposures)
    if unique & HIGH_ATTENTION:
        return AuthorityState.HIGH_ATTENTION
    if unique & REVIEW_RECOMMENDED:
        return AuthorityState.REVIEW_RECOMMENDED
    if unique and unique != {ExposureClass.UNKNOWN} and imported:
        return AuthorityState.RUNTIME_EXPOSED
    return AuthorityState.OBSERVED
