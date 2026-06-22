from __future__ import annotations

import json
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
RESULTS = ROOT / "results"
METRICS = [
    ("tests_passed", "Tests passed", "sum"),
    ("intent_violations", "Intent violations", "sum"),
    ("unnecessary_dependencies_added", "Unnecessary dependencies added", "sum"),
    ("risky_capabilities_added", "Risky capabilities added", "sum"),
    ("constraint_violations", "Constraint violations", "sum"),
    ("files_changed", "Average files changed", "average"),
    ("lines_changed", "Average lines changed", "average"),
    ("repair_attempts", "Repair attempts", "sum"),
    ("prior_decision_preserved", "Prior decision preserved", "percent_true"),
    ("rediscovery_required", "Rediscovery required", "percent_true"),
    ("architecture_regression", "Architecture regression", "sum"),
    ("memory_artifact_consulted", "Memory artifact consulted", "percent_true"),
    ("memory_artifact_updated_correctly", "Memory artifact updated correctly", "percent_true"),
]
SUMMARY_ROWS = [
    ("tests_passed", "Tasks Passed", "higher"),
    ("intent_violations", "Intent Violations", "lower"),
    ("constraint_violations", "Constraint Violations", "lower"),
    ("architecture_regression", "Architecture Regressions", "lower"),
    ("unnecessary_dependencies_added", "Unnecessary Dependencies", "lower"),
    ("memory_failures", "Memory Failures", "lower"),
    ("rediscovery_required", "Rediscovery Events", "lower"),
    ("repair_attempts", "Repair Attempts", "lower"),
]


def load_receipts() -> list[dict]:
    receipts = []
    for path in sorted(RUNS.glob("*/scoring_receipt.json")):
        receipt = json.loads(path.read_text(encoding="utf-8-sig"))
        receipts.append(receipt)
    return receipts


def values_for(receipts: list[dict], condition: str, key: str) -> list[float]:
    values = []
    for receipt in receipts:
        if receipt.get("condition") != condition:
            continue
        value = receipt.get(key)
        if isinstance(value, bool):
            values.append(1.0 if value else 0.0)
        elif isinstance(value, (int, float)):
            values.append(float(value))
    return values


def aggregate(values: list[float], method: str) -> str:
    if not values:
        return "not measured"
    if method == "sum":
        total = sum(values)
        return str(int(total)) if total.is_integer() else f"{total:.2f}"
    if method == "percent_true":
        return f"{(sum(values) / len(values)) * 100:.1f}% ({int(sum(values))}/{len(values)})"
    average = mean(values)
    return f"{average:.2f}"


def numeric_total(receipts: list[dict], condition: str, key: str) -> float | None:
    values = values_for(receipts, condition, key)
    if not values:
        return None
    return sum(values)


def memory_failures(receipts: list[dict], condition: str) -> float | None:
    values = []
    for receipt in receipts:
        if receipt.get("condition") != condition:
            continue
        value = receipt.get("prior_decision_preserved")
        if isinstance(value, bool):
            values.append(0.0 if value else 1.0)
    if not values:
        return None
    return sum(values)


def format_number(value: float | None) -> str:
    if value is None:
        return "not measured"
    return str(int(value)) if float(value).is_integer() else f"{value:.2f}"


def improvement(receipts: list[dict], key: str, direction: str) -> str:
    if key == "memory_failures":
        baseline = memory_failures(receipts, "baseline")
        aml = memory_failures(receipts, "aml")
    else:
        baseline = numeric_total(receipts, "baseline", key)
        aml = numeric_total(receipts, "aml", key)
    if baseline is None or aml is None:
        return "not measured"
    delta = (aml - baseline) if direction == "higher" else (baseline - aml)
    return format_number(delta)


def build_summary(receipts: list[dict]) -> dict:
    conditions = {}
    for condition in ("baseline", "aml"):
        condition_receipts = [receipt for receipt in receipts if receipt.get("condition") == condition]
        conditions[condition] = {
            "runs": len(condition_receipts),
            "metrics": {
                key: aggregate(values_for(receipts, condition, key), method)
                for key, _, method in METRICS
            },
            "memory_failures": format_number(memory_failures(receipts, condition)),
        }
    return {
        "runs_found": len(receipts),
        "conditions": conditions,
    }


