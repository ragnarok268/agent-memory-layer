from ds2.collectors.pyproject import collect_pyproject
from tests.helpers import cleanup_tmp_dir, workspace_tmp_dir


def test_collect_pyproject_reads_project_and_build_requirements() -> None:
    tmp_path = workspace_tmp_dir()
    try:
        (tmp_path / "pyproject.toml").write_text(
            """
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "demo"
version = "0.1.0"
dependencies = ["fastapi>=0.100", "httpx"]
""".strip()
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

        dependencies, warnings, found = collect_pyproject(tmp_path)

        assert found is True
        assert warnings == []
        names = [item["name"] for item in dependencies]
        assert names == ["fastapi", "httpx", "setuptools", "wheel"]
        assert [item["build_only"] for item in dependencies] == [False, False, True, True]
    finally:
        cleanup_tmp_dir(tmp_path)
