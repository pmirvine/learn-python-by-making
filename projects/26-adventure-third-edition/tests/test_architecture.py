"""Tests of which module may know about which. They read the code, and don't run it."""

import ast
import sys
from pathlib import Path

import cupboard

import adventure

ENGINE = Path(cupboard.__file__).parent
FRONT_END = Path(adventure.__file__).parent


def imports_of(path: Path) -> set[str]:
    """Return the top-level name of everything that a file imports."""
    found: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        match node:
            case ast.Import(names=names):
                found |= {alias.name.split(".")[0] for alias in names}
            case ast.ImportFrom(module=str(module), level=0):
                found.add(module.split(".")[0])
            case _:
                pass
    return found


def test_the_engine_knows_nothing_but_python_and_itself():
    for path in ENGINE.glob("*.py"):
        strangers = imports_of(path) - sys.stdlib_module_names - {"cupboard"}
        assert not strangers, f"{path.name} imports {strangers}"


def test_only_two_modules_know_which_game_is_being_played():
    knowing = {
        path.name for path in FRONT_END.glob("*.py") if "cupboard" in imports_of(path)
    }
    assert knowing == {"colossal.py"}
    assert "colossal" in (FRONT_END / "cli.py").read_text(encoding="utf-8")


def test_the_map_and_the_bargain_know_nothing_of_textual():
    for name in ["game.py", "chart.py", "colossal.py"]:
        assert not {"textual", "rich"} & imports_of(FRONT_END / name), name
