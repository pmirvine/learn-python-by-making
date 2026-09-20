"""The bug hunt's failing test: try what's shipped, where nothing else is installed.

The cure is in pyproject.toml, and not in the code: `uv remove --dev rich`, and then
`uv add rich`, which puts it under [project] dependencies, where users will get it.
"""

import shutil
import subprocess
from pathlib import Path

SHOUT = Path(__file__).parent.parent.parent / "bughunt" / "shout"


def shipped(project: Path, *command: str) -> subprocess.CompletedProcess[str]:
    """Build a project's wheel, and run a command with only that wheel installed."""
    subprocess.run(
        ["uv", "build", "--wheel", "--out-dir", "dist"], cwd=project, check=True
    )
    (wheel,) = (project / "dist").glob("*.whl")
    alone = ["uv", "run", "--isolated", "--no-project", "--with", str(wheel), *command]
    return subprocess.run(
        alone, cwd=project, capture_output=True, text=True, check=False
    )


def copy_of_shout(folder: Path) -> Path:
    ignore = shutil.ignore_patterns(".venv", "dist", "__pycache__", "uv.lock")
    return Path(shutil.copytree(SHOUT, folder / "shout", ignore=ignore))


def test_as_it_stands_it_cannot_run_anywhere_but_at_home(tmp_path: Path):
    done = shipped(copy_of_shout(tmp_path), "shout", "ship", "it")
    assert done.returncode != 0
    assert "No module named 'rich'" in done.stderr


def test_with_the_dependency_declared_it_can(tmp_path: Path):
    project = copy_of_shout(tmp_path)
    config = project / "pyproject.toml"
    text = config.read_text(encoding="utf-8")
    text = text.replace("dependencies = []", 'dependencies = ["rich>=15.0.0"]')
    config.write_text(text.replace('    "rich>=15.0.0",\n', ""), encoding="utf-8")

    done = shipped(project, "shout", "ship", "it")
    assert done.returncode == 0, done.stderr
    assert "SHIP IT!" in done.stdout
