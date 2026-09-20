from dashboard.stats import busiest_day, find_projects, measure, scan

MONDAY, TUESDAY = "2026-03-02T10:00:00+00:00", "2026-03-03T10:00:00+00:00"


def test_measuring_a_project_leaves_out_what_it_has_installed(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "game.py").write_text("x = 1\n\n\ny = 2\n", encoding="utf-8")
    (tmp_path / "test_game.py").write_text(
        "def test_one(): ...\n\nasync def test_two(): ...\n\ndef helper(): ...\n",
        encoding="utf-8",
    )
    installed = tmp_path / ".venv" / "lib"
    installed.mkdir(parents=True)
    (installed / "huge.py").write_text("z = 3\n" * 1000, encoding="utf-8")
    assert measure(tmp_path) == (5, 2)


def test_scanning_a_project(make_project):
    folder = make_project(
        "snake", [("a.py", MONDAY), ("b.py", MONDAY), ("c.py", TUESDAY)]
    )
    project = scan(folder)
    assert (project.name, project.branch, project.changed) == ("snake", "main", 0)
    assert len(project.commits) == 3
    assert project.days_worked == 2
    assert project.latest is not None
    assert f"{project.latest:%A}" == "Tuesday"
    assert project.lines == 3


def test_a_project_that_is_not_in_git_is_still_a_project(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    project = scan(tmp_path)
    assert project.commits == []
    assert project.latest is None
    assert project.branch == ""


def test_finding_projects(make_project, tmp_path):
    make_project("snake", [])
    make_project("breakout", [])
    (tmp_path / "notes").mkdir()
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    assert [folder.name for folder in find_projects(tmp_path)] == ["breakout", "snake"]


def test_the_busiest_day(make_project):
    snake = scan(make_project("snake", [("a.py", MONDAY), ("b.py", TUESDAY)]))
    life = scan(make_project("life", [("a.py", TUESDAY)]))
    assert busiest_day([snake, life]) == "Tuesday, with 2 commits"
    assert busiest_day([]) == "no day yet"
