import json
from pathlib import Path
import subprocess
import sys

from tests.helpers import cleanup_tmp_dir, workspace_tmp_dir


def test_cli_scan_fixture_writes_expected_outputs() -> None:
    tmp_path = workspace_tmp_dir()
    output_dir = tmp_path / "ds2_output"
    fixture = Path("tests/fixtures/fastapi_app")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "ds2.cli", "scan", str(fixture), "--out", str(output_dir), "--json"],
            capture_output=True,
            text=True,
            check=True,
        )

        graph = json.loads(result.stdout)
        package_map = {item["name"]: item for item in graph["direct_dependencies"]}

        assert (output_dir / "DS2_REPORT.md").exists()
        assert (output_dir / "ds2_graph.json").exists()
        assert (output_dir / "ds2_receipt.json").exists()
        assert "fastapi" in package_map
        assert "NETWORK_SERVER" in package_map["fastapi"]["exposures"]
        assert "ASYNC_RUNTIME" in package_map["starlette"]["exposures"]
        assert "NETWORK_CLIENT" in package_map["httpx"]["exposures"]
        assert "DATABASE_PERSISTENCE" in package_map["sqlalchemy"]["exposures"]
    finally:
        cleanup_tmp_dir(tmp_path)


def test_cli_version_outputs_package_version() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ds2.cli", "version"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert result.stdout.strip() == "0.1.0"


def test_cli_scan_human_output_mentions_report_and_receipt() -> None:
    tmp_path = workspace_tmp_dir()
    output_dir = tmp_path / "ds2_output"
    fixture = Path("tests/fixtures/fastapi_app")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "ds2.cli", "scan", str(fixture), "--out", str(output_dir)],
            capture_output=True,
            text=True,
            check=True,
        )

        assert "DS2 report generated:" in result.stdout
        assert "DS2 receipt generated:" in result.stdout
    finally:
        cleanup_tmp_dir(tmp_path)