def build_table(summary: dict, receipts: list[dict]) -> str:
    lines = ["# Benchmark Results", ""]
    if summary["runs_found"] == 0:
        lines.append("No scoring receipts have been collected yet.")
    lines.append("")
    lines.append("## Persistent Memory Summary")
    lines.append("")
    lines.append("| Metric | Baseline | AML | Improvement |")
    lines.append("| --- | ---: | ---: | ---: |")
    for key, label, direction in SUMMARY_ROWS:
        if key == "memory_failures":
            baseline = format_number(memory_failures(receipts, "baseline"))
            aml = format_number(memory_failures(receipts, "aml"))
        else:
            baseline = format_number(numeric_total(receipts, "baseline", key))
            aml = format_number(numeric_total(receipts, "aml", key))
        lines.append(f"| {label} | {baseline} | {aml} | {improvement(receipts, key, direction)} |")
    lines.append("")
    lines.append("## Full Metric Detail")
    lines.append("")
    lines.append("| Metric | Baseline | AML |")
    lines.append("| --- | ---: | ---: |")
    lines.append(f"| Runs | {summary['conditions'].get('baseline', {}).get('runs', 0)} | {summary['conditions'].get('aml', {}).get('runs', 0)} |")
    for key, label, _ in METRICS:
        baseline = summary["conditions"].get("baseline", {}).get("metrics", {}).get(key, "-")
        aml = summary["conditions"].get("aml", {}).get("metrics", {}).get(key, "-")
        lines.append(f"| {label} | {baseline} | {aml} |")
    lines.append("")
    lines.append("Results are descriptive only. They do not prove general model improvement.")
    lines.append("")
    return "\n".join(lines)


def describe_detected_behavior(task_id: str, receipt: dict) -> str:
    if task_id in {"task3", "memory_challenge_a"} and receipt.get("architecture_regression"):
        return "Detected database or SQLite-style persistence despite the file-based decision."
    if task_id == "memory_challenge_b" and receipt.get("architecture_regression"):
        return "Detected random or UUID-style identifiers despite the deterministic ID decision."
    if task_id in {"task8", "memory_challenge_c"} and receipt.get("architecture_regression"):
        return "Detected shell execution behavior despite the rejected shell-capability decision."
    if task_id in {"task4", "memory_challenge_d"} and receipt.get("architecture_regression"):
        return "Detected a second or incompatible feature-flag mechanism."
    if receipt.get("prior_decision_preserved") is True:
        return "Preserved the relevant prior decision according to the scoring receipt."
    return "No concrete memory-specific behavior was automatically summarized."


def build_case_studies(receipts: list[dict]) -> str:
    lines = ["# Qualitative Case Studies", ""]
    if not receipts:
        lines.append("No scoring receipts have been collected yet, so no case studies were generated.")
        lines.append("")
        return "\n".join(lines)
    by_task: dict[str, dict[str, dict]] = {}
    for receipt in receipts:
        by_task.setdefault(receipt.get("task_id", "unknown"), {})[receipt.get("condition", "unknown")] = receipt
    for task_id, pair in sorted(by_task.items()):
        baseline = pair.get("baseline")
        aml = pair.get("aml")
        if not baseline or not aml:
            continue
        baseline_failed_memory = baseline.get("architecture_regression") or baseline.get("rediscovery_required")
        aml_preserved = aml.get("prior_decision_preserved") is True and aml.get("architecture_regression") is False
        if not (baseline_failed_memory or aml_preserved):
            continue
        lines.append(f"## {task_id}")
        lines.append("")
        lines.append("Baseline:")
        lines.append(f"- {describe_detected_behavior(task_id, baseline)}")
        lines.append(f"- Intent violations: {baseline.get('intent_violations')}")
        lines.append(f"- Architecture regression: {baseline.get('architecture_regression')}")
        lines.append(f"- Rediscovery required: {baseline.get('rediscovery_required')}")
        lines.append("")
        lines.append("AML:")
        lines.append(f"- {describe_detected_behavior(task_id, aml)}")
        lines.append(f"- Prior decision preserved: {aml.get('prior_decision_preserved')}")
        lines.append(f"- Memory artifact consulted: {aml.get('memory_artifact_consulted')}")
        lines.append(f"- Architecture regression: {aml.get('architecture_regression')}")
        lines.append("")
        lines.append("Outcome:")
        if aml_preserved and baseline_failed_memory:
            lines.append("- Prior architectural knowledge was reused in the AML condition.")
        elif aml_preserved and baseline.get("prior_decision_preserved") is True:
            lines.append("- Both conditions preserved the relevant decision; no material AML-only benefit is shown by this pair.")
        elif aml_preserved:
            lines.append("- AML preserved the relevant decision, but the paired baseline evidence does not show a clear failure.")
        else:
            lines.append("- The paired evidence did not show successful memory reuse.")
        lines.append("")
    if len(lines) == 2:
        lines.append("No paired receipts contained enough evidence for an automatic case study.")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    receipts = load_receipts()
    summary = build_summary(receipts)
    (RESULTS / "results.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    (RESULTS / "results_table.md").write_text(build_table(summary, receipts), encoding="utf-8", newline="\n")
    (RESULTS / "case_studies.md").write_text(build_case_studies(receipts), encoding="utf-8", newline="\n")
    print(f"aggregated {len(receipts)} scoring receipt(s)")
    print(f"wrote {RESULTS / 'results_table.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
