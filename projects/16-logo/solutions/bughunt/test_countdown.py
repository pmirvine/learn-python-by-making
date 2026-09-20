"""The smallest program that shows the bug, as a test.

The colleague's Logo says 0 0 0. Yours says 1 2 3.
"""

import importlib.util
from pathlib import Path

from logo import Interpreter
from logo.turtle import Recorder

COUNTDOWN = """
    to countdown :n
      if :n = 0 [stop]
      countdown :n - 1
      print :n
    end
    countdown 3
"""


def colleagues_logo() -> type[Interpreter]:
    path = Path(__file__).parent.parent.parent / "bughunt" / "lopsided.py"
    spec = importlib.util.spec_from_file_location("lopsided", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ColleaguesLogo


def test_each_call_has_inputs_of_its_own():
    said: list[str] = []
    Interpreter(Recorder(), say=said.append).run(COUNTDOWN)
    assert said == ["1", "2", "3"]


def test_which_the_colleagues_logo_gets_wrong_in_this_particular_way():
    said: list[str] = []
    colleagues_logo()(Recorder(), say=said.append).run(COUNTDOWN)
    assert said == ["0", "0", "0"]
