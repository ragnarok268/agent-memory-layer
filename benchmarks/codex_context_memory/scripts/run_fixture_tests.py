from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = [
    ROOT / "fixtures" / "baseline_repo",
    ROOT / "fixtures" / "aml_repo",
]


def run_fixture(fixture: Path) -> int:
    print(f"running fixture tests: {fixture.relative_to(ROOT)}")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover"],
        cwd=fixture,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode


def main() -> int:
    failures = 0
    for fixture in FIXTURES:
        failures += 1 if run_fixture(fixture) else 0
    if failures:
        print(f"{failures} fixture test run(s) failed")
        return 1
    print("all fixture tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
