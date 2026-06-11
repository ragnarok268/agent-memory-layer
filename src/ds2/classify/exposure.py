"""Runtime exposure classification."""

from __future__ import annotations

from ds2.graph.model import ExposureClass


PACKAGE_EXPOSURES: dict[str, list[ExposureClass]] = {
    "fastapi": [ExposureClass.NETWORK_SERVER, ExposureClass.ASYNC_RUNTIME],
    "starlette": [ExposureClass.NETWORK_SERVER, ExposureClass.ASYNC_RUNTIME],
    "flask": [ExposureClass.NETWORK_SERVER],
    "django": [ExposureClass.NETWORK_SERVER],
    "requests": [ExposureClass.NETWORK_CLIENT],
    "httpx": [ExposureClass.NETWORK_CLIENT, ExposureClass.ASYNC_RUNTIME],
    "subprocess": [ExposureClass.PROCESS_EXECUTION],
    "sqlite3": [ExposureClass.DATABASE_PERSISTENCE],
    "sqlalchemy": [ExposureClass.DATABASE_PERSISTENCE],
    "redis": [ExposureClass.CACHE_OR_QUEUE],
    "celery": [ExposureClass.CACHE_OR_QUEUE, ExposureClass.ASYNC_RUNTIME],
    "boto3": [ExposureClass.CLOUD_API],
    "playwright": [ExposureClass.BROWSER_AUTOMATION],
    "selenium": [ExposureClass.BROWSER_AUTOMATION],
    "yaml": [ExposureClass.SERIALIZATION_PARSER],
    "pydantic": [ExposureClass.SERIALIZATION_PARSER],
    "pluggy": [ExposureClass.PLUGIN_OR_EXTENSION],
    "setuptools": [ExposureClass.BUILD_ONLY],
    "wheel": [ExposureClass.BUILD_ONLY],
}


def classify_package(package_name: str, *, build_only: bool = False) -> list[ExposureClass]:
    normalized = package_name.strip().lower().replace("_", "-")
    if build_only:
        return [ExposureClass.BUILD_ONLY]

    direct_match = PACKAGE_EXPOSURES.get(normalized)
    if direct_match:
        return sorted(set(direct_match), key=lambda item: item.value)

    dotted_base = normalized.split(".")[0]
    alt_match = PACKAGE_EXPOSURES.get(dotted_base)
    if alt_match:
        return sorted(set(alt_match), key=lambda item: item.value)

    return [ExposureClass.UNKNOWN]
