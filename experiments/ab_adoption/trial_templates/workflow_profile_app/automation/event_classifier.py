from __future__ import annotations

from pathlib import PurePosixPath


DEPENDENCY_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "poetry.lock",
}

DOC_EXTENSIONS = {".md", ".rst", ".txt"}
CODE_EXTENSIONS = {
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
    ".sh",
    ".ps1",
    ".yml",
    ".yaml",
}

IMPORT_SURFACE_PATTERNS = (
    "import requests",
    "from subprocess import",
    "import subprocess",
    "import socket",
    "import boto3",
    "import openai",
    "import os",
)

DECISION_PHRASES = (
    "decided to",
    "rejected",
    "tradeoff",
    "migration",
    "architecture",
    "constraint",
    "security",
    "local-first",
)


def normalize_path(path: str) -> str:
    return str(PurePosixPath(path.replace("\\", "/")))


def is_dependency_path(path: str) -> bool:
    normalized = normalize_path(path)
    name = PurePosixPath(normalized).name
    return name in DEPENDENCY_FILES


def is_docs_path(path: str) -> bool:
    normalized = normalize_path(path)
    pure = PurePosixPath(normalized)
    if pure.suffix.lower() in DOC_EXTENSIONS:
        return True
    return normalized.startswith("docs/")


def is_architecture_path(path: str) -> bool:
    normalized = normalize_path(path)
    lowered = normalized.lower()
    return lowered.startswith("docs/decisions/") or "architecture" in lowered


def is_code_path(path: str) -> bool:
    normalized = normalize_path(path)
    pure = PurePosixPath(normalized)
    if is_docs_path(normalized) or is_dependency_path(normalized):
        return False
    if pure.suffix.lower() in CODE_EXTENSIONS:
        return True
    return normalized.startswith(("src/", "app/", "automation/", "tests/"))


def extract_added_lines(diff_text: str) -> list[str]:
    added_lines: list[str] = []
    for line in diff_text.splitlines():
        if line.startswith("+++") or not line.startswith("+"):
            continue
        added_lines.append(line[1:].strip())
    return added_lines


def detect_import_surface(diff_text: str) -> list[str]:
    matches: list[str] = []
    haystack = extract_added_lines(diff_text)
    if not haystack:
        haystack = diff_text.splitlines()
    for line in haystack:
        lowered = line.strip().lower()
        for pattern in IMPORT_SURFACE_PATTERNS:
            if pattern in lowered:
                matches.append(line.strip())
                break
    return matches


def detect_decision_phrases(diff_text: str) -> list[str]:
    lowered = diff_text.lower()
    return [phrase for phrase in DECISION_PHRASES if phrase in lowered]


def classify_event(changed_paths: list[str], diff_text: str = "") -> dict:
    normalized_paths = [normalize_path(path) for path in changed_paths]
    dependency_paths = [path for path in normalized_paths if is_dependency_path(path)]
    architecture_paths = [path for path in normalized_paths if is_architecture_path(path)]
    code_paths = [path for path in normalized_paths if is_code_path(path)]
    import_lines = detect_import_surface(diff_text)
    decision_phrases = detect_decision_phrases(diff_text)

    decision_worthy = bool(dependency_paths or architecture_paths or decision_phrases)
    docs_only = bool(normalized_paths) and all(is_docs_path(path) for path in normalized_paths)
    if docs_only and not decision_worthy:
        labels = ["docs_only_change"]
    else:
        labels: list[str] = []
        if code_paths or import_lines:
            labels.append("code_change")
        if dependency_paths:
            labels.append("dependency_change")
        if import_lines:
            labels.append("import_surface_change")
        if decision_worthy:
            labels.append("decision_worthy_change")
        if not labels:
            labels.append("code_change")

    return {
        "labels": labels,
        "changed_paths": normalized_paths,
        "signals": {
            "dependency_paths": dependency_paths,
            "architecture_paths": architecture_paths,
            "code_paths": code_paths,
            "import_lines": import_lines,
            "decision_phrases": decision_phrases,
        },
    }
