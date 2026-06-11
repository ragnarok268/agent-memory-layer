"""Stable JSON helpers."""

from __future__ import annotations

import json
from hashlib import sha256
from typing import Any


def dumps_stable(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()
