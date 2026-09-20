import tomllib
from pathlib import Path

import pytest

import beeb
from beeb import cli


def test_the_version_is_the_one_in_pyproject():
    project = Path(__file__).parent.parent / "pyproject.toml"
    declared = tomllib.loads(project.read_text(encoding="utf-8"))["project"]["version"]
    assert beeb.__version__ == declared


def test_the_command_knows_its_version(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["beeb", "--version"])
    with pytest.raises(SystemExit):
        cli.main()
    assert capsys.readouterr().out.strip() == f"beeb {beeb.__version__}"


def test_the_test_card_has_eight_bars():
    cli.test_card()
    step = beeb.WIDTH // 8
    seen = [beeb.point(step * bar + step // 2, 512) for bar in range(8)]
    assert seen == list(range(8))


def test_everything_that_is_promised_is_there():
    for name in beeb.__all__:
        assert hasattr(beeb, name), name
