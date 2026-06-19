from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from automation.event_classifier import classify_event
from automation.intent_bootstrap import write_intent_draft
from automation.scp_draft import write_scp_draft


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_diff_text(diff_file: str | None) -> str:
    if not diff_file:
        return ""
    return Path(diff_file).read_text(encoding="utf-8")


def tool_status(command: list[str]) -> dict:
    executable = command[0]
    resolved = shutil.which(executable)
    if not resolved:
        return {
            "status": "skipped",
            "reason": "not installed",
            "command": " ".join(command),
            "returncode": None,
            "stdout": "",
            "stderr": "",
        }

    completed = subprocess.run(
        command,
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "status": "passed" if completed.returncode == 0 else "failed",
        "reason": "completed" if completed.returncode == 0 else "tool returned nonzero exit status",
        "command": " ".join(command),
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def build_summary(changed_paths: list[str], diff_text: str, classification: dict) -> dict:
    labels = classification["labels"]
    should_run_ia = "code_change" in labels
    should_run_ds2 = "dependency_change" in labels or "import_surface_change" in labels
    should_draft_scp = "decision_worthy_change" in labels

    ia_result = {"status": "not_needed", "reason": "no code change detected"}
    if should_run_ia:
        intent_path = ROOT_DIR / "intent.yaml"
        if not intent_path.exists():
            bootstrap = write_intent_draft(changed_files=classification["changed_paths"], root_dir=ROOT_DIR)
            ia_result = {
                "status": "blocked_until_intent_approved",
                "reason": "intent.yaml missing but IA verification was requested",
                "command": "ia check",
                "returncode": None,
                "stdout": "",
                "stderr": "",
                "intent_draft_yaml": bootstrap["yaml_path"],
                "intent_draft_markdown": bootstrap["markdown_path"],
            }
        else:
            ia_result = tool_status(["ia", "check"])

    ds2_result = {"status": "not_needed", "reason": "no dependency or import surface change detected"}
    if should_run_ds2:
        ds2_result = tool_status(["ds2", "scan", "."])

    scp_result = {
        "status": "not_needed",
        "reason": "no decision-worthy signal detected",
        "draft_path": None,
    }
    if should_draft_scp:
        draft_path = write_scp_draft(
            changed_paths=classification["changed_paths"],
            classification=classification,
            diff_text=diff_text,
            output_dir=ROOT_DIR / "artifacts" / "knowledge" / "scp_drafts",
        )
        scp_result = {
            "status": "drafted",
            "reason": "decision-worthy signal detected",
            "draft_path": str(draft_path.as_posix()),
        }

    return {
        "timestamp": utc_timestamp(),
        "changed_paths": changed_paths,
        "classification": classification,
        "checks": {
            "ia": ia_result,
            "ds2": ds2_result,
            "scp_draft": scp_result,
        },
    }


def write_outputs(summary: dict) -> tuple[Path, Path]:
    output_dir = ROOT_DIR / "artifacts" / "knowledge"
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "guardrail_summary.json"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8", newline="\n")

    labels = ", ".join(summary["classification"]["labels"])
    changed_files = summary["classification"]["changed_paths"]
    checks = summary["checks"]
    markdown_lines = [
        "# Guardrail Summary",
        "",
        f"- Timestamp: {summary['timestamp']}",
        f"- Event labels: {labels}",
        "",
        "## Changed files",
        "",
        *[f"- `{path}`" for path in changed_files],
        "",
        "## Check status",
        "",
        f"- IA: {checks['ia']['status']} ({checks['ia']['reason']})",
        f"- DS2: {checks['ds2']['status']} ({checks['ds2']['reason']})",
        f"- SCP draft: {checks['scp_draft']['status']} ({checks['scp_draft']['reason']})",
        "",
        "## Plain-English summary",
        "",
        "This summary records which guardrails were relevant for the detected change and whether they ran or were skipped.",
    ]
    if checks["scp_draft"].get("draft_path"):
        markdown_lines.extend(
            [
                "",
                "## SCP draft",
                "",
                f"- Draft path: `{checks['scp_draft']['draft_path']}`",
            ]
        )
    if checks["ia"]["status"] == "blocked_until_intent_approved":
        markdown_lines.extend(
            [
                "",
                "## Intent bootstrap created",
                "",
                "- IA was not run because `intent.yaml` is missing.",
                f"- Review `{checks['ia']['intent_draft_yaml']}` and `{checks['ia']['intent_draft_markdown']}`.",
                "- Promote the approved draft to `intent.yaml` before expecting IA verification to run.",
            ]
        )

    markdown_path = output_dir / "guardrail_summary.md"
    markdown_path.write_text("\n".join(markdown_lines) + "\n", encoding="utf-8", newline="\n")

    return json_path, markdown_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run thin IA + DS2 + SCP guardrails.")
    parser.add_argument("--changed", nargs="+", required=True, help="Changed file paths.")
    parser.add_argument("--diff-file", help="Optional path to a diff file.", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    diff_text = load_diff_text(args.diff_file)
    classification = classify_event(args.changed, diff_text=diff_text)
    summary = build_summary(changed_paths=args.changed, diff_text=diff_text, classification=classification)
    json_path, markdown_path = write_outputs(summary)
    print(f"Wrote {json_path.as_posix()}")
    print(f"Wrote {markdown_path.as_posix()}")
    if summary["checks"]["scp_draft"].get("draft_path"):
        print(f"Wrote {summary['checks']['scp_draft']['draft_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
