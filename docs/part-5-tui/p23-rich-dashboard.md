# Project 23 · Rich Dashboard

You've been at this for a while. There's a folder on your machine, called `making`, with more than twenty projects in it, and every one of them has a history in Git. How many commits is that? How many lines of Python? How many tests? Which project took longest? On which day of the week do you really do the work?

![A terminal window showing a dashboard: a panel that says "Your busiest day is Friday, with 29 commits", and a table of eight projects, newest first, with their branches, commits, last commit, lines, tests, and a little bar chart of the last twelve weeks for each. The bar charts form a staircase](../assets/p23-dashboard.svg)

This project answers those questions, in the terminal, and it looks like that. The staircase down the right-hand side is you, working through the tutorial, a project at a time.

Part 5 is about the terminal, and it starts with **Rich**, which you used in Project 4 for a few colours. It can do a great deal more than that. The Python in this chapter is the everyday sort that fills real programs, and that the tutorial hasn't had a reason to look at properly until now: **running other programs** and reading what they say, **dates and times**, and **sorting things by whatever you like**.

| | |
|---|---|
| **You'll learn** | `subprocess`; `datetime`, `timedelta`, time zones, and why a time should always know its zone; `Counter` again, and `defaultdict`; sort keys, `operator.attrgetter` and `itemgetter`, and stable sorts; Rich: tables, panels, progress bars, `Live`, and recording what's printed |
| **New tool skill** | Rich for debugging: `inspect`, pretty tracebacks, and a handler for `logging` |
| **Time** | 4 to 5 hours |
| **Before you start** | [Project 22](../part-4-web/p22-high-score-server.md). A `making` folder with some projects in it |

## Predict

!!! question "Predict"
    ```python
    import subprocess
    import sys

    done = subprocess.run(
        [sys.executable, "-c", "print('hello'); raise SystemExit(3)"],
        capture_output=True,
        text=True,
    )
    print(repr(done.stdout), done.returncode)
    ```

??? success "Answer"
    ```text
    'hello\n' 3
    ```

    `subprocess.run` starts another program, waits for it to finish, and tells you how it went. The program here is another copy of Python, told to print something, and to stop with an *exit status* of 3. A status of nought means "all went well", and anything else means that it didn't. **`run` doesn't mind.** A program that fails isn't an exception, unless you ask for it to be, which is a pattern that you've met before, with httpx. Stage 1.

!!! question "Predict"
    ```python
    from datetime import timedelta

    gap = timedelta(days=3, minutes=5)
    print(gap.days, gap.seconds, gap.total_seconds())
    ```

??? success "Answer"
    ```text
    3 300 259500.0
    ```

    A `timedelta` is a length of time. It's kept as days, seconds and microseconds, and **`.seconds` is only the seconds part**: the five minutes, and not the three days. It's the most misleading name in the standard library. What you nearly always want is `total_seconds()`. It's the bug hunt. Stage 2.

!!! question "Predict"
    ```python
    from datetime import UTC, datetime

    tokyo = datetime.fromisoformat("2026-09-20T20:00:00+09:00")
    london = datetime(2026, 9, 20, 12, 0, tzinfo=UTC)
    print(london - tokyo, tokyo < london, tokyo.hour, london.hour)
    ```

??? success "Answer"
    ```text
    1:00:00 True 20 12
    ```

    Eight in the evening in Tokyo is *earlier* than noon in London, by an hour. Each of those datetimes knows its time zone, which makes it **aware**, and so Python can compare them, and subtract them, correctly, though the clocks on the wall said 20 and 12. A datetime with no time zone is **naive**, and you can't even subtract one from the other kind: it's a `TypeError`. Stage 2.

!!! question "Predict"
    ```python
    from operator import itemgetter

    rows = [("snake", 31), ("life", 29), ("beeb", 31)]
    print(sorted(rows, key=itemgetter(1), reverse=True))
    print(sorted(sorted(rows), key=itemgetter(1), reverse=True))
    ```

??? success "Answer"
    ```text
    [('snake', 31), ('beeb', 31), ('life', 29)]
    [('beeb', 31), ('snake', 31), ('life', 29)]
    ```

    `itemgetter(1)` is a function that returns item 1 of whatever it's given, and so it's a ready-made sort key. Snake and Beeb are level on 31. Which comes first? Whichever came first *before* the sort: Python's sort is **stable**, which means that things that tie are left in the order that they arrived in. So to sort by score, and by name where the scores are equal, sort by name first, and then by score. Stage 4.

## Build

```console
$ cd making
$ uv init dashboard
$ cd dashboard
$ uv add rich
$ uv add --dev pytest ruff pyright
$ code .
```

Add the `[tool.pyright]` table from Project 17, with `strict`.

### Stage 1: Asking Git

Git knows everything that you want to know, and the way to ask it is to run it. **`subprocess`** is how one program runs another. Create `src/dashboard/git.py`:

