"""Repo-level checks for the bonus chapter, "Share it".

Both pages were run in a real browser while the chapter was written (see
scripts/browser.py). What can be checked without one is checked here.
"""

import ast
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).parent.parent
BONUS = ROOT / "projects" / "22x-share-it"
LIFE = ROOT / "projects" / "06-life" / "src" / "life"
HEADLESS = Path(__file__).parent / "headless.py"


def test_the_site_is_put_together_from_the_page_and_project_6s_package(tmp_path):
    result = subprocess.run(
        [sys.executable, BONUS / "make_site.py"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=True,
    )
    assert "Made site/" in result.stdout
    site = tmp_path / "site"
    assert (site / "index.html").is_file()
    assert (site / "life" / "core.py").read_text(encoding="utf-8") == (
        LIFE / "core.py"
    ).read_text(encoding="utf-8")
    assert not (site / "life" / "cli.py").exists()


def test_the_page_is_told_about_every_file_that_the_package_imports():
    settings = tomllib.loads(
        (BONUS / "life-in-a-tab" / "pyscript.toml").read_text(encoding="utf-8")
    )
    listed = {Path(name).name for name in settings["files"]}
    init = (LIFE / "__init__.py").read_text(encoding="utf-8")
    needed = {f"{module}.py" for module in re.findall(r"from life\.(\w+) import", init)}
    assert needed | {"__init__.py"} == listed


def test_the_pages_python_is_python_with_an_await_at_the_top_level():
    source = (BONUS / "life-in-a-tab" / "main.py").read_text(encoding="utf-8")
    compile(source, "main.py", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
    assert "from life import soup, step" in source


def test_the_page_asks_for_the_release_of_pyscript_that_the_chapter_names():
    html = (BONUS / "life-in-a-tab" / "index.html").read_text(encoding="utf-8")
    assert html.count("https://pyscript.net/releases/2026.7.3/") == 2


def test_the_cube_still_runs_on_the_desktop_with_its_loop_made_async():
    result = subprocess.run(
        [sys.executable, HEADLESS, BONUS / "cube-in-a-tab" / "main.py", "20"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr
