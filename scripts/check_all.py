"""Check every project in the tutorial, then the tutorial itself.

    uv run scripts/check_all.py            # everything
    uv run scripts/check_all.py 08         # just the projects whose folder starts with 08

Each project under projects/ is linted and tested inside its own environment,
from its own folder, so it behaves exactly as a reader's copy would.
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PROJECTS = ROOT / "projects"

failures: list[str] = []


def run(label: str, command: list[str | Path], cwd: Path) -> None:
    print(f"  {label:<28}", end="", flush=True)
    # UTF-8 everywhere, whatever the platform's default: the projects print
    # characters such as █ and ●, and Windows would otherwise choke on them.
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=os.environ | {"PYTHONUTF8": "1"},
        check=False,
    )
    if result.returncode == 0:
        print("ok")
        return
    print("FAILED")
    print(result.stdout + result.stderr)
    failures.append(f"{cwd.name}: {label}")


def check_project(project: Path) -> None:
    print(f"\n{project.name}")
    number = project.name.split("-")[0]
    ruff = ["uv", "run", "--project", ROOT, "ruff"]

    run("lockfile up to date", ["uv", "lock", "--check"], project)
    run("ruff check", [*ruff, "check", "."], project)
    run("ruff format --check", [*ruff, "format", "--check", "."], project)

    # A reader's tests live in tests/, or beside the code in the early, flat projects.
    if (project / "tests").is_dir() or list(project.glob("test_*.py")):
        ignore = [f"--ignore={folder}" for folder in ("stages", "bughunt", "solutions")]
        run("project tests", ["uv", "run", "pytest", "-q", *ignore], project)
    if list((project / "solutions").rglob("test_*.py")):
        run("solutions tests", ["uv", "run", "pytest", "-q", "solutions"], project)

    repo_tests = sorted((ROOT / "tests").glob(f"test_p{number}_*.py"))
    if repo_tests:
        command = [
            "uv",
            "run",
            "--project",
            project,
            "--with",
            "pytest",
            "pytest",
            "-q",
        ]
        run("repo-level tests", [*command, *repo_tests], ROOT)


def check_tutorial() -> None:
    print("\ntutorial")
    run("ruff check", ["uv", "run", "ruff", "check", "scripts", "tests"], ROOT)
    command = ["uv", "run", "ruff", "format", "--check", "scripts", "tests"]
    run("ruff format --check", command, ROOT)
    run("listings and REPL sessions", ["uv", "run", "scripts/check_docs.py"], ROOT)
    run("site builds", ["uv", "run", "zensical", "build", "--clean"], ROOT)


def main() -> None:
    wanted = sys.argv[1:]
    for project in sorted(p for p in PROJECTS.iterdir() if p.is_dir()):
        if not wanted or any(project.name.startswith(prefix) for prefix in wanted):
            check_project(project)
            # A project may hold another inside it: Project 11 has a Breakout
            # that depends on the beeb package in the folder above it, and
            # Project 27's bug hunt is a whole package with a fault in it.
            inside = [
                *project.glob("*/pyproject.toml"),
                *project.glob("bughunt/*/pyproject.toml"),
            ]
            for nested in sorted(inside):
                check_project(nested.parent)
    if not wanted:
        check_tutorial()

    if failures:
        print(f"\n{len(failures)} failed:")
        for failure in failures:
            print(f"  {failure}")
        raise SystemExit(1)
    print("\nAll good.")


if __name__ == "__main__":
    main()