<!-- listing: projects/23-rich-dashboard/src/dashboard/git.py -->
```python title="src/dashboard/git.py"
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
```

`run_git` is the only function in the project that starts another program, and everything about doing that properly is in it.

**The command is a list**, with one string for each argument, exactly as the other program will receive them: `["git", "-C", "/home/ada/making/snake", "log"]`. There's no shell in between. Spaces in a folder's name need no quotation marks, and a folder called `; rm -rf ~` is a folder with an odd name, and not an instruction.

!!! warning "Gotcha"
    You'll see `subprocess.run("git log " + folder, shell=True)` in old code, and in a good many answers on the web. That hands a *string* to the shell, which will act on any `;`, `|`, `$` or backquote that it finds in it. It's the third appearance in this tutorial of the same mistake: **data, pasted into code, as a string**. It was HTML in Project 18, and SQL in Project 20. Give `run` a list, and never say `shell=True` with anything in the string that you didn't write yourself.

**`capture_output=True`** collects what the program prints, where otherwise it would go straight to your terminal. There are two streams, as there have been since the 1970s: `stdout`, for results, and `stderr`, for complaints. **`text=True`** gives you strings, and not bytes. Say the `encoding` too, as you would for a file.

**`check=True`** is the switch that the first Predict was about. With it, an exit status other than nought raises `CalledProcessError`, which carries the status and both streams. `run_git` turns that into a `GitError`, with Git's own words as the message.

**`timeout=30`** is for the reason that every network call had one, in Project 20. A program that you've started can hang, and then so do you.

**`shutil.which("git")`** looks along the `PATH` for a program, as the shell does, and returns `None` if it isn't there. It makes for a kinder message than the `FileNotFoundError` that `run` would raise.

The other functions are questions for Git, asked in ways that were *designed* to be read by programs. `--format=%aI` prints nothing about each commit but its author's date, in the ISO 8601 form, with a time zone. `status --porcelain` is a terse format that's promised never to change. When you're going to parse a program's output, look in its manual for the option that's meant for it. It'll nearly always be there.

`git -C folder` means "as if I'd started you in that folder", and `-- .` on the end of a `log` means "only the commits that touched this folder". So it doesn't matter whether each of your projects is a repository of its own, or whether they all share one. (The tutorial's own are in one repository, and the dashboard works on them.)

### Stage 2: Dates and times

The standard library's `datetime` module has four types that matter.

| | | |
|---|---|---|
| `date` | a day | `date(2026, 9, 20)` |
| `time` | a time of day | rarely used by itself |
| `datetime` | a day and a time: a moment | `datetime(2026, 9, 20, 12, 0, tzinfo=UTC)` |
| `timedelta` | a length of time | `timedelta(days=3, minutes=5)` |

They do arithmetic, as you'd hope. A `datetime` minus a `datetime` is a `timedelta`. A `datetime` plus a `timedelta` is a `datetime`. A `timedelta` divided by a `timedelta` is a number.

**Naive and aware.** A `datetime` may carry a time zone, or not. The third Predict showed why it matters: "20:00" is nothing like enough to say *when* something happened. Your commits have their time zones with them, and a laptop travels. The rule is short, and it'll save you from a whole family of bugs:

- **Every datetime in a program should be aware.** `datetime.now(UTC)` is the present moment, and it's aware. A plain `datetime.now()` is naive, and Ruff's DTZ rules will object to it, as they did in Project 19.
- **Work in UTC, and convert at the edges**, for showing to people: `moment.astimezone()` converts to the time zone of the machine that it's running on.
- **Exchange them as ISO 8601 text**, with the offset on the end: `2026-09-20T20:00:00+09:00`. `datetime.fromisoformat` reads it, and `.isoformat()` writes it. It was designed so that sorting the text sorts the times.

Create `src/dashboard/when.py`:

<!-- listing: projects/23-rich-dashboard/src/dashboard/when.py -->
```python title="src/dashboard/when.py"
"""Dates and times, as people like to read them."""

from collections import Counter
from datetime import datetime, timedelta

BLOCKS = " ▁▂▃▄▅▆▇█"


def ago(then: datetime, now: datetime) -> str:
    """Say how long ago something happened, roughly, as a person would."""
    seconds = (now - then).total_seconds()
    if seconds < 0:
        return "in the future"
    for size, name in [(86400 * 365, "year"), (86400 * 30, "month"), (86400 * 7, "week"),
                       (86400, "day"), (3600, "hour"), (60, "minute")]:  # fmt: skip
        count = int(seconds // size)
        if count >= 1:
            return f"{count} {name}{'s' if count > 1 else ''} ago"
    return "just now"


def weekly(times: list[datetime], now: datetime, weeks: int) -> list[int]:
    """Count the commits in each of the last so-many weeks, oldest first."""
    counts = Counter((now - time) // timedelta(weeks=1) for time in times)
    return [counts[back] for back in reversed(range(weeks))]


def sparkline(counts: list[int]) -> str:
    """Draw some numbers as a row of little bars: ▁▂▃▄▅▆▇█."""
    tallest = max(counts, default=0)
    if tallest == 0:
        return " " * len(counts)
    return "".join(BLOCKS[-(-count * 8 // tallest)] for count in counts)
```

