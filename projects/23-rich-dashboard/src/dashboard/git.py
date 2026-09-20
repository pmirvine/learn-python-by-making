"""Asking Git questions, by running it, and reading what it says."""

import shutil
import subprocess
from datetime import datetime
from pathlib import Path


class GitError(Exception):
    """Git couldn't be run, or didn't like what it was asked."""


def run_git(folder: Path, *arguments: str) -> str:
    """Run `git` in a folder, and return what it printed."""
    if shutil.which("git") is None:
        raise GitError("There's no git on this machine")
    try:
        finished = subprocess.run(
            ["git", "-C", str(folder), *arguments],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
            timeout=30,
        )
    except subprocess.CalledProcessError as error:
        raise GitError(error.stderr.strip() or f"git {arguments[0]} failed") from error
    except subprocess.TimeoutExpired as error:
        raise GitError(f"git {arguments[0]} took too long in {folder}") from error
    return finished.stdout


def is_tracked(folder: Path) -> bool:
    """Is this folder inside a Git repository?"""
    try:
        return run_git(folder, "rev-parse", "--is-inside-work-tree").strip() == "true"
    except GitError:
        return False


def commit_times(folder: Path) -> list[datetime]:
    """Return when each commit that touched this folder was made, newest first."""
    printed = run_git(folder, "log", "--format=%aI", "--", ".")
    return [datetime.fromisoformat(line) for line in printed.splitlines()]


def branch(folder: Path) -> str:
    return run_git(folder, "branch", "--show-current").strip() or "(detached)"


def changed_files(folder: Path) -> int:
    """How many files in this folder have changes that haven't been committed?"""
    return len(run_git(folder, "status", "--porcelain", "--", ".").splitlines())
