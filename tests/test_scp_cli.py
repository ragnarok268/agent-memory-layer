from pathlib import Path
import subprocess
import sys

from tests.helpers import cleanup_tmp_dir, pythonpath_env, workspace_tmp_dir


def test_scp_cli_validate_passes_for_example() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "scp.cli", "validate", "examples/scp/SCP-0007.yaml"],
        capture_output=True,
        text=True,
        check=True,
        env=pythonpath_env(),
    )

    assert result.stdout.strip() == "Validated 1 file(s)."


def test_scp_cli_classify_outputs_no_preservation() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "scp.cli", "classify", "Formatting change only to normalize whitespace."],
        capture_output=True,
        text=True,
        check=True,
        env=pythonpath_env(),
    )

    assert result.stdout.strip() == "no_preservation"


def test_scp_cli_generate_writes_valid_yaml() -> None:
    tmp_path = workspace_tmp_dir()
    output_path = tmp_path / "generated.yaml"

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "scp.cli",
                "generate",
                "--summary",
                "Continue using FastAPI instead of adding another package.",
                "--out",
                str(output_path),
            ],
            capture_output=True,
            text=True,
            check=True,
            env=pythonpath_env(),
        )

        assert output_path.exists()
        assert result.stdout.strip() == f"Generated {output_path.as_posix()}"

        validate = subprocess.run(
            [sys.executable, "-m", "scp.cli", "validate", str(output_path)],
            capture_output=True,
            text=True,
            check=True,
            env=pythonpath_env(),
        )
        assert validate.stdout.strip() == "Validated 1 file(s)."
    finally:
        cleanup_tmp_dir(tmp_path)


def test_scp_cli_init_creates_valid_origin_card() -> None:
    tmp_path = workspace_tmp_dir()
    output_path = tmp_path / ".scp" / "origin.yaml"
    answers = "\n".join(
        [
            "Preserve important project decisions from adoption forward.",
            "Humans and AI maintainers.",
            "Local-first and deterministic.",
            "Do not reconstruct old history.",
            "Future sessions reuse preserved decisions.",
            "Adopt SCP for the repository.",
        ]
    ) + "\n"

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "scp.cli",
                "init",
                "--out",
                str(output_path),
            ],
            capture_output=True,
            text=True,
            check=True,
            env=pythonpath_env(),
            input=answers,
        )

        assert output_path.exists()
        assert result.stdout.strip().endswith(output_path.as_posix())

        validate = subprocess.run(
            [sys.executable, "-m", "scp.cli", "validate", str(output_path)],
            capture_output=True,
            text=True,
            check=True,
            env=pythonpath_env(),
        )
        assert validate.stdout.strip() == "Validated 1 file(s)."
    finally:
        cleanup_tmp_dir(tmp_path)


def test_scp_cli_init_handles_empty_answers_deterministically() -> None:
    tmp_path = workspace_tmp_dir()
    output_path = tmp_path / ".scp" / "origin.yaml"
    answers = "\n\n\n\n\n\n"

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "scp.cli",
                "init",
                "--out",
                str(output_path),
            ],
            capture_output=True,
            text=True,
            check=True,
            env=pythonpath_env(),
            input=answers,
        )

        content = output_path.read_text(encoding="utf-8")
        assert "Unspecified at adoption." in content
    finally:
        cleanup_tmp_dir(tmp_path)
