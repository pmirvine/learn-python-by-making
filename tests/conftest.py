"""Test helpers for the early, script-style projects.

Projects 0 to 2 come before the tutorial introduces pytest, so their folders
hold no tests of their own. These repo-level tests keep them honest instead.
"""

import builtins
import random
import runpy
import time
from pathlib import Path

import pytest

PROJECTS = Path(__file__).parent.parent / "projects"


@pytest.fixture
def play(monkeypatch, capsys):
    """Run a script as __main__ with scripted keyboard input and fixed 'random' choices.

    `secret` is what random.randint returns; `code`, if given, is what
    random.choices and random.sample return. time.sleep returns at once.

    Returns everything the script printed, with prompts and replies interleaved
    as they would appear in a terminal.
    """

    def _play(script, replies, secret=42, code=None):
        answers = iter(replies)

        def fake_input(prompt=""):
            reply = next(answers)
            print(f"{prompt}{reply}")
            return reply

        monkeypatch.setattr(builtins, "input", fake_input)
        monkeypatch.setattr(random, "randint", lambda low, high: secret)
        if code is not None:
            monkeypatch.setattr(random, "choices", lambda population, k: list(code))
            monkeypatch.setattr(random, "sample", lambda population, k: list(code))
        monkeypatch.setattr(time, "sleep", lambda seconds: None)
        runpy.run_path(str(PROJECTS / script), run_name="__main__")
        return capsys.readouterr().out

    return _play
