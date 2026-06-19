from __future__ import annotations

import json
from collections import Counter, defaultdict
from statistics import median
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ROOT_DIR / "results"
SUMMARY_PATH = ROOT_DIR / "results_summary.md"
SUBSCORE_KEYS = (
    "constraint_adherence",
    "dependency_discipline",
    "artifact_usage",
    "self_repair_behavior",
    "handoff_quality",
    "human_review_usefulness",
)
METRIC_KEYS = (
    "unnecessary_dependencies",
    "repeated_mistakes",
    "ignored_constraints",
    "repair_iterations",
    "artifact_reads",
    "artifact_writes",
)


def load_logs(results_dir: Path = RESULTS_DIR) -> list[dict]:
    if not results_dir.exists():
        return []
    logs: list[dict] = []
    for path in sorted(results_dir.glob("*.json")):
        if path.name.endswith(".timing.json"):
            continue
        with path.open("r", encoding="utf-8-sig") as handle:
            payload = json.load(handle)
            if "total_score" not in payload:
                continue
            logs.append(payload)
    return logs


def average(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 2)


def median_value(values: list[float]) -> float | None:
    if not values:
        return None
    return round(float(median(values)), 2)


def analyze_logs(logs: list[dict]) -> dict:
    counts = Counter()
    total_scores: dict[str, list[float]] = defaultdict(list)
    elapsed_times: dict[str, list[float]] = defaultdict(list)
    subscores: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    metrics: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    failures: dict[str, Counter] = defaultdict(Counter)
    fastest_runs: dict[str, dict | None] = defaultdict(lambda: None)
    slowest_runs: dict[str, dict | None] = defaultdict(lambda: None)

    for log in logs:
        condition = log.get("repo_condition", "unknown")
        counts[condition] += 1
        total_scores[condition].append(float(log.get("total_score", 0)))
        elapsed = log.get("elapsed_seconds")
        if elapsed is not None:
            elapsed_value = float(elapsed)
            elapsed_times[condition].append(elapsed_value)
            current_fastest = fastest_runs[condition]
            current_slowest = slowest_runs[condition]
            if current_fastest is None or elapsed_value < current_fastest["elapsed_seconds"]:
                fastest_runs[condition] = {
                    "run_id": log.get("run_id"),
                    "elapsed_seconds": round(elapsed_value, 2),
                }
            if current_slowest is None or elapsed_value > current_slowest["elapsed_seconds"]:
                slowest_runs[condition] = {
                    "run_id": log.get("run_id"),
                    "elapsed_seconds": round(elapsed_value, 2),
                }
        for key in SUBSCORE_KEYS:
            value = log.get("subscores", {}).get(key)
            if value is not None:
                subscores[condition][key].append(float(value))
        for key in METRIC_KEYS:
            value = log.get("metrics", {}).get(key)
            if value is not None:
                metrics[condition][key].append(float(value))
        for failure in log.get("failures", []):
            failures[condition][failure] += 1

    average_total = {condition: average(values) for condition, values in total_scores.items()}
    average_elapsed = {condition: average(values) for condition, values in elapsed_times.items()}
    median_elapsed = {condition: median_value(values) for condition, values in elapsed_times.items()}
    average_subscores = {
        condition: {key: average(values) for key, values in score_map.items()}
        for condition, score_map in subscores.items()
    }
    average_metrics = {
        condition: {key: average(values) for key, values in metric_map.items()}
        for condition, metric_map in metrics.items()
    }
    common_failures = {
        condition: counter.most_common(5)
        for condition, counter in failures.items()
    }

    return {
        "counts": dict(counts),
        "average_total_score": average_total,
        "average_elapsed_seconds": average_elapsed,
        "median_elapsed_seconds": median_elapsed,
        "average_subscores": average_subscores,
        "average_metrics": average_metrics,
        "fastest_runs": dict(fastest_runs),
        "slowest_runs": dict(slowest_runs),
        "common_failures": common_failures,
    }