**`ago`** takes `now` as a parameter, and doesn't look at the clock itself. That's Project 9's rule, which made `random` a parameter: a function that reads the clock gives a different answer every time that it's tested. It uses `total_seconds()`, from the second Predict, and then tries each unit, from the biggest downwards.

**`weekly`** has a pretty piece of arithmetic in it. `(now - time) // timedelta(weeks=1)` is "how many *whole* weeks ago was that?", as an `int`: floor division works on lengths of time. A `Counter` of those numbers is the number of commits in each week, and a `Counter` answers nought, without complaint, for a week with none.

**`sparkline`** draws a list of numbers with the eight block characters, `▁▂▃▄▅▆▇█`, which makes a bar chart in the space of a word. `-(-count * 8 // tallest)` is Project 19's trick for rounding up, so that a week with a single commit shows *something*.

```pycon
>>> from datetime import UTC, datetime, timedelta
>>> from dashboard.when import ago, sparkline, weekly
>>> now = datetime(2026, 9, 20, 12, 0, tzinfo=UTC)
>>> ago(now - timedelta(days=3, minutes=5), now)
'3 days ago'
>>> f"{now:%A %d %B %Y, at %H:%M}"
'Sunday 20 September 2026, at 12:00'
>>> times = [now - timedelta(days=days) for days in (0, 1, 1, 2, 9, 30)]
>>> weekly(times, now, 6)
[0, 1, 0, 0, 1, 4]
>>> sparkline(weekly(times, now, 6))
' ▂  ▂█'
```

