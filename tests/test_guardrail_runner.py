import json
import shutil
from pathlib import Path

from automation.guardrail_runner import main


TEST_WORK_ROOT = Path(__file__).resolve().parent.parent / "artifacts" / "_test_workspace"


def test_runner_writes_summaries_and_skips_missing_tools(monkeypatch):
    root_dir = TEST_WORK_ROOT / "runner_summary_case"
    try:
        shutil.rmtree(root_dir, ignore_errors=True)
        root_dir.mkdir(parents=True, exist_ok=True)
        (root_dir / "intent.yaml").write_text("local_first: true\n", encoding="utf-8")
        monkeypatch.setattr("automation.guardrail_runner.ROOT_DIR", root_dir)
        monkeypatch.setattr("automation.guardrail_runner.shutil.which", lambda _: None)

        exit_code = main(["--changed", "pyproject.toml", "src/app.py"])

        assert exit_code == 0

        json_path = root_dir / "artifacts" / "knowledge" / "guardrail_summary.json"
        markdown_path = root_dir / "artifacts" / "knowledge" / "guardrail_summary.md"
        assert json_path.exists()
        assert markdown_path.exists()

        summary = json.loads(json_path.read_text(encoding="utf-8"))
        assert summary["checks"]["ia"]["status"] == "skipped"
        assert summary["checks"]["ds2"]["status"] == "skipped"
        assert summary["checks"]["scp_draft"]["status"] == "drafted"

        markdown = markdown_path.read_text(encoding="utf-8")
        assert "IA: skipped (not installed)" in markdown
        assert "DS2: skipped (not installed)" in markdown
        assert "SCP draft: drafted" in markdown
    finally:
        shutil.rmtree(root_dir, ignore_errors=True)


def test_runner_docs_only_does_not_trigger_ia(monkeypatch):
    root_dir = TEST_WORK_ROOT / "runner_docs_case"
    try:
        shutil.rmtree(root_dir, ignore_errors=True)
        root_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr("automation.guardrail_runner.ROOT_DIR", root_dir)
        monkeypatch.setattr("automation.guardrail_runner.shutil.which", lambda _: None)

        exit_code = main(["--changed", "README.md", "docs/guide.md"])

        assert exit_code == 0

        json_path = root_dir / "artifacts" / "knowledge" / "guardrail_summary.json"
        summary = json.loads(json_path.read_text(encoding="utf-8"))
        assert summary["classification"]["labels"] == ["docs_only_change"]
        assert summary["checks"]["ia"]["status"] == "not_needed"
    finally:
        shutil.rmtree(root_dir, ignore_errors=True)


def test_runner_decision_worthy_diff_file_generates_draft(monkeypatch):
    root_dir = TEST_WORK_ROOT / "runner_diff_case"
    try:
        shutil.rmtree(root_dir, ignore_errors=True)
        root_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr("automation.guardrail_runner.ROOT_DIR", root_dir)
        monkeypatch.setattr("automation.guardrail_runner.shutil.which", lambda _: None)

        diff_file = root_dir / "sample.diff"
        diff_file.write_text("+We decided to keep the local-first architecture.\n", encoding="utf-8")

        exit_code = main(["--changed", "docs/notes.md", "--diff-file", str(diff_file)])

        assert exit_code == 0

        json_path = root_dir / "artifacts" / "knowledge" / "guardrail_summary.json"
        summary = json.loads(json_path.read_text(encoding="utf-8"))
        draft_path = summary["checks"]["scp_draft"]["draft_path"]
        assert draft_path is not None
        assert Path(draft_path).exists()
    finally:
        shutil.rmtree(root_dir, ignore_errors=True)


def test_runner_bootstraps_intent_when_missing(monkeypatch):
    root_dir = TEST_WORK_ROOT / "runner_intent_bootstrap_case"
    try:
        shutil.rmtree(root_dir, ignore_errors=True)
        root_dir.mkdir(parents=True, exist_ok=True)
        (root_dir / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
        (root_dir / "README.md").write_text("local-first\nhuman-readable\nmachine-readable\n", encoding="utf-8")
        monkeypatch.setattr("automation.guardrail_runner.ROOT_DIR", root_dir)
        monkeypatch.setattr("automation.guardrail_runner.shutil.which", lambda _: None)

        exit_code = main(["--changed", "README.md", "pyproject.toml", "src/app.py"])

        assert exit_code == 0

        json_path = root_dir / "artifacts" / "knowledge" / "guardrail_summary.json"
        markdown_path = root_dir / "artifacts" / "knowledge" / "guardrail_summary.md"
        intent_yaml = root_dir / "artifacts" / "knowledge" / "intent_draft.yaml"
        intent_markdown = root_dir / "artifacts" / "knowledge" / "intent_draft.md"

        summary = json.loads(json_path.read_text(encoding="utf-8"))
        assert summary["checks"]["ia"]["status"] == "blocked_until_intent_approved"
        assert summary["checks"]["ia"]["intent_draft_yaml"] == intent_yaml.as_posix()
        assert summary["checks"]["ia"]["intent_draft_markdown"] == intent_markdown.as_posix()
        assert intent_yaml.exists()
        assert intent_markdown.exists()

        yaml_text = intent_yaml.read_text(encoding="utf-8")
        assert 'status: "needs_human_review"' in yaml_text
        assert '  - "src/app.py"' in yaml_text

        markdown_text = markdown_path.read_text(encoding="utf-8")
        assert "Intent bootstrap created" in markdown_text
        assert "IA was not run because `intent.yaml` is missing." in markdown_text
    finally:
        shutil.rmtree(root_dir, ignore_errors=True)


def test_runner_does_not_create_intent_draft_when_intent_exists(monkeypatch):
    root_dir = TEST_WORK_ROOT / "runner_intent_exists_case"
    try:
        shutil.rmtree(root_dir, ignore_errors=True)
        root_dir.mkdir(parents=True, exist_ok=True)
        (root_dir / "intent.yaml").write_text("local_first: true\n", encoding="utf-8")
        monkeypatch.setattr("automation.guardrail_runner.ROOT_DIR", root_dir)
        monkeypatch.setattr("automation.guardrail_runner.shutil.which", lambda _: None)

        exit_code = main(["--changed", "src/app.py"])

        assert exit_code == 0

        summary = json.loads((root_dir / "artifacts" / "knowledge" / "guardrail_summary.json").read_text(encoding="utf-8"))
        assert summary["checks"]["ia"]["status"] == "skipped"
        assert not (root_dir / "artifacts" / "knowledge" / "intent_draft.yaml").exists()
    finally:
        shutil.rmtree(root_dir, ignore_errors=True)
