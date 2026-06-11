import json
from pathlib import Path

from ds2.scan import run_scan
from tests.helpers import cleanup_tmp_dir, workspace_tmp_dir


def test_repeated_scans_produce_stable_hashes() -> None:
    fixture = Path("tests/fixtures/fastapi_app")
    tmp_path = workspace_tmp_dir()
    output_dir = tmp_path / "ds2_output"

    try:
        first = run_scan(fixture, output_dir)
        second = run_scan(fixture, output_dir)

        assert first["receipt_sha256"] == second["receipt_sha256"]
        assert first["report_sha256"] == second["report_sha256"]
        assert first["graph_sha256"] == second["graph_sha256"]
        assert (output_dir / "DS2_REPORT.md").read_text(encoding="utf-8") == first["report_text"]

        receipt = json.loads((output_dir / "ds2_receipt.json").read_text(encoding="utf-8"))
        assert receipt["report_sha256"] == first["report_sha256"]
        assert receipt["graph_sha256"] == first["graph_sha256"]
    finally:
        cleanup_tmp_dir(tmp_path)
