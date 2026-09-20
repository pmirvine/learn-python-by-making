"""Is this ready to be released? These tests look at the project, and not at the code."""

import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
PROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
    "project"
]


def notes(version: str) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(ROOT / "scripts" / "notes.py"), version]
    return subprocess.run(
        command, capture_output=True, text=True, encoding="utf-8", check=False
    )


def test_the_changelog_has_something_to_say_about_this_version():
    done = notes(PROJECT["version"])
    assert done.returncode == 0, done.stderr
    assert "### " in done.stdout
    assert "## [" not in done.stdout


def test_the_changelog_says_nothing_about_a_version_that_never_was():
    done = notes("0.0.7")
    assert done.returncode != 0
    assert "says nothing about 0.0.7" in done.stderr


@pytest.fixture(scope="session")
def wheel(tmp_path_factory: pytest.TempPathFactory) -> zipfile.ZipFile:
    """Build the wheel, as `uv build` would, and open it."""
    out = tmp_path_factory.mktemp("dist")
    command = ["uv", "build", "--wheel", "--out-dir", str(out), str(ROOT)]
    subprocess.run(command, check=True, capture_output=True)
    (built,) = out.glob("*.whl")
    return zipfile.ZipFile(built)


def test_the_wheel_holds_the_package_and_nothing_else(wheel: zipfile.ZipFile):
    tops = {name.split("/")[0] for name in wheel.namelist()}
    assert tops == {"beeb", f"beeb_lpbm-{PROJECT['version']}.dist-info"}


def test_the_wheel_says_that_it_has_type_hints_and_a_licence(wheel: zipfile.ZipFile):
    names = wheel.namelist()
    assert "beeb/py.typed" in names
    assert any(name.endswith("licenses/LICENSE") for name in names)


def test_the_wheel_knows_its_command(wheel: zipfile.ZipFile):
    (entry_points,) = [
        name for name in wheel.namelist() if name.endswith("entry_points.txt")
    ]
    assert "beeb = beeb.cli:main" in wheel.read(entry_points).decode()
