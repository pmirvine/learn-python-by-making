"""Repo-level checks for Project 20: the bug hunt, the type-in, and the extras.

The reader's own tests are in the project's tests/ folder.
"""

import importlib.util
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

pytest.importorskip("pyfax_live", reason="needs the Project 20 environment")

P20 = Path(__file__).parent.parent / "projects" / "20-pyfax-live"


def test_the_bug_hunt_shows_its_symptom():
    result = subprocess.run(
        [sys.executable, P20 / "bughunt" / "search.py"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )
    assert result.returncode == 1
    assert "Letters from Enid:\n    More hedgehogs, please." in result.stdout
    assert 'sqlite3.OperationalError: near "Brien": syntax error' in result.stderr


def test_and_the_same_hole_lets_a_stranger_read_everything():
    spec = importlib.util.spec_from_file_location(
        "search", P20 / "bughunt" / "search.py"
    )
    search = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(search)
    import sqlite3

    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE letters (name TEXT, message TEXT)")
    db.executemany("INSERT INTO letters VALUES (?, ?)", search.LETTERS)
    leaked = search.letters_from(db, "' OR '1'='1")
    assert len(leaked) == len(search.LETTERS)
    assert any("NOT FOR PUBLICATION" in message for message in leaked)


def test_the_type_in_clock_serves_a_picture_that_asks_to_be_fetched_again():
    spec = importlib.util.spec_from_file_location("clock", P20 / "clock.py")
    clock = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(clock)
    response = clock.app.test_client().get("/")
    assert response.mimetype == "image/svg+xml"
    assert response.headers["Refresh"] == "1"
    tree = ET.fromstring(response.text)
    assert len(list(tree.iter("{http://www.w3.org/2000/svg}line"))) == 3


def test_the_application_starts_with_its_own_settings(tmp_path, monkeypatch):
    from pyfax_live import create_app

    monkeypatch.chdir(P20)
    monkeypatch.setenv("PYFAX_DATABASE", str(tmp_path / "env.sqlite3"))
    monkeypatch.setenv("PYFAX_SECRET_KEY", "from the environment")
    monkeypatch.setenv("PYFAX_WEATHER_SECONDS", "60")
    app = create_app()
    assert app.config["SECRET_KEY"] == "from the environment"
    assert app.config["WEATHER_SECONDS"] == 60
    assert (tmp_path / "env.sqlite3").exists()
    index = app.test_client().get("/100.html").text
    assert 'href="301.html"' in index
    assert 'href="500.html"' in index


def test_the_launch_configuration_is_sound():
    launch = json.loads((P20 / ".vscode" / "launch.json").read_text(encoding="utf-8"))
    (configuration,) = launch["configurations"]
    assert configuration["module"] == "flask"
    assert "--no-reload" in configuration["args"]
