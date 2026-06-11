import json
from pathlib import Path

from ds2.scan import run_scan
from tests.helpers import cleanup_tmp_dir, workspace_tmp_dir


def test_example_fastapi_artifacts_match_committed_outputs() -> None:
    example_dir = Path("examples/fastapi_app")
    tmp_path = workspace_tmp_dir()
    output_dir = tmp_path / "golden_compare"

    try:
        result = run_scan(example_dir, output_dir)

        assert result["report_text"] == (example_dir / "DS2_REPORT.md").read_text(encoding="utf-8")
        assert result["graph_text"] == (example_dir / "ds2_graph.json").read_text(encoding="utf-8")
        assert result["receipt_text"] == (example_dir / "ds2_receipt.json").read_text(encoding="utf-8")
    finally:
        cleanup_tmp_dir(tmp_path)


def test_fixture_fastapi_outputs_match_golden_files() -> None:
    fixture_dir = Path("tests/fixtures/fastapi_app")
    golden_dir = fixture_dir / "golden"
    tmp_path = workspace_tmp_dir()
    output_dir = tmp_path / "fixture_compare"

    try:
        result = run_scan(fixture_dir, output_dir)

        assert result["report_text"] == (golden_dir / "DS2_REPORT.md").read_text(encoding="utf-8")
        assert result["graph_text"] == (golden_dir / "ds2_graph.json").read_text(encoding="utf-8")
        assert result["receipt_text"] == (golden_dir / "ds2_receipt.json").read_text(encoding="utf-8")

        receipt = json.loads(result["receipt_text"])
        assert receipt["scanned_path"] == "tests/fixtures/fastapi_app"
        assert receipt["generated_files"] == ["DS2_REPORT.md", "ds2_graph.json", "ds2_receipt.json"]
    finally:
        cleanup_tmp_dir(tmp_path)
