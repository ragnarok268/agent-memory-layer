from __future__ import annotations


def format_profile(name: str, role: str) -> str:
    clean_name = name.strip()
    clean_role = role.strip()
    return f"{clean_name} - {clean_role}"
