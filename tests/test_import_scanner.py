from ds2.collectors.imports import scan_imports
from tests.helpers import cleanup_tmp_dir, workspace_tmp_dir


def test_import_scanner_collects_top_level_imports_only() -> None:
    tmp_path = workspace_tmp_dir()
    try:
        (tmp_path / "app.py").write_text(
            """
import fastapi
from sqlalchemy import create_engine

def nested():
    import httpx
    return httpx
""".strip()
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

        imports, warnings = scan_imports(tmp_path)

        assert warnings == []
        assert imports == {"fastapi": ["fastapi"], "sqlalchemy": ["sqlalchemy"]}
    finally:
        cleanup_tmp_dir(tmp_path)


def test_import_scanner_maps_common_import_names() -> None:
    tmp_path = workspace_tmp_dir()
    try:
        (tmp_path / "config.py").write_text(
            "import yaml\nfrom bs4 import BeautifulSoup\n",
            encoding="utf-8",
            newline="\n",
        )

        imports, _ = scan_imports(tmp_path)

        assert imports == {"PyYAML": ["yaml"], "beautifulsoup4": ["bs4"]}
    finally:
        cleanup_tmp_dir(tmp_path)