A datetime in an f-string takes a format of its own, after the colon: `%A` is the day's name, `%d` the day of the month, `%B` the month's name, `%H:%M` the time. The [table of them all](https://docs.python.org/3/library/datetime.html#format-codes) is one to bookmark, since nobody remembers it.

!!! note "Under the bonnet"
    `UTC` is a fixed offset, of nought. "Europe/London" isn't: it's an hour ahead in the summer, and it has a history. For real places, there's `zoneinfo`, in the standard library: `datetime.now(ZoneInfo("Europe/London"))`. The rules come from a database that's kept up to date by volunteers, since governments do change them, sometimes at a few weeks' notice. It's a good reason to keep your own arithmetic in UTC.

!!! success "Checkpoint"
    Test `when.py`, which is all pure functions, and commit both.

    ```console
    $ git add .
    $ git commit -m "Ask Git for a project's history, and say when things happened"
    ```

### Stage 3: What's worth knowing about a project

Create `src/dashboard/stats.py`:

<!-- listing: projects/23-rich-dashboard/src/dashboard/stats.py -->
```python title="src/dashboard/stats.py"
"""What there is to know about one project, and how to find it out."""

import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from dashboard import git

SKIP = {".venv", ".git", "__pycache__", "build", "dist", "site", "node_modules"}
TEST = re.compile(r"^\s*(?:async\s+)?def test_", re.MULTILINE)


@dataclass
class Project:
    name: str
    path: Path
    commits: list[datetime] = field(default_factory=list[datetime])
    branch: str = ""
    changed: int = 0
    lines: int = 0
    tests: int = 0

    @property
    def latest(self) -> datetime | None:
        return max(self.commits, default=None)

    @property
    def days_worked(self) -> int:
        """On how many different days was something committed?"""
        return len({commit.date() for commit in self.commits})


def python_files(folder: Path) -> list[Path]:
    """Return the project's own Python files, and not the ones it has installed."""
    return [
        path
        for path in folder.rglob("*.py")
        if not SKIP & set(path.relative_to(folder).parts)
    ]


def measure(folder: Path) -> tuple[int, int]:
    """Count the lines of Python in a folder that aren't blank, and the tests."""
    lines = tests = 0
    for path in python_files(folder):
        text = path.read_text(encoding="utf-8", errors="replace")
        lines += sum(1 for line in text.splitlines() if line.strip())
        tests += len(TEST.findall(text))
    return lines, tests


def scan(folder: Path) -> Project:
    """Find out everything about one project."""
    lines, tests = measure(folder)
    project = Project(folder.name, folder, lines=lines, tests=tests)
    if git.is_tracked(folder):
        project.commits = git.commit_times(folder)
        project.branch = git.branch(folder)
        project.changed = git.changed_files(folder)
    return project


def find_projects(root: Path) -> list[Path]:
    """Return the folders in `root` that look like Python projects, in order of name."""
    return sorted(
        folder
        for folder in root.iterdir()
        if folder.is_dir() and (folder / "pyproject.toml").is_file()
    )


def busiest_day(projects: list[Project]) -> str:
    """On which day of the week is the most work done?"""
    days = Counter(f"{commit:%A}" for project in projects for commit in project.commits)
    if not days:
        return "no day yet"
    (day, count), *_ = days.most_common(1)
    return f"{day}, with {count} commits"
```

**`python_files`** uses `rglob`, from Project 19, which finds files in a folder and in every folder inside it. The catch is `.venv`, which has thousands of Python files in it that aren't yours. `path.relative_to(folder).parts` is the pieces of a path, as a tuple, and `SKIP & set(…)` is the intersection of two sets, from Project 4: if any part of the path is a folder to be skipped, the intersection isn't empty, and the file is left out.

**`TEST`** counts tests with a regular expression. `re.MULTILINE` makes `^` match at the start of *every line*, and not only at the start of the text. It counts `async def test_…` too, which you'll be writing in Project 25.

**`days_worked`** is a set comprehension. `commit.date()` throws away the time, and a set throws away the duplicates, and so its length is the number of different days.

**`busiest_day`** is a `Counter` again, fed by a generator with two `for`s in it. `most_common(1)` returns a list of one pair, and `(day, count), *_ = …` takes it apart.

`Counter` has a cousin, which you haven't met, for when you're collecting things and not counting them. A **`defaultdict`** is a dictionary that makes a value for any key that it hasn't seen, by calling the function that you gave it:

```pycon
>>> from collections import defaultdict
>>> by_score = defaultdict(list)
>>> for name, score in [("snake", 31), ("life", 29), ("beeb", 31)]:
...     by_score[score].append(name)
>>> dict(by_score)
{31: ['snake', 'beeb'], 29: ['life']}
```

Without it, you'd write `if score not in by_score: by_score[score] = []`, every time. A `Counter` is more or less a `defaultdict(int)`, with some extras. One of the challenges wants one.

### Stage 4: Sorting by anything

`sorted`, `list.sort`, `min` and `max` all take a **`key`**: a function that's called once for each item, and returns *what to sort it by*. You've written them as lambdas since Project 3. Create `src/dashboard/view.py`, and look at the top of it first:

<!-- listing: projects/23-rich-dashboard/src/dashboard/view.py -->
```python title="src/dashboard/view.py"
"""Showing it all, with Rich."""

from collections.abc import Callable
from datetime import datetime
from operator import attrgetter

from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from dashboard.stats import Project, busiest_day
from dashboard.when import ago, sparkline, weekly


def newest_first(project: Project) -> float:
    """A sort key: the time of the latest commit, as a number, or 0 if there isn't one."""
    return -project.latest.timestamp() if project.latest else 0.0


# Each way of sorting is a function that takes a project and returns what to sort by.
SORTS: dict[str, Callable[[Project], str | float]] = {
    "name": attrgetter("name"),
    "recent": newest_first,
    "commits": lambda project: -len(project.commits),
    "lines": lambda project: -project.lines,
    "tests": lambda project: -project.tests,
}
```

**`SORTS` is a dictionary of functions**, from the name of an order to the key that produces it. The command line will offer `sorted(SORTS)` as its choices, and the table will say `sorted(projects, key=SORTS[order])`. To add a way of sorting, you add a line here, and nothing else changes. It's the registry idea again, from Projects 16 and 17, without the decorators.

**`attrgetter("name")`**, from the `operator` module, is a function that returns the `name` attribute of whatever it's given. It's `lambda project: project.name`, spelt in a way that says what it's for. `itemgetter(1)`, in the fourth Predict, is its twin, for `thing[1]`. Both take several names, and then return a tuple, which is how you sort on two things at once: `attrgetter("branch", "name")`.

**Descending order** can be had in two ways. `reverse=True` reverses the whole sort. Here, each key returns a *negative* number, so that the biggest comes first, and then every order can go through the same `sorted` call. That only works for numbers: there's no such thing as minus a string.

**Things that might be missing** need care. A project with no commits has no latest commit, and `None` can't be compared with a datetime. `newest_first` gives such a project a key of 0, which sorts after every negative timestamp, and so it goes to the bottom.

And remember the fourth Predict: **the sort is stable**. `find_projects` hands the projects over in order of name, and so, in every other order, the ones that tie are in order of name. That's free.

### Stage 5: Rich

Here's the rest of `view.py`:

<!-- listing: projects/23-rich-dashboard/src/dashboard/view.py -->
```python title="src/dashboard/view.py"
def table(projects: list[Project], now: datetime, order: str, weeks: int) -> Table:
    grid = Table(title=f"Sorted by {order}", title_justify="left", expand=True)
    grid.add_column("Project", style="bold cyan", no_wrap=True)
    grid.add_column("Branch")
    grid.add_column("Commits", justify="right")
    grid.add_column("Last commit")
    grid.add_column("Lines", justify="right")
    grid.add_column("Tests", justify="right")
    grid.add_column(f"Last {weeks} weeks", style="green", no_wrap=True)

    for project in sorted(projects, key=SORTS[order]):
        branch = Text(project.branch or "not in Git", style="dim")
        if project.changed:
            branch = Text(f"{project.branch} +{project.changed}", style="yellow")
        grid.add_row(
            Text(project.name),  # a Text is never read as markup, whatever it's called
            branch,
            f"{len(project.commits):,}",
            ago(project.latest, now) if project.latest else "never",
            f"{project.lines:,}",
            f"{project.tests:,}",
            sparkline(weekly(project.commits, now, weeks)),
        )

    grid.add_section()
    grid.add_row(
        f"{len(projects)} projects",
        "",
        f"{sum(len(project.commits) for project in projects):,}",
        "",
        f"{sum(project.lines for project in projects):,}",
        f"{sum(project.tests for project in projects):,}",
        "",
        style="bold",
    )
    return grid


def dashboard(
    projects: list[Project], now: datetime, order: str = "name", weeks: int = 12
) -> RenderableType:
    """Return the whole display, ready for a console to print."""
    days = sum(project.days_worked for project in projects)
    summary = Text.assemble(
        "Your busiest day is ",
        (busiest_day(projects), "bold magenta"),
        f". {days} project-days of work so far.",
    )
    return Group(
        Panel(summary, title="Learn Python by making"),
        table(projects, now, order, weeks),
    )
```

In Project 4 you gave Rich strings with markup in them. Its real strength is that it has **objects for things that can be shown**, which it calls *renderables*, and which fit inside one another.

- A **`Table`** has columns, each with a style and a justification, and rows. `expand=True` makes it as wide as the terminal, and Rich works out the widths of the columns, wraps what doesn't fit, and draws the lines. `add_section` rules a line off before the totals.
- A **`Text`** is a string with styles attached to parts of it. `Text.assemble` builds one from pieces, each of which is a plain string, or a pair of a string and a style. It's the safe way of showing text that you didn't write. Rich reads a plain string as markup, and so a project whose folder was called `[bold]` would vanish from the table, and that's why the name goes in as a `Text`. (There's that mistake again.)
- A **`Panel`** puts a border round another renderable, with a title.
- A **`Group`** is several renderables, one above another, as a single thing.

