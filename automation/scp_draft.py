from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def draft_slug(timestamp: str, decision_type: str) -> str:
    compact = timestamp.replace("-", "").replace(":", "").replace("T", "-").replace("Z", "")
    normalized_type = decision_type.replace("_", "-")
    return f"{compact}-{normalized_type}.md"


def infer_decision_type(labels: list[str], signals: dict) -> str:
    if "dependency_change" in labels:
        return "dependency_decision"
    phrases = set(signals.get("decision_phrases", []))
    architecture_paths = signals.get("architecture_paths", [])
    if architecture_paths or "architecture" in phrases or "migration" in phrases:
        return "architecture_decision"
    if {"constraint", "security", "local-first"} & phrases:
        return "constraint_change"
    return "major_implementation_decision"


def build_draft_markdown(
    changed_paths: list[str],
    classification: dict,
    diff_text: str = "",
    timestamp: str | None = None,
) -> tuple[str, str]:
    used_timestamp = timestamp or utc_timestamp()
    labels = classification.get("labels", [])
    signals = classification.get("signals", {})
    decision_type = infer_decision_type(labels, signals)
    title = f"Draft SCP memory for {decision_type}"

    snippet_lines = []
    if diff_text:
        for line in diff_text.splitlines():
            stripped = line.strip()
            if stripped:
                snippet_lines.append(stripped)
            if len(snippet_lines) == 5:
                break
    evidence_snippet = "\n".join(snippet_lines) if snippet_lines else "No diff snippet provided."

    markdown = "\n".join(
        [
            f"# {title}",
            "",
            "> Draft only. This is not approved project memory.",
            "",
            f"- Timestamp: {used_timestamp}",
            f"- Suspected decision type: `{decision_type}`",
            f"- Trigger signals: {', '.join(labels) if labels else 'none'}",
            "",
            "## Changed files",
            "",
            *[f"- `{path}`" for path in changed_paths],
            "",
            "## Evidence snippet",
            "",
            "```text",
            evidence_snippet,
            "```",
            "",
            "## Human review checklist",
            "",
            "- Confirm whether the change is actually preservation-worthy.",
            "- Confirm or correct the suspected decision type.",
            "- Add rationale, constraints, impact, and revisit conditions if the draft should become real memory.",
            "- Do not treat this draft as approved SCP history without review.",
            "",
        ]
    )

    return decision_type, markdown


def write_scp_draft(
    changed_paths: list[str],
    classification: dict,
    diff_text: str = "",
    output_dir: str | Path = "artifacts/knowledge/scp_drafts",
    timestamp: str | None = None,
) -> Path:
    used_timestamp = timestamp or utc_timestamp()
    decision_type, markdown = build_draft_markdown(
        changed_paths=changed_paths,
        classification=classification,
        diff_text=diff_text,
        timestamp=used_timestamp,
    )
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    target = output_path / draft_slug(used_timestamp, decision_type)
    target.write_text(markdown, encoding="utf-8", newline="\n")
    return target
