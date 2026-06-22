# Benchmark Results


## Persistent Memory Summary

| Metric | Baseline | AML | Improvement |
| --- | ---: | ---: | ---: |
| Tasks Passed | 12 | 11 | -1 |
| Intent Violations | 3 | 0 | 3 |
| Constraint Violations | 3 | 0 | 3 |
| Architecture Regressions | 1 | 0 | 1 |
| Unnecessary Dependencies | 0 | 0 | 0 |
| Memory Failures | 1 | 0 | 1 |
| Rediscovery Events | not measured | not measured | not measured |
| Repair Attempts | 4 | 4 | 0 |

## Full Metric Detail

| Metric | Baseline | AML |
| --- | ---: | ---: |
| Runs | 12 | 12 |
| Tests passed | 12 | 11 |
| Intent violations | 3 | 0 |
| Unnecessary dependencies added | 0 | 0 |
| Risky capabilities added | 1 | 0 |
| Constraint violations | 3 | 0 |
| Average files changed | 2.50 | 2.58 |
| Average lines changed | 45.42 | 53.08 |
| Repair attempts | 4 | 4 |
| Prior decision preserved | 75.0% (3/4) | 100.0% (2/2) |
| Rediscovery required | not measured | not measured |
| Architecture regression | 1 | 0 |
| Memory artifact consulted | 0.0% (0/12) | 100.0% (9/9) |
| Memory artifact updated correctly | not measured | not measured |

Results are descriptive only. They do not prove general model improvement.