`dashboard` *returns* the display, and doesn't print it. That's your old rule, of keeping the working-out apart from the showing, and it pays twice in the next file.

`f"{project.lines:,}"` puts commas into a number, and so does the `:,` in every other cell.

Create `src/dashboard/cli.py`:

<!-- listing: projects/23-rich-dashboard/src/dashboard/cli.py -->
```python title="src/dashboard/cli.py"
"""How your projects are getting on: a dashboard in the terminal."""

import argparse
import time
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console, RenderableType
from rich.live import Live
from rich.progress import track

from dashboard.stats import find_projects, scan
from dashboard.view import SORTS, dashboard


def build(
    root: Path, order: str, weeks: int, console: Console | None
) -> RenderableType:
    """Scan every project under a folder, and return the display."""
    folders = find_projects(root)
    if console is not None:
        folders = track(
            folders, description="Scanning", console=console, transient=True
        )
    projects = [scan(folder) for folder in folders]
    return dashboard(projects, datetime.now(UTC), order, weeks)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--sort", choices=sorted(SORTS), default="name")
    parser.add_argument("--weeks", type=int, default=12)
    parser.add_argument("--watch", type=float, metavar="SECONDS", help="keep looking")
    args = parser.parse_args()

    console = Console()
    if not args.watch:
        console.print(build(args.root, args.sort, args.weeks, console))
        return

    with Live(build(args.root, args.sort, args.weeks, None), console=console) as live:
        try:
            while True:
                time.sleep(args.watch)
                live.update(build(args.root, args.sort, args.weeks, None))
        except KeyboardInterrupt:
            pass
```

Set the command in `pyproject.toml` to `dashboard = "dashboard.cli:main"`.

**`track`** wraps anything that you can loop over, and shows a progress bar while you do. `transient=True` makes it vanish when it's finished. It matters here: there are four runs of Git for every project, and twenty-six projects took 1.7 seconds on the machine that this was written on, which is long enough to wonder whether anything is happening.

**`Live`** is a display that *redraws itself in place*. It's a context manager. Inside the `with`, `live.update(…)` swaps what's showing for something new, with no flicker, and no scrolling. With `--watch 5`, the dashboard looks again every five seconds. Leave it running in a corner, commit something in another terminal, and watch the count go up.

