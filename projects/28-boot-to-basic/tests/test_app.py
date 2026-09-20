from pathlib import Path

from micro.app import stock


def test_a_new_disc_is_stocked_with_the_welcome_programs(tmp_path: Path):
    stock(tmp_path / "disc")
    names = {path.name for path in (tmp_path / "disc").iterdir()}
    assert {
        "alien.bas",
        "carpet.bas",
        "ship.sprite",
        "alien.sprite",
        "bolt.sprite",
    } <= names


def test_what_is_on_the_disc_already_is_left_alone(tmp_path: Path):
    (tmp_path / "alien.bas").write_text('10 PRINT "MINE"\n', encoding="utf-8")
    stock(tmp_path)
    assert (tmp_path / "alien.bas").read_text(encoding="utf-8") == '10 PRINT "MINE"\n'
    assert (tmp_path / "carpet.bas").exists()
