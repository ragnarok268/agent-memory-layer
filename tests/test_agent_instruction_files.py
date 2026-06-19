from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

INSTRUCTION_FILES = [
    ROOT_DIR / "AGENTS.md",
    ROOT_DIR / "CLAUDE.md",
    ROOT_DIR / "GEMINI.md",
    ROOT_DIR / ".cursor" / "rules" / "engineering-knowledge-workflow.mdc",
]


def test_instruction_files_exist():
    for path in INSTRUCTION_FILES:
        assert path.exists(), f"Missing instruction file: {path}"


def test_instruction_files_reference_guardrails_and_summary():
    for path in INSTRUCTION_FILES:
        text = path.read_text(encoding="utf-8")
        assert "automation/guardrail_runner.py" in text
        assert "guardrail_summary.md" in text


def test_instruction_files_stay_compact():
    for path in INSTRUCTION_FILES:
        lines = path.read_text(encoding="utf-8").splitlines()
        assert len(lines) < 100, f"Instruction file too long: {path}"


def test_instruction_files_do_not_claim_formal_standard():
    forbidden = (
        "this methodology is an industry standard",
        "is an industry standard",
        "formal industry standard",
    )
    for path in INSTRUCTION_FILES:
        lowered = path.read_text(encoding="utf-8").lower()
        assert not any(phrase in lowered for phrase in forbidden), f"Standard claim found in {path}"