!!! example "Run it"
    ```console
    $ uv run dashboard ..
    $ uv run dashboard .. --sort recent
    $ uv run dashboard .. --sort lines --weeks 26
    $ uv run dashboard .. --watch 5
    ```

    Make the terminal narrower, and run it again. Try `--sort banana`, and see what `argparse` makes of it.

    That's your own work, measured. Have a good look at it.

#### Testing what's shown

A `Console` can be told to **record** what it prints, and to give it back as plain text. `tests/test_view.py`:

<!-- listing: projects/23-rich-dashboard/tests/test_view.py -->
```python title="tests/test_view.py"
def project(name: str, days_ago: list[int], lines: int, tests: int) -> Project:
    commits = [NOW - timedelta(days=days) for days in days_ago]
    return Project(name, Path(name), commits, "main", 0, lines, tests)


PROJECTS = [
    project("snake", [1, 2, 3], lines=800, tests=31),
    project("asteroids", [40], lines=900, tests=12),
    project("hi-lo", [], lines=200, tests=0),
]


def shown(order: str) -> str:
    console = Console(record=True, width=120)
    console.print(dashboard(PROJECTS, NOW, order, weeks=8))
    return console.export_text()
# ...
def test_what_is_on_the_screen():
    text = shown("name")
    assert "Sorted by name" in text
    assert "1 day ago" in text
    assert "never" in text
    assert "3 projects" in text
    assert "1,900" in text
    assert text.index("asteroids") < text.index("hi-lo") < text.index("snake")
```

A recording console can also `export_svg()`, which is a picture of a terminal window, and that's how the one at the top of this chapter was made. No screenshot was taken.

#### Testing with real repositories

`git.py` runs a real program, and the honest way to test it is against a real repository. `tmp_path` makes that cheap. `tests/conftest.py`:

<!-- listing: projects/23-rich-dashboard/tests/conftest.py -->
```python title="tests/conftest.py"
import os
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

type Commit = tuple[
    str, str
]  # a file's name, and the date, as 2026-03-02T10:00:00+00:00


def git(folder: Path, *arguments: str, when: str = "2026-01-01T00:00:00+00:00") -> None:
    """Run git as a made-up person, at a made-up time, so that tests are repeatable."""
    identity = {
        "GIT_AUTHOR_NAME": "A. Reader",
        "GIT_AUTHOR_EMAIL": "reader@example.com",
        "GIT_AUTHOR_DATE": when,
        "GIT_COMMITTER_NAME": "A. Reader",
        "GIT_COMMITTER_EMAIL": "reader@example.com",
        "GIT_COMMITTER_DATE": when,
    }
    subprocess.run(
        ["git", "-c", "commit.gpgsign=false", *arguments],
        cwd=folder,
        env=os.environ | identity,
        check=True,
        capture_output=True,
    )


@pytest.fixture
def make_project(tmp_path: Path) -> Callable[[str, list[Commit]], Path]:
    """Return a function that makes a project, with a history, in a folder of its own."""

    def make(name: str, commits: list[Commit]) -> Path:
        folder = tmp_path / name
        folder.mkdir()
        (folder / "pyproject.toml").write_text(f'[project]\nname = "{name}"\n')
        git(folder, "init", "--quiet", "--initial-branch=main")
        for file_name, when in commits:
            (folder / file_name).write_text(f"# written at {when}\n", encoding="utf-8")
            git(folder, "add", ".", when=when)
            git(folder, "commit", "--quiet", "-m", f"Add {file_name}", when=when)
        return folder

    return make
```

**`make_project` is a fixture that returns a function.** A fixture normally hands a test a *thing*. Some tests want several things, each a little different, and then the fixture can hand over the means of making them. It's called a *factory fixture*, and it's a closure, from Project 7: `make` remembers `tmp_path`.

Git takes the date of a commit from two environment variables, if they're set, and `env=os.environ | identity` passes the present environment on, with those added. So every test's history is the same, to the second, whenever it's run. `tests/test_git.py`:

<!-- listing: projects/23-rich-dashboard/tests/test_git.py -->
```python title="tests/test_git.py"
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
# ...
def test_a_plain_folder_is_not_tracked(tmp_path):
    assert not git.is_tracked(tmp_path)
    with pytest.raises(git.GitError, match="not a git repository"):
        git.commit_times(tmp_path)


def test_git_missing_altogether(tmp_path, monkeypatch):
    monkeypatch.setattr("shutil.which", lambda name: None)
    with pytest.raises(git.GitError, match="no git on this machine"):
        git.run_git(tmp_path, "status")
```

The second commit was made at half past eleven at night, in India. It comes back with its offset intact, and it's *equal* to six in the evening, UTC, since they're the same moment. The last test removes Git from the machine, as far as `shutil.which` is concerned, with `monkeypatch`.

