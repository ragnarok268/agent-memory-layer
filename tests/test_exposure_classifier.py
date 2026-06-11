from ds2.classify.authority import classify_authority
from ds2.classify.exposure import classify_package
from ds2.graph.model import AuthorityState, ExposureClass


def test_exposure_classifier_maps_runtime_packages() -> None:
    assert classify_package("fastapi") == [ExposureClass.ASYNC_RUNTIME, ExposureClass.NETWORK_SERVER]
    assert classify_package("httpx") == [ExposureClass.ASYNC_RUNTIME, ExposureClass.NETWORK_CLIENT]
    assert classify_package("sqlalchemy") == [ExposureClass.DATABASE_PERSISTENCE]
    assert classify_package("setuptools", build_only=True) == [ExposureClass.BUILD_ONLY]


def test_authority_classifier_marks_high_attention_and_review() -> None:
    assert (
        classify_authority([ExposureClass.NETWORK_SERVER], imported=True)
        == AuthorityState.HIGH_ATTENTION
    )
    assert (
        classify_authority([ExposureClass.NETWORK_CLIENT], imported=True)
        == AuthorityState.REVIEW_RECOMMENDED
    )
