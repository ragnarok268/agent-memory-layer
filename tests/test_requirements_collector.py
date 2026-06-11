from pathlib import Path

from ds2.collectors.requirements import collect_requirements, parse_requirement_name


def test_parse_requirement_name_handles_versions_and_comments() -> None:
    assert parse_requirement_name("fastapi>=0.110") == "fastapi"
    assert parse_requirement_name("httpx[http2]==0.27.0 # pinned") == "httpx"
    assert parse_requirement_name("# comment") is None


def test_collect_requirements_reads_fixture() -> None:
    fixture = Path("tests/fixtures/fastapi_app")
    dependencies, warnings, found = collect_requirements(fixture)

    assert found is True
    assert warnings == []
    assert [item["name"] for item in dependencies] == ["fastapi", "httpx", "sqlalchemy"]
