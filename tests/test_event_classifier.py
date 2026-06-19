from automation.event_classifier import classify_event


def test_dependency_change_triggers_ds2_labels():
    result = classify_event(["pyproject.toml"])

    assert "dependency_change" in result["labels"]
    assert "decision_worthy_change" in result["labels"]


def test_code_change_triggers_code_label():
    result = classify_event(["src/app.py"])

    assert "code_change" in result["labels"]


def test_docs_only_change_is_not_code_change_without_decision_signal():
    result = classify_event(["README.md", "docs/guide.md"])

    assert result["labels"] == ["docs_only_change"]


def test_import_surface_change_detected_from_diff():
    diff_text = "+import requests\n+import os\n"

    result = classify_event(["src/app.py"], diff_text=diff_text)

    assert "import_surface_change" in result["labels"]
    assert result["signals"]["import_lines"] == ["import requests", "import os"]


def test_decision_worthy_diff_detected_from_phrase():
    diff_text = "+We decided to keep the local-first architecture for security tradeoff reasons.\n"

    result = classify_event(["docs/notes.md"], diff_text=diff_text)

    assert "decision_worthy_change" in result["labels"]
