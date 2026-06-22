# Completion-Adjusted Benchmark Results

This adjusted view preserves the raw initial execution separately and substitutes rerun evidence only for AML runs classified as infrastructure interruptions.

| Metric | Baseline | AML |
| --- | ---: | ---: |
| Completed runs | 12/12 | 11/12 |
| Tasks Passed | 12 | 11 |
| Intent Violations | 3 | 0 |
| Constraint Violations | 3 | 0 |
| Architecture Regressions | 1 | 0 |
| Unnecessary Dependencies | 0 | 0 |
| Risky Capabilities | 1 | 0 |
| Repair Attempts | 4 | 6 |
| Average Files Changed | 2.50 | 2.92 |
| Average Lines Changed | 45.42 | 58.83 |
| Prior Decision Preserved | 75.0% (3/4) | 100.0% (3/3) |
| Memory Artifact Consulted | 0.0% (0/12) | 100.0% (11/11) |
| Rediscovery Required | not measured | not measured |

Raw initial results remain in `results/results.json` and `results/results_table.md`.
