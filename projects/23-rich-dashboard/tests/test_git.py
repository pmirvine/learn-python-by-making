from datetime import UTC, datetime, timedelta

import pytest

from dashboard import git


def test_commit_times_come_back_newest_first_with_their_time_zones(make_project):
    folder = make_project(
        "snake",
        [("a.py", "2026-03-02T10:00:00+00:00"), ("b.py", "2026-03-09T23:30:00+05:30")],
    )
    newest, oldest = git.commit_times(folder)
    assert oldest == datetime(2026, 3, 2, 10, tzinfo=UTC)
    assert newest.utcoffset() == timedelta(hours=5, minutes=30)
    assert newest == datetime(2026, 3, 9, 18, tzinfo=UTC)
    assert newest.tzinfo != UTC


def test_branch_and_changes(make_project):
    folder = make_project("snake", [("a.py", "2026-03-02T10:00:00+00:00")])
    assert git.branch(folder) == "main"
    assert git.changed_files(folder) == 0
    (folder / "a.py").write_text("changed\n", encoding="utf-8")
    (folder / "new.py").write_text("new\n", encoding="utf-8")
    assert git.changed_files(folder) == 2


def test_a_folder_inside_a_repository_has_a_history_of_its_own(make_project):
    folder = make_project("making", [("a.py", "2026-03-02T10:00:00+00:00")])
    inner = folder / "inner"
    inner.mkdir()
    assert git.is_tracked(inner)
    assert git.commit_times(inner) == []


def test_a_plain_folder_is_not_tracked(tmp_path):
    assert not git.is_tracked(tmp_path)
    with pytest.raises(git.GitError, match="not a git repository"):
        git.commit_times(tmp_path)


def test_git_missing_altogether(tmp_path, monkeypatch):
    monkeypatch.setattr("shutil.which", lambda name: None)
    with pytest.raises(git.GitError, match="no git on this machine"):
        git.run_git(tmp_path, "status")
