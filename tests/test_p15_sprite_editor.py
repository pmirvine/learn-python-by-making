"""Repo-level checks for Project 15: the stages, the bug hunt, and the extras.

The reader's own tests are in the project's tests/ folder.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("sprite_editor", reason="needs the Project 15 environment")

from sprite_editor.sprite import Sprite

P15 = Path(__file__).parent.parent / "projects" / "15-sprite-editor"
HEADLESS = Path(__file__).parent / "headless.py"


def load_stage(name: str):
    spec = importlib.util.spec_from_file_location(name, P15 / "stages" / f"{name}.py")
    stage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stage)
    return stage


def run(*arguments: str | Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )


def test_the_stages_work_and_say_nothing():
    for name in ("stage1_sprite", "stage2_commands", "stage3_tools", "stage4_app"):
        source = (P15 / "stages" / f"{name}.py").read_text(encoding="utf-8")
        assert "logging" not in source, name

    sprite = load_stage("stage1_sprite").Sprite.from_text("sprite 2 1\n.3\n")
    assert sprite[1, 0] == 3

    commands = load_stage("stage2_commands")
    picture = Sprite.from_text("sprite 2 1\n.3\n")
    history = commands.History(picture)
    history.perform(commands.Flip())
    assert picture[0, 0] == 3
    history.undo()
    assert picture[1, 0] == 3

    tools = load_stage("stage3_tools")
    pencil = tools.Pencil()
    pencil.press(picture, (0, 0), 5)
    assert pencil.release(picture).after == {(0, 0): 5}
    assert issubclass(tools.Eraser, tools.Pencil)


def test_the_example_sprites_load():
    for path in (P15 / "examples").glob("*.sprite"):
        sprite = Sprite.load(path)
        assert (sprite.width, sprite.height) == (16, 16), path.name
        assert sprite.pixels, path.name


def test_the_bug_hunt_shows_its_symptom():
    result = run(P15 / "bughunt" / "history.py")
    assert result.returncode == 0, result.stderr
    assert "DEBUG Did Blue line. 1 done, 1 undone" in result.stdout
    assert "1 1 1 1 1" in result.stdout
    assert result.stdout.rstrip().endswith(". . . . .\n    . . 4 . .\n    . . 4 . .")


def test_the_mended_history():
    result = run(P15 / "solutions" / "bughunt" / "history.py")
    assert result.returncode == 0, result.stderr
    assert "DEBUG Did Blue line. 1 done, 0 undone" in result.stdout
    assert "1 1 1 1 1" not in result.stdout


def test_the_type_in_shows_a_sprite_in_the_terminal():
    result = run(P15 / "show.py", P15 / "examples" / "invader.sprite")
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    assert len(lines) == 8
    assert "\x1b[32;42m▀" in lines[3]
    assert all(line.endswith("\x1b[0m") for line in lines)


def test_the_editor_runs_and_keeps_a_log(tmp_path):
    program = tmp_path / "play.py"
    log_file = tmp_path / "editor.log"
    picture = tmp_path / "new.sprite"
    program.write_text(
        "import sys\n"
        "from sprite_editor.app import main\n\n"
        f"sys.argv = ['sprite-editor', r'{picture}', '-vv', '--log-file', r'{log_file}']\n"
        "main()\n",
        encoding="utf-8",
    )
    result = run(HEADLESS, program, "20")
    assert result.returncode == 0, result.stderr
    assert "isn't there yet, so here's a blank 16 by 16" in log_file.read_text(
        encoding="utf-8"
    )


def test_the_stage4_editor_runs_too(tmp_path):
    program = tmp_path / "play.py"
    program.write_text(
        "import runpy, sys\n"
        f"sys.argv = ['sprite-editor', r'{tmp_path / 'new.sprite'}']\n"
        f"runpy.run_path(r'{P15 / 'stages' / 'stage4_app.py'}')['main']()\n",
        encoding="utf-8",
    )
    result = run(HEADLESS, program, "20")
    assert result.returncode == 0, result.stderr


def test_the_launch_configuration_is_sound():
    launch = json.loads((P15 / ".vscode" / "launch.json").read_text(encoding="utf-8"))
    (configuration,) = launch["configurations"]
    assert configuration["module"] == "sprite_editor.app"
    source = (P15 / "src" / "sprite_editor" / "app.py").read_text(encoding="utf-8")
    assert source.rstrip().endswith('if __name__ == "__main__":\n    main()')