def markdown_report(analysis: dict, logs: list[dict]) -> str:
    conditions = ("baseline", "workflow")

    def format_value(mapping: dict, condition: str, fallback: str = "-") -> str:
        value = mapping.get(condition)
        if value is None:
            return fallback
        return str(value)

    if not logs:
        return "\n".join(
            [
                "# A/B Adoption Results",
                "",
                "No result logs were found.",
                "",
                "Add JSON files under `experiments/ab_adoption/results/` and rerun `python experiments/ab_adoption/analyze_results.py`.",
                "",
                "Metric| Baseline| Workflow",
                "---|---|---",
                "Runs| -| -",
                "Avg Score| -| -",
                "Avg Time (s)| -| -",
                "Median Time (s)| -| -",
                "Avg Constraint Score| -| -",
                "Avg Dependency Score| -| -",
                "Avg Artifact Usage| -| -",
                "Avg Self Repair| -| -",
                "",
            ]
        )

    lines = [
        "# A/B Adoption Results",
        "",
        "## Compact Comparison",
        "",
        "Metric| Baseline| Workflow",
        "---|---|---",
        f"Runs| {format_value(analysis['counts'], 'baseline')}| {format_value(analysis['counts'], 'workflow')}",
        f"Avg Score| {format_value(analysis['average_total_score'], 'baseline')}| {format_value(analysis['average_total_score'], 'workflow')}",
        f"Avg Time (s)| {format_value(analysis['average_elapsed_seconds'], 'baseline')}| {format_value(analysis['average_elapsed_seconds'], 'workflow')}",
        f"Median Time (s)| {format_value(analysis['median_elapsed_seconds'], 'baseline')}| {format_value(analysis['median_elapsed_seconds'], 'workflow')}",
        f"Avg Constraint Score| {format_value(analysis['average_subscores'].get('baseline', {}), 'constraint_adherence')}| {format_value(analysis['average_subscores'].get('workflow', {}), 'constraint_adherence')}",
        f"Avg Dependency Score| {format_value(analysis['average_subscores'].get('baseline', {}), 'dependency_discipline')}| {format_value(analysis['average_subscores'].get('workflow', {}), 'dependency_discipline')}",
        f"Avg Artifact Usage| {format_value(analysis['average_subscores'].get('baseline', {}), 'artifact_usage')}| {format_value(analysis['average_subscores'].get('workflow', {}), 'artifact_usage')}",
        f"Avg Self Repair| {format_value(analysis['average_subscores'].get('baseline', {}), 'self_repair_behavior')}| {format_value(analysis['average_subscores'].get('workflow', {}), 'self_repair_behavior')}",
        "",
        "## Count By Condition",
        "",
    ]
    for condition, count in sorted(analysis["counts"].items()):
        lines.append(f"- `{condition}`: {count}")

    lines.extend(["", "## Average Total Score By Condition", ""])
    for condition, value in sorted(analysis["average_total_score"].items()):
        lines.append(f"- `{condition}`: {value}")

    lines.extend(["", "## Timing By Condition", ""])
    for condition in conditions:
        avg_time = analysis["average_elapsed_seconds"].get(condition)
        med_time = analysis["median_elapsed_seconds"].get(condition)
        fastest = analysis["fastest_runs"].get(condition)
        slowest = analysis["slowest_runs"].get(condition)
        lines.append(f"- `{condition}` average elapsed seconds: {avg_time if avg_time is not None else 'insufficient data'}")
        lines.append(f"- `{condition}` median elapsed seconds: {med_time if med_time is not None else 'insufficient data'}")
        if fastest:
            lines.append(f"- `{condition}` fastest run: {fastest['run_id']} ({fastest['elapsed_seconds']}s)")
        else:
            lines.append(f"- `{condition}` fastest run: insufficient data")
        if slowest:
            lines.append(f"- `{condition}` slowest run: {slowest['run_id']} ({slowest['elapsed_seconds']}s)")
        else:
            lines.append(f"- `{condition}` slowest run: insufficient data")

    lines.extend(["", "## Average Subscores By Condition", ""])
    for condition, score_map in sorted(analysis["average_subscores"].items()):
        lines.append(f"- `{condition}`:")
        for key in SUBSCORE_KEYS:
            if key in score_map:
                lines.append(f"  - {key}: {score_map[key]}")

    lines.extend(["", "## Average Reliability Metrics By Condition", ""])
    for condition in conditions:
        metric_map = analysis["average_metrics"].get(condition, {})
        lines.append(f"- `{condition}`:")
        if metric_map:
            for key in METRIC_KEYS:
                if key in metric_map:
                    lines.append(f"  - {key}: {metric_map[key]}")
        else:
            lines.append("  - insufficient data")

    lines.extend(["", "## Common Failures", ""])
    for condition in conditions:
        failures = analysis["common_failures"].get(condition, [])
        lines.append(f"- `{condition}`:")
        if failures:
            for failure, count in failures:
                lines.append(f"  - {failure}: {count}")
        else:
            lines.append("  - none recorded")

    lines.append("")
    return "\n".join(lines)


def write_summary(text: str, summary_path: Path = SUMMARY_PATH) -> Path:
    summary_path.write_text(text, encoding="utf-8", newline="\n")
    return summary_path


def main() -> int:
    logs = load_logs()
    analysis = analyze_logs(logs)
    report = markdown_report(analysis, logs)
    path = write_summary(report)
    print(path.as_posix())
    if not logs:
        print("No result logs found. Add JSON files under experiments/ab_adoption/results/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
