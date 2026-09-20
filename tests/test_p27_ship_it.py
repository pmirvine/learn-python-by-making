"""Project 27: the type-in listing, the bug hunt's fault, and the README's picture."""

import re
import subprocess
import tomllib
from pathlib import Path

import pytest

PROJECT = Path(__file__).parent.parent / "projects" / "27-ship-it"


@pytest.fixture(scope="module")
def wheel(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("dist")
    command = ["uv", "build", "--wheel", "--out-dir", str(out), str(PROJECT)]
    subprocess.run(command, check=True, capture_output=True, timeout=120)
    (built,) = out.glob("*.whl")
    return built


def test_the_type_in_listing_fits_the_page():
    lines = (PROJECT / "inside.py").read_text(encoding="utf-8").splitlines()
    assert len(lines) <= 30


def test_the_type_in_listing_looks_inside_a_wheel(wheel: Path):
    done = subprocess.run(
        ["uv", "run", "--project", str(PROJECT), "python", "inside.py", str(wheel)],
        capture_output=True, text=True, encoding="utf-8", cwd=PROJECT, check=True, timeout=120,
    )  # fmt: skip
    assert "beeb/py.typed" in done.stdout
    assert re.search(r"Name:\s+beeb-lpbm", done.stdout)
    assert re.search(r"Requires-Dist:\s+pygame-ce>=2\.5\.2", done.stdout)
    assert re.search(r"a README of \d+ words", done.stdout)


def test_the_bug_hunt_declares_its_dependency_in_the_wrong_place():
    config = tomllib.loads(
        (PROJECT / "bughunt/shout/pyproject.toml").read_text("utf-8")
    )
    assert config["project"]["dependencies"] == []
    assert any(item.startswith("rich") for item in config["dependency-groups"]["dev"])
    assert "from rich" in (PROJECT / "bughunt/shout/src/shout/__init__.py").read_text(
        "utf-8"
    )


def test_the_readme_uses_whole_addresses_because_pypi_needs_them():
    readme = (PROJECT / "README.md").read_text(encoding="utf-8")
    targets = re.findall(r"\]\(([^)]+)\)", readme)
    assert targets
    assert all(target.startswith("https://") for target in targets), targets
    assert (PROJECT / "docs" / "testcard.png").is_file()


def test_the_workflows_agree_with_the_chapter():
    check = (PROJECT / ".github/workflows/check.yml").read_text(encoding="utf-8")
    release = (PROJECT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "--resolution lowest-direct" in check
    assert "--with dist/*.whl" in check
    assert "workflow_call" in check
    assert "id-token: write" in release
    assert "uv publish --index testpypi" in release
