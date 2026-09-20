"""Test helpers for the early, script-style projects.

Projects 0 to 2 come before the tutorial introduces pytest, so their folders
hold no tests of their own. These repo-level tests keep them honest instead.
"""

import builtins
import random
import runpy
from pathlib import Path

import pytest

PROJECTS = Path(__file__).parent.parent / "projects"


@pytest.fixture
def play(monkeypatch, capsys):
    """Run a script as __main__ with scripted keyboard input and a fixed 'random' number.

    Returns everything the script printed, with prompts and replies interleaved
    as they would appear in a terminal.
    """

    def _play(script, replies, secret=42):
        answers = iter(replies)

        def fake_input(prompt=""):
            reply = next(answers)
            print(f"{prompt}{reply}")
            return reply

        monkeypatch.setattr(builtins, "input", fake_input)
        monkeypatch.setattr(random, "randint", lambda low, high: secret)
        runpy.run_path(str(PROJECTS / script), run_name="__main__")
        return capsys.readouterr().out

    return _play