!!! success "Checkpoint"
    ```console
    $ uv run pyright
    $ git add .
    $ git commit -m "Add the dashboard: a table, a panel, five ways of sorting, and --watch"
    $ git push
    ```

### Stage 6: Rich, for finding things out

Rich is as useful for debugging as it is for display. Three things are worth knowing about.

**`inspect`** shows you what an object is, and what's in it:

<!-- no-doctest -->
```pycon
>>> from rich import inspect
>>> inspect(timedelta(days=3, minutes=5))
╭──────────────────────── <class 'datetime.timedelta'> ────────────────────────╮
│ Difference between two datetime values.                                      │
│                                                                              │
│ ╭──────────────────────────────────────────────────────────────────────────╮ │
│ │ datetime.timedelta(days=3, seconds=300)                                  │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
│                                                                              │
│         days = 3                                                             │
│ microseconds = 0                                                             │
│      seconds = 300                                                           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

That would have settled the second Predict at a glance. `inspect(thing, methods=True)` lists the methods too, each with the first line of its docstring. It's `dir` and `help`, in a form that you can read.

**Pretty tracebacks.** Two lines at the top of a program make every uncaught exception come out with colour, with the source code round each line, and, if you ask, the local variables at each level:

```python
from rich.traceback import install

install(show_locals=True)
```

**A handler for `logging`.** Project 15's logging can be sent through Rich, which lines it up in columns, colours the levels, and highlights numbers and paths:

```python
import logging

from rich.logging import RichHandler

logging.basicConfig(level="INFO", format="%(message)s", handlers=[RichHandler()])
```

And `uv run python -m rich` shows off everything that the library can do.

## Type-in listing

When do you really work? Here's a chart of one repository's commits, by the hour of the day, in twenty-three lines, with no Rich at all. Save it as `busy.py`, and run it inside any project: `uv run ../dashboard/busy.py`.

<!-- listing: projects/23-rich-dashboard/busy.py -->
```python title="busy.py" linenums="1"
"""When do you work? A chart of this repository's commits, by the hour of the day."""

import subprocess
from collections import Counter
from datetime import datetime

printed = subprocess.run(
    ["git", "log", "--format=%aI"], capture_output=True, text=True, check=True
).stdout
times = [datetime.fromisoformat(line) for line in printed.splitlines()]
hours = Counter(time.hour for time in times)
days = Counter(f"{time:%a}" for time in times)

tallest = max(hours.values(), default=1)
for hour in range(24):
    bar = "█" * round(40 * hours[hour] / tallest)
    print(f"{hour:02}:00 {bar} {hours[hour] or ''}")

print()
print("  ".join(f"{day} {count}" for day, count in days.most_common()))
if times:
    span = max(times) - min(times)
    print(f"{len(times)} commits in {span.days + 1} days, since {min(times):%d %B %Y}")
```

1. What would happen if this were run in a folder that isn't a repository? Which argument decides, and what would you see?
2. `time.hour` is the hour *on the committer's own clock*. If you'd made half of your commits on holiday in Tokyo, would you want them at the hour that it was there, or the hour that it was at home? How would you get the other?
3. Lines 16 and 17 ask the `Counter` about hours in which there were no commits. Why doesn't that raise a `KeyError`? What does `hours[hour] or ''` do?
4. `days.most_common()` gives the days in order of how busy they were. How would you show them from Monday to Sunday?
5. Why `span.days + 1`?

## Bug hunt

A colleague wrote their own `ago`. "Something's wrong with my old projects," they say. "They all look as if I'd worked on them this morning." It's in the tutorial's repository, as `projects/23-rich-dashboard/bughunt/stale.py`.

```console
$ uv run bughunt/stale.py
             0:05:00  ->  5 minutes ago
             3:00:00  ->  3 hours ago
     2 days, 6:00:00  ->  2 days ago
     3 days, 0:05:00  ->  5 minutes ago
   400 days, 0:00:10  ->  just now
