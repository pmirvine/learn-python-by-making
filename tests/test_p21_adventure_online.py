"""Repo-level checks for Project 21: the bug hunt, the type-in, and the extras.

The reader's own tests are in the project's tests/ folder. The pages were also
driven in a real browser while the chapter was written: see scripts/browser.py.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("cupboard_web", reason="needs the Project 21 environment")

P21 = Path(__file__).parent.parent / "projects" / "21-adventure-online"
WEB = P21 / "src" / "cupboard_web"


def test_the_type_in_reads_a_session_cookie_with_no_key():
    from cupboard_web import create_app

    client = create_app({"SECRET_KEY": "nobody told peek.py this"}).test_client()
    page = client.get("/").text
    token = page.split('name="token" value="')[1].split('"')[0]
    client.post("/command", data={"text": "south", "token": token})
    cookie = client.get_cookie("session")
    assert cookie is not None

    result = subprocess.run(
        [sys.executable, P21 / "peek.py", cookie.value],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=True,
    )
    revealed = json.loads(result.stdout.split("\n\nThe signature")[0])
    assert revealed["state"]["location"] == "hall"
    assert revealed["state"]["places"]["key"] == "flowerpots"


def test_the_bug_hunt_has_everybody_playing_one_game():
    spec = importlib.util.spec_from_file_location(
        "shared", P21 / "bughunt" / "shared.py"
    )
    shared = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(shared)
    alice, bob = shared.app.test_client(), shared.app.test_client()
    assert "Moves: 0" in bob.get("/").text
    alice.post("/command", data={"text": "south"})
    assert "Moves: 1" in bob.get("/").text


def test_htmx_is_the_version_that_the_chapter_names():
    script = (WEB / "static" / "htmx.min.js").read_text(encoding="utf-8")
    assert 'version:"2.0.10"' in script


def test_the_templates_need_nothing_that_the_content_security_policy_forbids():
    for template in (WEB / "templates").glob("*.html"):
        html = template.read_text(encoding="utf-8")
        assert "<style" not in html, template.name
        assert "hx-on" not in html, template.name
        assert "onclick" not in html, template.name
        assert "https://" not in html, template.name


def test_the_example_env_file_holds_no_secret():
    example = (P21 / ".env.example").read_text(encoding="utf-8")
    assert "CUPBOARD_SECRET_KEY=\n" in example
    assert not (P21 / ".env").exists()
