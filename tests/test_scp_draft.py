import shutil
from pathlib import Path

from automation.scp_draft import build_draft_markdown, write_scp_draft


TEST_WORK_ROOT = Path(__file__).resolve().parent.parent / "artifacts" / "_test_workspace"


def test_scp_draft_contains_plain_english_sections():
    classification = {
        "labels": ["dependency_change", "decision_worthy_change"],
        "signals": {
            "dependency_paths": ["pyproject.toml"],
            "architecture_paths": [],
            "decision_phrases": [],
        },
    }

    temp_dir = TEST_WORK_ROOT / "scp_draft_case"
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
        temp_dir.mkdir(parents=True, exist_ok=True)
        path = write_scp_draft(
            changed_paths=["pyproject.toml", "src/app.py"],
            classification=classification,
            diff_text="+decided to keep the existing dependency set\n",
            output_dir=temp_dir,
            timestamp="2026-06-17T12:00:00Z",
        )

        content = path.read_text(encoding="utf-8")
        assert "Draft only. This is not approved project memory." in content
        assert "Human review checklist" in content
        assert "`dependency_decision`" in content
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_build_draft_uses_fallback_when_no_diff():
    classification = {
        "labels": ["decision_worthy_change"],
        "signals": {
            "dependency_paths": [],
            "architecture_paths": [],
            "decision_phrases": ["constraint"],
        },
    }

    decision_type, markdown = build_draft_markdown(
        changed_paths=["docs/decisions/local-first.md"],
        classification=classification,
        diff_text="",
        timestamp="2026-06-17T12:00:00Z",
    )

    assert decision_type == "constraint_change"
    assert "No diff snippet provided." in markdown