```

1. **Reproduce it.** Three of the five are right. What do the wrong ones have in common?
2. **Write a failing test**, with a table of gaps and what each ought to say. Which gaps would you choose, now that you know?
3. **Fix it.**

??? success "Solution"
    The function says `gap.seconds`, and that was the second Predict. A `timedelta` of 3 days and 5 minutes has a `.days` of 3, and a `.seconds` of **300**. The first test, `gap.seconds < 3600`, passes, and the days are never looked at. 400 days and 10 seconds is "just now".

    It's right for anything under a day, since then the seconds are all that there is. It's right, by luck, for 2 days and 6 hours, since 6 hours of seconds is too many for the first two tests, and the third, `gap.days < 1`, fails properly. It's wrong for any gap of more than a day whose *odd part* is under an hour. So it works in a quick try, and goes wrong for a fraction of your projects, differently each day. That's the nastiest kind of bug.

    The fix is `gap.total_seconds()`, once, at the top, and then to work from that number alone.

    ```python
    @pytest.mark.parametrize(
        ("gap", "words"),
        [
            (timedelta(days=3, minutes=5), "3 days ago"),
            (timedelta(days=400, seconds=10), "1 year ago"),
            (timedelta(days=2, hours=6), "2 days ago"),
        ],
    )
    def test_the_days_count_for_something(gap, words):
        assert ago(NOW - gap, NOW) == words
    ```

    **What to take from it.** Test the *boundaries*, and test values that are made of more than one part. "5 minutes" and "3 hours" are the cases that anybody would think of, and they pass. "3 days and 5 minutes" is the case that finds the bug, and it comes from asking: *what are the pieces of this value, and have I tried one where several of them matter at once?*

## Challenges

Make a branch for each, and merge it with a pull request.

**Tweak**

1. Add a column for the number of days on which each project was worked on. `Project` already knows.
2. Add `--sort days`, and `--sort changed`, which puts the projects with uncommitted work at the top. How many lines was that?
3. Colour the "last commit" cell: green if it was this week, yellow if this month, and dim otherwise. A cell can be a `Text`.

**Extend**

1. **Streaks.** For how many days in a row have you committed something, across all projects? What was your longest run? You'll want a set of dates, and `timedelta(days=1)`. Mind the ends of months, which `date` arithmetic gets right for you, and *which* day a commit at five to midnight belongs to.
2. **A timeline.** Under the table, list the months, with the projects that were worked on in each: `March: hi-lo, dice-lab, codebreaker`. That's a `defaultdict(set)`, keyed by `f"{commit:%Y-%m}"`, which sorts correctly as text.
3. **Faster.** Most of the 1.7 seconds is spent waiting for Git, a hundred times over, one after another. The projects don't depend on each other. `concurrent.futures.ThreadPoolExecutor` has a `map` that's used exactly as the built-in one is, and runs several at once. Measure it before and after. Project 25 explains why it works.
4. **A heat map.** GitHub shows a year of commits as a grid of little squares, a column to a week and a row to a day, with darker greens for busier days. Draw yours, with Rich. `Text` can be styled a character at a time, and `on green` is a background.

??? tip "Hint for streaks"
    Make a set of the dates. A date *starts* a streak if the day before it isn't in the set. From each start, count forward until you fall out of the set.

**Invent**

1. **GitHub too.** `gh api repos/{owner}/{repo}` returns JSON about a repository: its stars, its open issues, whether the last workflow passed. `gh` deals with logging in, and you only have to run it and parse what comes back. Add a column that shows whether each project's CI is green.
2. **Your year, in review.** A one-page summary for the end of the tutorial: the totals, the longest streak, the biggest day, your most-used words in commit messages, and the hour at which you do your best work. Export it as an SVG, and put it in your profile.

A solution to the first Extend, and the bug hunt's tests, are in the project's `solutions/` folder.

## Recap

You can now:

- [x] run another program with `subprocess.run`, safely, with a list, a time-out and `check=True`, and read its output and its exit status
- [x] say why `shell=True` is the same mistake as SQL injection
- [x] find a program's machine-readable output, such as `--porcelain` and `--format`
- [x] use `date`, `datetime` and `timedelta`, and do arithmetic with them
- [x] keep every datetime aware, work in UTC, and exchange times as ISO 8601
- [x] use `total_seconds()`, and know what `.seconds` really is
- [x] format dates in f-strings
- [x] pass the clock in as a parameter, so that code about time can be tested
- [x] count with `Counter`, and collect with `defaultdict`
- [x] sort by any key, with lambdas, `attrgetter` and `itemgetter`, and use the stability of the sort for ties
- [x] build a display from Rich's tables, panels, texts and groups, show progress with `track`, and update in place with `Live`
- [x] test terminal output by recording it, and export it as an SVG
- [x] write a factory fixture, and test against real, repeatable Git repositories
- [x] use `rich.inspect`, Rich's tracebacks and its logging handler

**Read more:** [`subprocess`](https://docs.python.org/3/library/subprocess.html) · [`datetime`](https://docs.python.org/3/library/datetime.html), and [`zoneinfo`](https://docs.python.org/3/library/zoneinfo.html) · [The sorting HOWTO](https://docs.python.org/3/howto/sorting.html), which is short and excellent · [`collections`](https://docs.python.org/3/library/collections.html) · [Rich's documentation](https://rich.readthedocs.io/) · [Falsehoods programmers believe about time](https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time), which is funny, and then alarming

Rich draws things, and then it's finished. It can't take a click, or a key, or keep several parts of the screen alive at once. For that, the same people wrote **Textual**, which is to the terminal what a web browser's page is to a window: widgets, layout, stylesheets and events. In [Project 24](p24-teletext-viewer.md), PyFax comes to the terminal.
