"""Repo-level checks for Project 11: the programs a reader runs, with no loudspeaker.

The reader's own tests are in the project's tests/ folder.
"""

import subprocess
import sys
import wave
from pathlib import Path

import pytest

pytest.importorskip("beeb.synth", reason="needs the Project 11 environment")

P11 = Path(__file__).parent.parent / "projects" / "11-sound-and-envelope"
HEADLESS = Path(__file__).parent / "headless.py"


@pytest.mark.parametrize("script", ["examples/beep.py", "siren.py"])
def test_wav_writers(script, tmp_path):
    result = subprocess.run(
        [sys.executable, P11 / script],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    (saved,) = tmp_path.glob("*.wav")
    with wave.open(str(saved), "rb") as file:
        assert file.getframerate() == 22_050
        assert file.getsampwidth() == 2
        assert file.getnframes() >= 22_050


@pytest.mark.parametrize(
    "script", ["examples/scope.py", "examples/piano.py", "examples/tune.py"]
)
def test_program_runs_for_thirty_frames(script):
    result = subprocess.run(
        [sys.executable, HEADLESS, P11 / script, "30"],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_the_bug_hunt_crashes_as_the_chapter_says():
    result = subprocess.run(
        [sys.executable, P11 / "bughunt" / "chord.py"],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
        env={"SDL_AUDIODRIVER": "dummy", "PATH": ""},
    )
    assert result.returncode != 0
    assert "OverflowError" in result.stderr
