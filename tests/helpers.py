from __future__ import annotations

from pathlib import Path
import shutil
import os
import uuid


def workspace_tmp_dir() -> Path:
    base = Path("_runtime_tmp")
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"tmp_{uuid.uuid4().hex}"
    path.mkdir(parents=True, exist_ok=False)
    return path


def cleanup_tmp_dir(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


def pythonpath_env() -> dict[str, str]:
    env = os.environ.copy()
    src_path = str(Path("src").resolve())
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = src_path if not existing else f"{src_path}{os.pathsep}{existing}"
    return env
