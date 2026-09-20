"""Repo-level checks for Project 17: the example programs, the bug hunt, and the extras.

The reader's own tests are in the project's tests/ folder.
"""

import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("tiny_basic", reason="needs the Project 17 environment")

P17 = Path(__file__).parent.parent / "projects" / "17-tiny-basic"
BASIC = ("-c", "from tiny_basic.repl import main; main()")  # what `uv run basic` does


def run(*arguments: str | Path, typed: str = "") -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *arguments],
        input=typed,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
        check=False,
    )


def test_the_wave_is_a_wave():
    result = run(*BASIC, P17 / "examples" / "wave.bas")
    assert result.returncode == 0, result.stderr
    columns = [line.index("*") for line in result.stdout.splitlines()]
    # 12.6 is 42 steps of 0.3, and so there "ought" to be 43. Floats say otherwise.
    assert len(columns) == 42
    assert columns[0] == 20
    assert min(columns) == 2
    assert max(columns) == 37


def test_hi_lo_can_be_won():
    # Guess every number from 1 to 100 in turn. One of them has to be right.
    typed = "\n".join(str(guess) for guess in range(1, 101))
    result = run(*BASIC, P17 / "examples" / "hilo.bas", typed=typed)
    assert result.returncode == 0, result.stderr
    assert "Too low." in result.stdout or "in 1 tries" in result.stdout
    assert "Too high." not in result.stdout
    assert "Got it, in " in result.stdout.splitlines()[-1]


def test_the_primes_program_counts_correctly_with_a_smaller_limit(tmp_path):
    source = (P17 / "examples" / "primes.bas").read_text(encoding="utf-8")
    program = tmp_path / "primes.bas"
    program.write_text(source.replace("LIMIT = 20000", "LIMIT = 100"), encoding="utf-8")
    result = run(*BASIC, program, "--time")
    assert result.stdout == "25 primes below 100\n"
    assert "[running:" in result.stderr


def test_a_conversation_at_the_prompt():
    typed = '10 PRINT "HELLO"\n20 GOTO 10\nLIST\n30 FROB\nQUIT\n'
    result = run(*BASIC, typed=typed)
    assert '   10 PRINT "HELLO"\n   20 GOTO 10\n' in result.stdout
    assert "Mistake: I don't know what to do with FROB" in result.stdout


def test_the_bug_hunt_shows_its_symptom():
    result = run(P17 / "bughunt" / "sums.py")
    assert result.returncode == 0, result.stderr
    assert "10 - 4 - 3     = 9   <-- it ought to be 3" in result.stdout
    assert result.stdout.count("it ought to be") == 3
    assert "2 ^ 3 ^ 2      = 512\n" in result.stdout


def test_parsing_once_is_a_good_deal_cheaper():
    result = run(P17 / "measure_parse.py")
    assert result.returncode == 0, result.stderr
    times = float(result.stdout.rstrip().split()[-3])
    assert times > 3


def test_the_workflow_and_the_settings_say_what_the_chapter_says():
    workflow = (P17 / ".github" / "workflows" / "check.yml").read_text(encoding="utf-8")
    for step in (
        "uv sync --locked",
        "ruff check",
        "ruff format --check",
        "pyright",
        "pytest --cov",
    ):
        assert f"- run: uv run {step}" in workflow or f"- run: {step}" in workflow
    settings = (P17 / "pyproject.toml").read_text(encoding="utf-8")
    assert 'typeCheckingMode = "strict"' in settings
    assert 'basic = "tiny_basic.repl:main"' in settings


def test_the_package_passes_pyright_in_strict_mode():
    """The chapter says "0 errors". pyright fetches its own Node the first time."""
    result = subprocess.run(
        [sys.executable, "-m", "pyright"],
        cwd=P17,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=600,
        check=False,
    )
    if "0 errors" not in result.stdout and "error:" not in result.stdout:
        pytest.skip(f"pyright couldn't be run here: {result.stderr[-200:]}")
    assert "0 errors, 0 warnings" in result.stdout, result.stdout
