import shutil
from pathlib import Path

from automation.intent_bootstrap import build_intent_draft, write_intent_draft


TEST_WORK_ROOT = Path(__file__).resolve().parent.parent / "artifacts" / "_test_workspace"


def test_python_project_inference_and_draft_fields():
    root_dir = TEST_WORK_ROOT / "intent_python_case"
    shutil.rmtree(root_dir, ignore_errors=True)
    root_dir.mkdir(parents=True, exist_ok=True)
    try:
        (root_dir / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
        (root_dir / "README.md").write_text(
            "local-first\nno telemetry\nhuman-readable\nmachine-readable\n",
            encoding="utf-8",
        )

        draft = build_intent_draft(root_dir, ["pyproject.toml", "src/app.py"], timestamp="2026-06-17T12:30:00Z")

        assert draft["status"] == "needs_human_review"
        assert draft["inferred_project_type"] == "python_project"
        assert "local_first_required" in draft["inferred_constraints"]
        assert "no_telemetry" in draft["inferred_constraints"]
        assert "human_readable_artifacts" in draft["inferred_constraints"]
        assert "machine_readable_artifacts" in draft["inferred_constraints"]
        assert "src/app.py" in draft["changed_files"]
    finally:
        shutil.rmtree(root_dir, ignore_errors=True)


def test_documentation_project_inference_works():
    root_dir = TEST_WORK_ROOT / "intent_docs_case"
    shutil.rmtree(root_dir, ignore_errors=True)
    root_dir.mkdir(parents=True, exist_ok=True)
    try:
        (root_dir / "README.md").write_text("do not claim standard\n", encoding="utf-8")
        docs_dir = root_dir / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        (docs_dir / "guide.md").write_text("human-readable\nmachine-readable\n", encoding="utf-8")

        draft = build_intent_draft(root_dir, ["README.md", "docs/guide.md"], timestamp="2026-06-17T12:30:00Z")

        assert draft["inferred_project_type"] == "documentation_project"
        assert draft["suggested_intent"].startswith("Preserve and explain")
        assert "do_not_claim_industry_standard" in draft["inferred_constraints"]
    finally:
        shutil.rmtree(root_dir, ignore_errors=True)


def test_write_intent_draft_creates_yaml_and_markdown():
    root_dir = TEST_WORK_ROOT / "intent_write_case"
    shutil.rmtree(root_dir, ignore_errors=True)
    root_dir.mkdir(parents=True, exist_ok=True)
    try:
        (root_dir / "README.md").write_text("no secrets\n", encoding="utf-8")
        result = write_intent_draft(
            changed_files=["README.md", "src/app.py"],
            root_dir=root_dir,
            timestamp="2026-06-17T12:30:00Z",
        )

        yaml_path = Path(result["yaml_path"])
        markdown_path = Path(result["markdown_path"])
        yaml_text = yaml_path.read_text(encoding="utf-8")

        assert yaml_path.exists()
        assert markdown_path.exists()
        assert 'status: "needs_human_review"' in yaml_text
        assert 'reason: "intent.yaml missing but IA verification was requested"' in yaml_text
        assert '  - "src/app.py"' in yaml_text
    finally:
        shutil.rmtree(root_dir, ignore_errors=True)
