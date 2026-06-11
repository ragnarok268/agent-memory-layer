"""AST-based Python import scanner."""

from __future__ import annotations

import ast
from pathlib import Path

from ds2.graph.model import WarningRecord

IMPORT_TO_PACKAGE = {
    "yaml": "PyYAML",
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
    "PIL": "Pillow",
    "bs4": "beautifulsoup4",
}

STDLIB_ALLOWLIST = {
    "__future__",
    "abc",
    "argparse",
    "ast",
    "asyncio",
    "collections",
    "contextlib",
    "csv",
    "dataclasses",
    "datetime",
    "functools",
    "hashlib",
    "importlib",
    "io",
    "json",
    "logging",
    "math",
    "os",
    "pathlib",
    "re",
    "sqlite3",
    "subprocess",
    "sys",
    "tempfile",
    "textwrap",
    "threading",
    "time",
    "tomllib",
    "typing",
    "unittest",
    "uuid",
}


def normalize_import_to_package(import_name: str) -> str:
    base = import_name.split(".", 1)[0]
    return IMPORT_TO_PACKAGE.get(base, base)


def _is_local_module(project_path: Path, module_name: str) -> bool:
    candidate = module_name.replace(".", "/")
    return (project_path / f"{candidate}.py").exists() or (project_path / candidate / "__init__.py").exists()


def scan_imports(project_path: Path) -> tuple[dict[str, list[str]], list[WarningRecord]]:
    observed: dict[str, set[str]] = {}
    warnings: list[WarningRecord] = []

    for file_path in sorted(project_path.rglob("*.py")):
        if any(part.startswith(".") for part in file_path.parts):
            continue
        try:
            tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
        except Exception as exc:
            warnings.append(WarningRecord(source="imports", message=f"Failed to parse {file_path.name}: {exc}"))
            continue

        for node in tree.body:
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if not node.module or node.level != 0:
                    continue
                names = [node.module]
            else:
                continue

            for name in names:
                base = name.split(".", 1)[0]
                if base in STDLIB_ALLOWLIST or _is_local_module(project_path, base):
                    continue
                package_name = normalize_import_to_package(name)
                observed.setdefault(package_name, set()).add(base)

    return {name: sorted(import_names) for name, import_names in sorted(observed.items())}, warnings
