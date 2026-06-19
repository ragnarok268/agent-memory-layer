from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".kt",
    ".go",
    ".rs",
    ".rb",
    ".php",
}

CONSTRAINT_PATTERNS = {
    "local-first": "local_first_required",
    "no telemetry": "no_telemetry",
    "no secrets": "no_secrets",
    "human-readable": "human_readable_artifacts",
    "machine-readable": "machine_readable_artifacts",
    "do not claim standard": "do_not_claim_industry_standard",
    "industry standard": "do_not_claim_industry_standard",
}


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def candidate_text_files(root_dir: Path) -> list[Path]:
    candidates: list[Path] = []
    for relative in ("README.md", "AGENTS.md"):
        candidate = root_dir / relative
        if candidate.exists():
            candidates.append(candidate)
    docs_dir = root_dir / "docs"
    if docs_dir.exists():
        candidates.extend(sorted(docs_dir.rglob("*.md")))
    return candidates


def infer_project_type(root_dir: Path, changed_files: list[str]) -> str:
    normalized = [path.replace("\\", "/") for path in changed_files]
    if (root_dir / "pyproject.toml").exists() or (root_dir / "requirements.txt").exists():
        return "python_project"
    if (root_dir / "package.json").exists():
        return "node_or_javascript_project"

    markdown_paths = 0
    source_paths = 0
    for path in normalized:
        suffix = Path(path).suffix.lower()
        if suffix == ".md":
            markdown_paths += 1
        if suffix in SOURCE_EXTENSIONS or path.startswith(("src/", "app/", "automation/", "tests/")):
            source_paths += 1

    if markdown_paths >= max(1, len(normalized)) and source_paths == 0:
        return "documentation_project"
    return "unknown"


def infer_constraints(root_dir: Path) -> list[str]:
    found: list[str] = []
    for path in candidate_text_files(root_dir):
        try:
            text = path.read_text(encoding="utf-8").lower()
        except OSError:
            continue
        for phrase, constraint in CONSTRAINT_PATTERNS.items():
            if phrase in text and constraint not in found:
                found.append(constraint)
    return found


def suggested_intent_for(project_type: str) -> str:
    if project_type == "documentation_project":
        return (
            "Preserve and explain the AI-native engineering knowledge workflow "
            "using clear, local-first, human-readable and machine-readable artifacts."
        )
    if project_type == "python_project":
        return (
            "Maintain project behavior while avoiding unintended network, telemetry, shell, "
            "or destructive file-system behavior unless explicitly approved."
        )
    return (
        "Maintain the requested behavior while avoiding unintended side effects and "
        "preserving reviewable artifacts."
    )


def build_intent_draft(root_dir: Path, changed_files: list[str], timestamp: str | None = None) -> dict:
    generated_at = timestamp or utc_timestamp()
    project_type = infer_project_type(root_dir, changed_files)
    constraints = infer_constraints(root_dir)
    return {
        "status": "needs_human_review",
        "source": "automation_intent_bootstrap",
        "generated_at": generated_at,
        "reason": "intent.yaml missing but IA verification was requested",
        "changed_files": [path.replace("\\", "/") for path in changed_files],
        "inferred_project_type": project_type,
        "inferred_constraints": constraints,
        "suggested_intent": suggested_intent_for(project_type),
        "review_checklist": [
            "Does this intent match the actual project?",
            "Are any required capabilities missing?",
            "Are any constraints too strict?",
            "Should network, shell, telemetry, or file-system access be explicitly allowed?",
            "Should this draft be promoted to intent.yaml?",
        ],
    }


def yaml_lines_from_draft(draft: dict) -> list[str]:
    lines = [
        f'status: "{draft["status"]}"',
        f'source: "{draft["source"]}"',
        f'generated_at: "{draft["generated_at"]}"',
        f'reason: "{draft["reason"]}"',
        "changed_files:",
    ]
    lines.extend([f'  - "{path}"' for path in draft["changed_files"]])
    lines.append(f'inferred_project_type: "{draft["inferred_project_type"]}"')
    lines.append("inferred_constraints:")
    if draft["inferred_constraints"]:
        lines.extend([f'  - "{item}"' for item in draft["inferred_constraints"]])
    else:
        lines.append('  - "none_detected"')
    lines.extend(
        [
            "suggested_intent: |",
            f'  {draft["suggested_intent"]}',
            "review_checklist:",
        ]
    )
    lines.extend([f'  - "{item}"' for item in draft["review_checklist"]])
    return lines


def markdown_lines_from_draft(draft: dict) -> list[str]:
    constraint_lines = [f'- `{item}`' for item in draft["inferred_constraints"]]
    if not constraint_lines:
        constraint_lines = ["- `none_detected`"]
    return [
        "# Intent Draft",
        "",
        "> Draft only. This intent needs human review before it becomes intent.yaml.",
        "",
        f'- Status: `{draft["status"]}`',
        f'- Source: `{draft["source"]}`',
        f'- Generated at: `{draft["generated_at"]}`',
        f'- Reason: {draft["reason"]}',
        f'- Inferred project type: `{draft["inferred_project_type"]}`',
        "",
        "## Changed files",
        "",
        *[f'- `{path}`' for path in draft["changed_files"]],
        "",
        "## Inferred constraints",
        "",
        *constraint_lines,
        "",
        "## Suggested intent",
        "",
        draft["suggested_intent"],
        "",
        "## Review checklist",
        "",
        *[f"- {item}" for item in draft["review_checklist"]],
        "",
    ]


def write_intent_draft(
    changed_files: list[str],
    root_dir: Path | str | None = None,
    timestamp: str | None = None,
) -> dict:
    base_dir = Path(root_dir) if root_dir is not None else ROOT_DIR
    output_dir = base_dir / "artifacts" / "knowledge"
    output_dir.mkdir(parents=True, exist_ok=True)

    draft = build_intent_draft(base_dir, changed_files, timestamp=timestamp)
    yaml_path = output_dir / "intent_draft.yaml"
    markdown_path = output_dir / "intent_draft.md"
    yaml_path.write_text("\n".join(yaml_lines_from_draft(draft)) + "\n", encoding="utf-8", newline="\n")
    markdown_path.write_text(
        "\n".join(markdown_lines_from_draft(draft)),
        encoding="utf-8",
        newline="\n",
    )
    return {
        "draft": draft,
        "yaml_path": str(yaml_path.as_posix()),
        "markdown_path": str(markdown_path.as_posix()),
    }
