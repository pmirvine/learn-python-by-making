"""Project 28: the stage script, the bug hunt, and the listings on the disc."""

import subprocess
from pathlib import Path

PROJECT = Path(__file__).parent.parent / "projects" / "28-boot-to-basic"
HEADLESS = {"SDL_VIDEODRIVER": "dummy", "SDL_AUDIODRIVER": "dummy"}


def run(*args: str) -> str:
    import os

    done = subprocess.run(
        ["uv", "run", "--project", str(PROJECT), *args],
        capture_output=True, text=True, encoding="utf-8", cwd=PROJECT, check=True,
        timeout=180, env={**os.environ, **HEADLESS},
    )  # fmt: skip
    return done.stdout


def test_stage_three_draws_its_three_layers():
    code = (
        "import runpy; runpy.run_path('stages/stage3_screen.py')['main'](frames=2); "
        "import pygame; window = pygame.display.get_surface(); "
        "print(window.get_size(), window.get_at((40, 40))[:3])"
    )
    size, _, colour = run("python", "-c", code).strip().splitlines()[-1].partition(") ")
    assert size == "(640, 512"
    assert colour == "(255, 255, 0)", "the banner should be yellow, over the red lines"


def test_the_bug_hunt_really_has_it_backwards():
    out = run("python", "bughunt/glancing.py")
    assert "One right on top of the other. Touching? False" in out
    assert "Nowhere near each other.       Touching? True" in out


def test_the_type_in_game_fits_the_page():
    listing = (
        (PROJECT / "src" / "micro" / "welcome" / "alien.bas")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    assert len(listing) <= 30
    assert all(len(line) <= 88 for line in listing)


def test_the_micro_depends_on_four_of_the_readers_own_packages():
    import tomllib

    config = tomllib.loads((PROJECT / "pyproject.toml").read_text(encoding="utf-8"))
    assert set(config["tool"]["uv"]["sources"]) == {
        "beeb-lpbm", "pyfax", "sprite-editor", "tiny-basic",
    }  # fmt: skip


def test_the_welcome_disc_travels_in_the_wheel(tmp_path: Path):
    import zipfile

    command = ["uv", "build", "--wheel", "--out-dir", str(tmp_path), str(PROJECT)]
    subprocess.run(command, check=True, capture_output=True, timeout=180)
    (wheel,) = tmp_path.glob("*.whl")
    names = zipfile.ZipFile(wheel).namelist()
    assert "micro/welcome/alien.bas" in names
    assert "micro/welcome/ship.sprite" in names
    assert "micro/py.typed" in names


def test_the_command_knows_its_version():
    assert run("micro", "--version").strip().endswith("micro 0.1.0")
