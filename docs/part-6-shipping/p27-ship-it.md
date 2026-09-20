# Project 27 · Ship It

In 1983, shipping a program meant a twin-deck cassette recorder, a box of C15s, an inlay run off on the school's photocopier, a pile of jiffy bags, and a small ad in the back pages of a magazine, which you paid for by the word.

You have it easier. By the end of this project, anybody in the world who has uv will be able to type one line:

```console
$ uvx --from beeb-yourname beeb
```

and see this, and hear a beep, on a computer that you've never touched, and that has never heard of you.

![Eight vertical bars: black, red, green, yellow, blue, magenta, cyan and white, above a row of short white lines](../assets/p27-testcard.png)

There's no new program in this project. There's an old one, the `beeb` package from Projects 8 and 11, **made ready for strangers**. That's a craft of its own, and it has less to do with code than you might expect. A stranger can't ask you what the package is for, or whether version 0.3 will break their program, or whether they're allowed to use it at work. Everything that they need to know has to travel with the package: in its metadata, its README, its changelog, its licence and its version number. And since you won't be there when it's installed, you have to be sure that what you've shipped is what you tested.

| | |
|---|---|
| **You'll learn** | What a package really is: wheels, sdists and metadata; `pyproject.toml`, field by field; the name you install and the name you import; version numbers in full; honest dependency bounds; READMEs, changelogs and licences; publishing to an index; releases made by a tag; pip and venv, for when you meet them |
| **New tool skills** | pre-commit hooks; CI that tests the oldest of everything, and the wheel itself; trusted publishing |
| **Time** | 4 to 5 hours |
| **Before you start** | [Project 11](../part-2-pygame/p11-sound-and-envelope.md), which left `beeb` at version 0.2.0; [Project 17](../part-3-interpreters/p17-tiny-basic.md), for CI and `uv build`; [Project 22](../part-4-web/p22-high-score-server.md), for semantic versioning, tags and releases |

## Predict

!!! question "Predict"
    ```python
    from packaging.version import Version

    print("1.10.0" > "1.9.0")
    print(Version("1.10.0") > Version("1.9.0"))
    print(Version("1.0") == Version("1.0.0"))
    print(sorted(["1.0.0", "1.0.0rc1", "1.0.0.post1", "1.0.0.dev3", "1.0.0b2", "0.9"], key=Version))
    ```

??? success "Answer"
    ```text
    False
    True
    True
    ['0.9', '1.0.0.dev3', '1.0.0b2', '1.0.0rc1', '1.0.0', '1.0.0.post1']
    ```

    Version numbers aren't strings, and they aren't numbers. As strings, `"1.10.0"` comes *before* `"1.9.0"`, since `"1"` comes before `"9"`, and more than one real project has been bitten by it at its tenth release. **`packaging`** is the library that uv, pip and PyPI all use to read versions, and it's already in your environment, since pytest depends on it. The last line is the whole life of a release, in order: development, beta, release candidate, the release, and a post-release to mend a typing error in the README. Stage 4.

!!! question "Predict"
    ```python
    from packaging.specifiers import SpecifierSet

    versions = ["2.5.2", "2.5.9", "2.6.0", "3.0.0"]
    for spec in [">=2.5.8", "~=2.5.8", "~=2.5", ">=2.5,<3", "==2.5.*"]:
        print(f"{spec:<10}", [v for v in versions if v in SpecifierSet(spec)])
    ```

??? success "Answer"
    ```text
    >=2.5.8    ['2.5.9', '2.6.0', '3.0.0']
    ~=2.5.8    ['2.5.9']
    ~=2.5      ['2.5.2', '2.5.9', '2.6.0']
    >=2.5,<3   ['2.5.2', '2.5.9', '2.6.0']
    ==2.5.*    ['2.5.2', '2.5.9']
    ```

    These are the spellings that go in `dependencies`. `>=` is a floor, and nothing else. **`~=`** is "compatible with": the last number that you give may rise, and the ones before it may not, so `~=2.5.8` means `>=2.5.8, ==2.5.*`, and `~=2.5` means `>=2.5, ==2.*`. A comma means "and". Which of them you *should* write is a matter of honesty, and Stage 3 is about it.

!!! question "Predict"
    ```python
    from importlib.metadata import packages_distributions

    print(packages_distributions()["pygame"])
    ```

??? success "Answer"
    ```text
    ['pygame-ce']
    ```

    You type `import pygame`, and you ran `uv add pygame-ce`. They're different names, for different things. **`pygame` is a package**: a folder of modules, which Python imports. **`pygame-ce` is a distribution**: a thing with a version number, which an index holds and uv installs. Usually the two names agree, and nobody notices that there are two. `importlib.metadata` is how a running program asks about what's installed. Stage 2.

## Build

This project is done in your `beeb` folder, from Project 11, on a branch.

```console
$ cd making/beeb
$ git switch -c ship-it
$ uv add --dev pyright
```

### Stage 1: What's in a wheel?

You built a wheel in Project 17, and installed it, and never looked inside. Look now.

```console
$ uv build
Building source distribution...
Building wheel from source distribution...
Successfully built dist/beeb-0.2.0.tar.gz
Successfully built dist/beeb-0.2.0-py3-none-any.whl
$ uv run python -m zipfile -l dist/beeb-0.2.0-py3-none-any.whl
```

**A wheel is a zip file**, with a different ending. There are two folders in it. One is `beeb/`: your package, exactly as it is in `src/`. The other is `beeb-0.2.0.dist-info/`, and holds four small text files:

| | |
|---|---|
| `METADATA` | everything that's in the `[project]` table, and the whole of your README, in the format of an e-mail's headers, which was the obvious choice in 2001 |
| `WHEEL` | the version of the wheel format, and what made it |
| `entry_points.txt` | your commands: `beeb = beeb:main` |
| `RECORD` | every file, with its size and its hash, so that an installer can check them, and an uninstaller can find them |

**Installing a wheel is unzipping it** into the environment's `site-packages` folder, and writing a small script for each command. Nothing of yours is *run*. That's the point of the format, and it's why installing is so quick, and so safe.

The file's name is a sentence: `beeb-0.2.0-py3-none-any.whl` is *beeb*, version *0.2.0*, for *any Python 3*, needing *no* particular build of the interpreter, on *any* platform. Compare the wheel of pygame-ce that uv chose for the Mac that this was written on: `pygame_ce-2.5.8-cp314-cp314-macosx_10_15_universal2.whl`. On Windows it would have been `…-cp314-cp314-win_amd64.whl`. That package has compiled C in it, and so there's a different wheel for each Python, and each kind of computer. Yours is pure Python, and one wheel serves everybody.

The `.tar.gz` is the **source distribution**, or *sdist*: your `pyproject.toml`, README and `src/`, from which a wheel can be built by anybody who has to. Look in it (`tar tzf`), and notice what *isn't* there: no `tests/`, no `examples/`, no `uv.lock`. Hold on to that.

Who decides what goes in? The **build backend**, which is named in the `[build-system]` table that `uv init` wrote for you in Project 5, and which you've never had reason to read:

```toml
[build-system]
requires = ["uv_build>=0.12.17,<0.13.0"]
build-backend = "uv_build"
```

`uv build`, or pip, or anything else that needs a wheel from your source, reads that table, installs what it `requires`, and calls the backend. `uv_build` is uv's own, and it's quick and strict. Others that you'll meet in other people's projects are `hatchling`, `setuptools`, which is the ancestor of them all, and `maturin`, for packages written partly in Rust. Since they all meet at `pyproject.toml`, you can build anybody's project without knowing which they chose.

### Stage 2: A name of your own

An index holds one project called `beeb`, for ever, and it isn't going to be yours: every reader of this tutorial has one. So the distribution needs a name that nobody else has. Your GitHub name on the end will do: `beeb-yourname`. Look it up on [pypi.org](https://pypi.org) before you grow fond of it.

The *import* name needn't change, and shouldn't, since every program that you've written says `import beeb`. This is the third Predict's distinction, put to use:

```toml
[project]
name = "beeb-yourname"

[tool.uv.build-backend]
module-name = "beeb"
```

Left to itself, `uv_build` would look for a package called `beeb_yourname`. The second table tells it where to look.

Names on an index are compared after being *normalised*: lower case, with every run of `-`, `_` and `.` turned into a single `-`. So `Beeb_Yourname` and `beeb.yourname` are the same project as yours, and can't be registered by anybody else.

!!! warning "Gotcha"
    The reverse is also true, and it's a security problem. Anybody may register `reqeusts`, or `python-dateutils`, and wait for a typing mistake. It's called *typosquatting*, and the packages that do it aren't friendly. **Copy the names of dependencies from their own documentation**, and look twice at the name before you `uv add` something that you've only heard of.

Projects of yours that depend on `beeb` by its path, as Breakout has since Project 11, know it by its old name. In each of them, `uv remove beeb`, and then `uv add --editable ../beeb`, will find the new one. Their code doesn't change at all.

### Stage 3: `pyproject.toml`, field by field

Here's the whole of the `[project]` table, as it's going to be:

<!-- listing: projects/27-ship-it/pyproject.toml -->
```toml title="pyproject.toml"
[project]
name = "beeb-lpbm"
version = "1.0.0"
description = "MOVE, DRAW, PLOT, SOUND and ENVELOPE: BBC Micro-style graphics and sound, on Pygame."
readme = "README.md"
license = "MIT"
license-files = ["LICENSE"]
authors = [{ name = "A. Reader" }]
keywords = ["bbc micro", "retro", "graphics", "sound", "pygame", "education"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Topic :: Multimedia :: Graphics",
    "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
    "Typing :: Typed",
]
requires-python = ">=3.13"
dependencies = ["pygame-ce>=2.5.2"]

[project.urls]
Homepage = "https://github.com/yourname/beeb"
Changelog = "https://github.com/yourname/beeb/blob/main/CHANGELOG.md"
Issues = "https://github.com/yourname/beeb/issues"

[project.scripts]
beeb = "beeb.cli:main"
```

In this chapter's copy, the name ends in `lpbm`, for "Learn Python by Making", and the author is A. Reader. Yours won't.

**`description`** is one line, and it's what's shown in a list of search results. **`readme`** names the file that becomes the project's front page on the index.

**`license`** is an *SPDX expression*: a short, standard name, such as `MIT`, `Apache-2.0` or `GPL-3.0-or-later`, from [a list](https://spdx.org/licenses/) that lawyers and programs both understand. **`license-files`** names the files that hold the words, which travel inside the wheel. Stage 5 is about which to choose.

**`authors`** are names, with e-mail addresses if you wish. Anything that you put here is public for ever, and harvested by spammers within the week. A name is enough.

**`classifiers`** are labels from [a fixed list](https://pypi.org/classifiers/), which the index uses for browsing, and rejects if they're misspelt. Say which Pythons you test on, and that you're `Typing :: Typed`. There's one that's worth knowing for its side effect: a project with the classifier `Private :: Do Not Upload` will be refused by PyPI, which is a cheap insurance against publishing your employer's code by accident.

**`[project.urls]`** become the links in the side bar of the project's page. A few names, such as `Homepage`, `Changelog` and `Issues`, get an icon.

**`requires-python`** is a floor, and only a floor. Never write `<4`, or `<3.15`. You can't know that your package will break on a Python that doesn't exist yet, and installers take you at your word.

#### Honest dependencies

`uv add pygame-ce` wrote `pygame-ce>=2.5.8`, because 2.5.8 was the newest version on that day. It's a guess at a floor, and it's the safest guess that uv could make. For your own programs, it doesn't matter. For a library, it's a claim that you're making to strangers: *this won't work with anything older*. Is that true? A stranger whose project needs pygame-ce 2.5.5, for some reason of their own, is being told that they can't have `beeb`.

You can find out, since uv can be asked to choose **the oldest versions that your bounds allow**, where it would usually choose the newest:

```console
$ uv run --isolated --python 3.13 --resolution lowest-direct pytest
```

`--isolated` does it in a throw-away environment, and leaves your own alone. Lower the floor, run that, and repeat. When this chapter was written, the tests passed with 2.5.2, and 2.5.0 couldn't be installed at all on Python 3.13, since it was released before 3.13 was, and has no wheel for it. So `>=2.5.2` is the true floor, and that's what the listing says. A **bound should be a fact that you've tested**, and not an accident of the day on which you typed `uv add`.

What about a ceiling? `pygame-ce>=2.5.2,<3` looks prudent. For a **library**, it's nearly always a mistake. You don't *know* that 3.0 will break you. If it doesn't, your cap has made `beeb` impossible to install beside anything that needs 3.0, and the only cure is for you to make a new release, for every one of your users to wait for. If it does, you can publish a fix on the day. Caps on libraries cause more breakage than they prevent. (The cap on `uv_build`, in Stage 1, is uv's own advice about its own backend, and a requirement for *building* inconveniences nobody who's installing.)

For an **application**, the reasoning is the other way about, and you have something better than a cap. `uv.lock` pins *every* package, exactly, and it's why `uv sync --locked` builds the same environment in CI as on your desk. Project 24 pinned `textual>=8,<9` as well, and that was reasonable: an app has no dependents to inconvenience, and Textual's API was still moving.

Remember what wasn't in the sdist. **`uv.lock` doesn't ship.** Your users get `Requires-Dist: pygame-ce>=2.5.2`, from `METADATA`, and their installer chooses. The lock file is for you. The bounds are for them.

#### Three kinds of extra

| Table | Who gets them | For |
|---|---|---|
| `[project] dependencies` | everybody who installs the package | what the package can't run without |
| `[project.optional-dependencies]` | whoever asks: `uv add "beeb-yourname[numpy]"` | features that not everybody wants, and their cost. These are called *extras*, and they're published in the metadata |
| `[dependency-groups]` | you, and your CI. They're never published | pytest, ruff, pyright: what's needed to *work on* the package |

Put a thing in the wrong one of those, and you have the commonest packaging bug there is. It's this chapter's bug hunt.

#### Entry points

`[project.scripts]` is one kind of **entry point**: a name, and a function to call. `[project.gui-scripts]` is the same, but on Windows it doesn't open a console window behind your game. And `[project.entry-points."some.group"]` is the general form, which is how plug-ins work. When you installed pytest-asyncio, pytest found it without being told, since pytest-asyncio's metadata has an entry point in the group `pytest11`, and pytest asks `importlib.metadata` for everything in that group. No registry, and no configuration: installing *is* registering.

### Stage 4: One version number

The version is in `pyproject.toml`. A program that wants to say `--version` needs it too, and **two copies of a fact will disagree by the third release**. So ask the installed package. At the top of `src/beeb/__init__.py`:

<!-- listing: projects/27-ship-it/src/beeb/__init__.py -->
```python title="src/beeb/__init__.py"
from importlib.metadata import version
# ...
# The one true version number is in pyproject.toml. This asks the installed package for it.
__version__ = version("beeb-lpbm")
```

It asks by the *distribution's* name, since that's what has a version. Add `"__version__"` to `__all__`.

The test card moves out of `__init__.py`, into a module of its own, where it gains an argument parser. Create `src/beeb/cli.py`, and point `[project.scripts]` at `beeb.cli:main`:

<!-- listing: projects/27-ship-it/src/beeb/cli.py -->
```python title="src/beeb/cli.py"
"""The `beeb` command: a test card. Eight bars and a beep mean that everything works."""

import argparse

from beeb import HEIGHT, WIDTH, __version__, draw, gcol, mode, move, plot, sound, vsync


def block(left: int, bottom: int, right: int, top: int) -> None:
    """Fill a rectangle the way BBC programs did: as two triangles."""
    move(left, bottom)
    move(right, bottom)
    plot(85, left, top)
    plot(85, right, top)


def test_card() -> None:
    mode(2)
    bar = WIDTH // 8
    for colour in range(8):
        gcol(0, colour)
        block(colour * bar, 128, (colour + 1) * bar - 1, HEIGHT - 1)

    gcol(0, 7)
    for x in range(0, WIDTH, 64):
        move(x, 0)
        draw(x, 96)


def main() -> None:
    parser = argparse.ArgumentParser(prog="beeb", description=__doc__)
    parser.add_argument("--version", action="version", version=f"beeb {__version__}")
    parser.parse_args()

    test_card()
    sound(1, -12, 101, 6)
    while True:
        vsync()
```

`action="version"` is argparse's own: it prints, and exits.

`tests/test_cli.py`:

<!-- listing: projects/27-ship-it/tests/test_cli.py -->
```python title="tests/test_cli.py"
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
```

And to change it, there's a command, which edits `pyproject.toml`, and brings the lock file and the environment into step:

```console
$ uv version
beeb-yourname 0.2.0
$ uv version --bump minor --dry-run
beeb-yourname 0.2.0 => 0.3.0
$ uv version --bump major
beeb-yourname 0.2.0 => 1.0.0
```

#### Version numbers, in full

Project 22 gave you semantic versioning: **major** for a change that breaks your users' programs, **minor** for something new, **patch** for a fix. Python's own rules, in a document called PEP 440, agree, and add what comes before and after a release. That was the first Predict:

| | | |
|---|---|---|
| `1.1.0.dev0` | development | "on the way to 1.1.0". `uv version --bump minor --bump dev` |
| `1.1.0a1`, `1.1.0b2` | alpha, beta | "try it, and expect changes" |
| `1.1.0rc1` | release candidate | "this is 1.1.0, unless you find something" |
| `1.1.0` | final | |
| `1.1.0.post1` | post-release | "the same code. The README had a mistake in it" |

An installer never chooses a pre-release, unless it's asked to: `uv add "beeb-yourname>=1.1.0rc1"`, or `--prerelease allow`. So you can put a release candidate in front of the brave, without troubling the cautious.

**What does 1.0.0 mean?** Less than people fear, and more than they think. It says nothing about quality, or completeness. It's a **promise**: from here on, the first number changes if, and only if, your users' programs might break. Below 1.0.0, by convention, anything may change at any time, and nobody can rely on you. `beeb` has been used by six of your projects, and its interface hasn't changed since Project 11. It's ready to promise.

A promise needs to say *what about*. For a library, it's **the public interface**, and Python's convention for that is in your hands already: the names in `__all__`, without a leading underscore, as they're documented. `beeb.screen._need_canvas` is nobody's business, and may change in a patch release. `beeb.draw` may not.

One day you'll regret a name, and the promise doesn't trap you. It asks for manners. Keep the old name working, make it *say* that it's going, and remove it at the next major version. Python 3.13 has a decorator for it, `@warnings.deprecated("Use block().")`, which warns whoever calls the function, and makes editors strike the name through. The first Extend challenge is to try it.

#### Shipping your hints

`beeb` has had type hints since Project 8, and nobody else's pyright has ever looked at them, since a package's hints are ignored unless it has a **`py.typed`** file in it. You met that from the other side, in Projects 20 and 25. Before you add one, make sure that your hints are fit to be seen. Turn strict mode on, in `pyproject.toml`, and run `uv run pyright`.

When this chapter was written, it had one complaint: `samples`, in `synth.py`, said that it returned an `array`, and didn't say of what. `array[int]` mended it. It had been there, unnoticed, since Project 11. Then:

```console
$ touch src/beeb/py.typed
```

On Windows, make an empty file of that name in VS Code.

!!! success "Checkpoint"
    ```console
    $ uv run pytest
    $ uv run beeb --version
    beeb 1.0.0
    $ git add .
    $ git commit -m "One version number, a --version flag, and published type hints"
    ```

### Stage 5: For strangers

#### A README

Every one of your projects has had an empty `README.md` in it since the day that `uv init` made it. It's the front page of the repository on GitHub, and of the project on the index, and for most visitors it's the only page. A stranger arrives with questions, in this order, and leaves at the first one that isn't answered:

1. **What is it?** One sentence, and a picture. If it makes pictures, show one.
2. **Can I try it in a minute?** One command to paste. For you, it's `uvx`.
3. **How do I use it?** The smallest complete example, and a table of what there is.
4. **Will it break my program next month?** Your versioning promise, and a link to the changelog.
5. **How do I work on it?** Clone, sync, test.
6. **Am I allowed?** The licence.

Here's the top of `beeb`'s. Write the rest for yourself, or take it from the tutorial's repository.

<!-- listing: projects/27-ship-it/README.md -->
````markdown title="README.md"
# beeb

`MOVE`, `DRAW`, `PLOT`, `SOUND` and `ENVELOPE`, for Python: the graphics and sound
commands of a BBC Micro, built on [pygame-ce](https://pyga.me).

![Eight colour bars, as on a television test card](https://raw.githubusercontent.com/yourname/beeb/main/docs/testcard.png)

The screen is 1280 by 1024, with the origin at the bottom left, whatever the size of
the window. There are eight colours, three channels of square waves, and one of noise.

## Try it

You need [uv](https://docs.astral.sh/uv/), and nothing else:

```console
$ uvx --from beeb-lpbm beeb
```

Eight bars and a beep mean that everything works. Escape closes the window.
````

!!! warning "Gotcha"
    On GitHub, `![test card](docs/testcard.png)` works, since GitHub knows where your files are. **On the index, it's a broken image**: the README is copied into `METADATA` as text, and the picture stays behind. Every link and every image in a README that's going to an index has to be a whole address, beginning `https://`. For a picture in a GitHub repository, it's `https://raw.githubusercontent.com/yourname/beeb/main/docs/testcard.png`.

The picture itself is one line, in the REPL, with the test card showing: `beeb.screenshot("docs/testcard.png")`.

#### A changelog

`git log` is a record of what *you* did, for you: "Fix off-by-one in plot 85", "Oops", "Make ruff happy". A **changelog** is a record of what *changed for the user*, for the user, and hardly any of your commits belong in it. Its reader has one question, which is "what happens to me if I upgrade?"

There's a convention, called [Keep a Changelog](https://keepachangelog.com/), and it's worth following, because people already know how to read it. Newest first. A heading for each version, with its date. Under it, only the groups that are needed, from **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed** and **Security**. And at the top, a section called **Unreleased**, which is where you write each change *in the same commit that makes it*, while you still remember what it was. Releasing is then a matter of changing that heading to a number and a date.

<!-- listing: projects/27-ship-it/CHANGELOG.md -->
```markdown title="CHANGELOG.md"
# Changelog

Everything that a user of beeb would notice is written down here, newest first.
The format is that of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the version numbers follow [semantic versioning](https://semver.org).

## [Unreleased]

## [1.0.0] - 2026-09-20

The interface is now a promise: everything in `beeb.__all__` will go on working
until 2.0.

### Added

- `beeb --version`, and `beeb.__version__`.
- Type hints are published: the package has a `py.typed`, and passes pyright's strict mode.
- A README, a licence (MIT) and this changelog.

### Changed

- The name to install is now `beeb-lpbm`. The name to import is still `beeb`.
- The test card beeps.

### Fixed

- `beeb.synth.samples` said that it returned an `array`, and didn't say of what.
```

The rest of it is the past: go back through your tags, and write down what 0.2.0 and 0.1.0 brought. The lines at the very bottom of the file turn each heading into a link to GitHub's comparison of two tags, such as `https://github.com/yourname/beeb/compare/v0.2.0...v1.0.0`.

A file with so regular a shape can be read by a program, and in Stage 8 one will be: the notes on the release page will be this version's section, and nothing will be typed twice. Create `scripts/notes.py`:

<!-- listing: projects/27-ship-it/scripts/notes.py -->
```python title="scripts/notes.py"
"""Print one version's section of CHANGELOG.md: the notes for its release.

uv run scripts/notes.py 1.0.0
"""

import re
import sys
from pathlib import Path

CHANGELOG = Path(__file__).parent.parent / "CHANGELOG.md"


def sections(changelog: str) -> dict[str, str]:
    """Return what the changelog says about each version, newest first."""
    body = re.split(r"^\[[^\]]+\]: ", changelog, maxsplit=1, flags=re.MULTILINE)[0]
    found: dict[str, str] = {}
    for section in re.split(r"^## ", body, flags=re.MULTILINE)[1:]:
        heading, _, text = section.partition("\n")
        if match := re.match(r"\[(?P<version>[^\]]+)\]", heading):
            found[match["version"]] = text.strip()
    return found


def main() -> None:
    known = sections(CHANGELOG.read_text(encoding="utf-8"))
    match sys.argv[1:]:
        case [version] if version in known:
            print(known[version])
        case [version]:
            raise SystemExit(f"CHANGELOG.md says nothing about {version}.")
        case _:
            raise SystemExit("Usage: notes.py VERSION")


if __name__ == "__main__":
    main()
```

`re.split` with `^## ` and `re.MULTILINE` cuts the file at every second-level heading, and `partition` takes the heading off each piece. And a test, in `tests/test_release.py`, makes it impossible to release a version that the changelog hasn't heard of:

<!-- listing: projects/27-ship-it/tests/test_release.py -->
```python title="tests/test_release.py"
"""Is this ready to be released? These tests look at the project, and not at the code."""

import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
PROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
    "project"
]


def notes(version: str) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(ROOT / "scripts" / "notes.py"), version]
    return subprocess.run(
        command, capture_output=True, text=True, encoding="utf-8", check=False
    )


def test_the_changelog_has_something_to_say_about_this_version():
    done = notes(PROJECT["version"])
    assert done.returncode == 0, done.stderr
    assert "### " in done.stdout
    assert "## [" not in done.stdout


def test_the_changelog_says_nothing_about_a_version_that_never_was():
    done = notes("0.0.7")
    assert done.returncode != 0
    assert "says nothing about 0.0.7" in done.stderr
```

#### A licence

Code with no licence isn't free for all. It's the opposite: by default, in nearly every country, **nobody has the right to copy, change or use what you've written**, whatever you intended by putting it on GitHub. A licence is how you give that permission, and a cautious stranger, or any stranger with an employer, won't touch a package that hasn't one.

You don't write your own. You choose one of a few that are well understood.

| | In a sentence | You'll have met it on |
|---|---|---|
| **MIT** | Do what you like, keep my name on it, and don't blame me | Rich, Textual, pytest, FastAPI, Ruff and uv (with Apache-2.0) |
| **BSD-3-Clause** | The same, and don't use my name to advertise yours | Flask, Jinja, httpx, NumPy |
| **Apache-2.0** | The same, with careful words about patents | Requests, and most things from large companies |
| **LGPL** | Use it from any program. Changes to *it* must be shared | pygame-ce |
| **GPL** | Anything that includes it must be GPL as well | Git, and the Linux kernel |
| **CC BY-SA** | For words and pictures, not for code | this tutorial's prose, and Wikipedia |

For a small library that you'd like people to use, **MIT** is the usual choice in the Python world, and [choosealicense.com](https://choosealicense.com/), which GitHub runs, explains the others in plain words. Put the text in a file called `LICENSE`, with the year and your name in it. `gh repo edit` won't do it for you, but GitHub's "Add file" button offers a licence chooser when you name a new file `LICENSE`.

None of that is legal advice, and if money or an employer comes into it, ask somebody who's qualified to give some. Note, too, that your *dependencies'* licences are conditions on you. `beeb` imports pygame-ce, under the LGPL, which permits that. It couldn't copy code out of a GPL project and remain MIT.

!!! success "Checkpoint"
    ```console
    $ uv build
    $ uv run python -m zipfile -l dist/beeb_yourname-1.0.0-py3-none-any.whl
    $ git add .
    $ git commit -m "Add a README, a changelog and a licence"
    ```

    Is the `LICENSE` in the wheel? Where?

### Stage 6: A guard on the gate

You have ruff, pyright and pytest, and you forget to run them. Everybody does. CI catches it, five minutes later, with a red cross beside your name. It would be better not to have made the commit at all.

Git will run a program of yours at certain moments, if it finds one in `.git/hooks/` with the right name. `pre-commit` is run before each commit, and if it fails, there's no commit. But `.git/` isn't part of the repository, and so hooks aren't shared, or versioned, and everybody who clones has to set them up by hand. A tool called **[pre-commit](https://pre-commit.com/)** mends that. The hooks are described in a file that *is* in the repository. Create `.pre-commit-config.yaml`:

<!-- listing: projects/27-ship-it/.pre-commit-config.yaml -->
```yaml title=".pre-commit-config.yaml"
# Checks that run on every `git commit`, before the commit is made.
#   uvx pre-commit install           once, in each clone
#   uvx pre-commit run --all-files   whenever you like
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: check-toml
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.16.8
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: 0.12.17
    hooks:
      - id: uv-lock
```

Each `repo` is a Git repository that publishes hooks, at a tag, and pre-commit fetches each into an environment of its own, so that none of them needs to be among your project's dependencies. The first group are small and useful: is every TOML and YAML file well formed, has anybody left `<<<<<<<` in a file, is somebody about to commit a 40-megabyte video. The second is ruff. The third makes sure that `uv.lock` agrees with `pyproject.toml`.

```console
$ uvx pre-commit install
pre-commit installed at .git/hooks/pre-commit
$ uvx pre-commit run --all-files
check toml...............................................................Passed
check yaml...............................................................Passed
fix end of files.........................................................Passed
trim trailing whitespace.................................................Passed
check for added large files..............................................Passed
check for merge conflicts................................................Passed
ruff check...............................................................Passed
ruff format..............................................................Passed
uv-lock..................................................................Passed
```

`install` is done once in each clone, which is why it's in the README. From then on, every `git commit` runs the hooks, on the files that are staged. Here's a commit of a file with an unused import in it, and some spaces at the end of a line:

```console
$ git commit -m "Oops"
...
trim trailing whitespace.................................................Failed
- hook id: trailing-whitespace
- exit code: 1
- files were modified by this hook

Fixing src/beeb/oops.py

...
ruff check...............................................................Failed
- hook id: ruff-check
- files were modified by this hook

Found 1 error (1 fixed, 0 remaining).
...
```

**There was no commit.** Two hooks failed, and both mended the file as they did so. Look at what they did with `git diff`, `git add` it, and commit again. `uvx pre-commit autoupdate` moves every `rev` to its newest tag, and is worth running every month or two.

!!! warning "Gotcha"
    `git commit --no-verify` skips the hooks, and anybody who hasn't run `pre-commit install` never had them. **Hooks are a courtesy to yourself. CI is the law.** Whatever the hooks check, CI has to check as well, and it's in the next stage. Keep slow things, such as pytest, out of the hooks, or you'll learn to type `--no-verify` without thinking.

### Stage 7: CI that tests what you ship

Project 17's workflow ran the checks on three operating systems and two Pythons. That tests *your folder*, with *the newest of everything*. Your users have neither. Replace `.github/workflows/check.yml`, or create it if `beeb` never had one:

<!-- listing: projects/27-ship-it/.github/workflows/check.yml -->
```yaml title=".github/workflows/check.yml"
name: Check

on:
  push:
    branches: [main]
  pull_request:
  workflow_call: # so that the release workflow can run all of this first

permissions:
  contents: read

env:
  SDL_VIDEODRIVER: dummy
  SDL_AUDIODRIVER: dummy

jobs:
  test:
    name: Python ${{ matrix.python }} on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python: ["3.13", "3.14"]
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.1.0
        with:
          enable-cache: true
          python-version: ${{ matrix.python }}
      - run: uv sync --locked
      - run: uv run ruff check
      - run: uv run ruff format --check
      - run: uv run pyright
      - run: uv run pytest

  oldest:
    name: The oldest of everything
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.1.0
      - run: uv run --isolated --python 3.13 --resolution lowest-direct pytest

  wheel:
    name: What's shipped
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.1.0
      - run: uv build
      - name: Test the wheel, and not the folder
        run: uv run --isolated --no-project --with dist/*.whl --with pytest pytest tests
      - uses: actions/upload-artifact@v7
        with:
          name: dist
          path: dist/
```

The two `SDL_` variables tell Pygame's foundations that there's no screen and no loudspeaker, as your `conftest.py` does.

**`oldest`** is Stage 3's command, run for ever after. If somebody uses a function that arrived in pygame-ce 2.5.6, this job will fail, and you'll have to choose between the function and the floor, with your eyes open.

**`wheel`** builds the package, makes an environment with *nothing in it but the wheel and pytest*, and runs the tests there. `--no-project` tells uv to forget that it's standing in a project. It's the only job that tests what a user will actually get. If a data file isn't being packed, or a dependency is declared in the wrong table, everything else on this page will pass, and this will fail. It then keeps the built files, as an *artifact* of the run, which you can download from the run's page.

**`workflow_call`**, in the `on:` table, lets another workflow use this one as a step. The next stage does.

### Stage 8: Release

Here's the whole ritual of a release, once everything above is in place.

```console
$ uv version --bump major                 # or minor, or patch
$ code CHANGELOG.md                       # "Unreleased" becomes "[1.0.0] - 2026-09-20"
$ uv run pytest
$ git commit -am "Release 1.0.0"
$ git switch main
$ git merge ship-it
$ git tag -a v1.0.0 -m "Version 1.0.0"
$ git push origin main v1.0.0
```

Everything after that is done by a robot, which is started by the tag. Create `.github/workflows/release.yml`:

<!-- listing: projects/27-ship-it/.github/workflows/release.yml -->
```yaml title=".github/workflows/release.yml"
name: Release

# Runs when a tag such as v1.0.0 is pushed.
on:
  push:
    tags: ["v*"]

jobs:
  check:
    uses: ./.github/workflows/check.yml

  publish:
    name: Publish to TestPyPI
    needs: check
    runs-on: ubuntu-latest
    environment: testpypi
    permissions:
      id-token: write # lets TestPyPI check that this really is your repository
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.1.0
      - name: The tag and the version must agree
        run: test "v$(uv version --short)" = "${{ github.ref_name }}"
      - run: uv build
      - run: uv publish --index testpypi

  release:
    name: Make the GitHub release
    needs: publish
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.1.0
      - run: uv build
      - name: Take this version's section out of the changelog
        run: uv run --no-project scripts/notes.py "$(uv version --short)" > notes.md
      - run: gh release create "${{ github.ref_name }}" dist/* --title "${{ github.ref_name }}" --notes-file notes.md
        env:
          GH_TOKEN: ${{ github.token }}
```

**`needs`** puts the jobs in order: nothing is published unless every check has passed, and no release is announced unless the publishing worked. The first step of `publish` is a one-line guard against the commonest slip in the ritual, which is to tag `v1.0.1` with `pyproject.toml` still saying 1.0.0. `test` is the shell's own command for comparing, and if the two differ, the job stops there.

The last job makes the release page, as you did by hand in Project 22, with two improvements. The wheel and the sdist are attached to it. And its notes aren't GitHub's list of commits: they're **this version's section of your changelog**, which `scripts/notes.py` has cut out.

#### Where it's published

**[PyPI](https://pypi.org)**, the Python Package Index, is where `uv add` looks. **[TestPyPI](https://test.pypi.org)** is its twin, for practising: a separate site, with separate accounts, which is emptied from time to time, and on which nothing matters. **Publish this project to TestPyPI, and not to PyPI.** The real index is a shared, permanent namespace, and ten thousand copies of a tutorial's exercise would be litter.

The `[[tool.uv.index]]` table that's needed is short:

<!-- listing: projects/27-ship-it/pyproject.toml -->
```toml title="pyproject.toml"
# Where `uv publish --index testpypi` sends things.
[[tool.uv.index]]
name = "testpypi"
url = "https://test.pypi.org/simple/"
publish-url = "https://test.pypi.org/legacy/"
explicit = true
```

`explicit = true` means that this index is used only when something asks for it by name, and never for ordinary dependencies.

How does TestPyPI know that the upload is really from you? The old way is a **token**: a long password, made on the site, kept as a secret in GitHub, and passed as `uv publish --token`. It works, and it's one more secret to leak, and to renew. The new way is **trusted publishing**, and it has no secret at all. On TestPyPI, in your account's *Publishing* page, you say: "I trust the workflow `release.yml`, in the repository `yourname/beeb`, in its environment `testpypi`." When the job runs, GitHub gives it a signed note saying exactly which workflow, repository and environment it is. `uv publish` presents the note, and TestPyPI checks the signature. That's what `id-token: write` permits, and the `environment:` line is where, in the repository's settings on GitHub, you can require a person to approve each run.

!!! bug "Not yet verified first-hand"
    The tutorial's own repository is private, and has no TestPyPI account, so the upload to TestPyPI, and the trusted-publishing handshake, haven't been run by the author. The workflow follows [uv's guide to publishing](https://docs.astral.sh/uv/guides/package/) and [PyPI's to trusted publishers](https://docs.pypi.org/trusted-publishers/), and both files pass `actionlint`. Everything else in this chapter, including `uv publish` itself, has been run as written, against the index described next. If a step here doesn't match what you see, please open an issue.

Three rules of any index, which surprise people:

- **A version can be uploaded once, ever.** Not even its owner can replace `1.0.0`. If it's wrong, release `1.0.1`. This is why there are release candidates, and rehearsals.
- **You can't really delete.** You can *yank* a release, which hides it from installers that aren't asking for it by its exact number, and leaves it there for the projects that had already locked it.
- **Everything is public, at once, and mirrored.** Never publish a secret, since unpublishing doesn't work.

#### A rehearsal, with an index of your own

An index is a web server with a particular arrangement of pages, and you can run one on your own computer. It's a complete rehearsal, with no account, and nothing at stake. In one terminal:

```console
$ mkdir ../shelf
$ uvx --from pypiserver pypi-server run -p 8099 -a . -P . ../shelf
```

`-a . -P .` means "no passwords", which is right for a server that only your own computer can reach, and for nothing else. In another terminal, in `beeb`:

```console
$ uv build
$ uv publish --publish-url http://localhost:8099/ -u reader -p anything
Uploading beeb_yourname-1.0.0-py3-none-any.whl (10.0KiB)
Uploading beeb_yourname-1.0.0.tar.gz (8.2KiB)
```

Do it again, and it's refused: the first rule. Now be a stranger. Go somewhere that has nothing to do with `beeb`:

```console
$ cd ~
$ uvx --index http://localhost:8099/simple/ --from beeb-yourname beeb
```

Eight bars, and a beep. uv fetched your wheel from the shelf, read its `Requires-Dist`, fetched pygame-ce from PyPI, made an environment, found `beeb` in `entry_points.txt`, and ran `beeb.cli:main`. Every part of this chapter was in that one command. To depend on it from a project:

```console
$ uv init tryit
$ cd tryit
$ uv add --index rehearsal=http://localhost:8099/simple/ beeb-yourname
```

Look at what that wrote in `pyproject.toml`. The index has a name, and under `[tool.uv.sources]` there's `beeb-yourname = { index = "rehearsal" }`: **this package comes from that index, and nothing else does.**

!!! warning "Gotcha"
    That last detail is a matter of security. If you add a second index carelessly, an installer may look on *it* for *every* package. Somebody who registers the name of one of your private packages on a public index, with a higher version number, can then have their code installed in place of yours. It's called **dependency confusion**, and it has happened to very large companies. Tie each package to its index, as uv has done for you here.

### Stage 9: pip and venv, for when you meet them

uv is new. Most tutorials, most answers on the web and a good many work-places use the tools that came before it, and you should be able to read them. There's nothing new to understand, since **uv does the same things, in the same way, and mostly keeps them out of your sight**.

```console
$ python3 -m venv .venv                       # make an environment. On Windows: py -m venv .venv
$ source .venv/bin/activate                   # on Windows: .venv\Scripts\activate
(.venv) $ python -m pip install dist/beeb_yourname-1.0.0-py3-none-any.whl
(.venv) $ python -m pip list
Package       Version
------------- -------
beeb-yourname 1.0.0
pip           26.0
pygame-ce     2.5.8
(.venv) $ beeb --version
beeb 1.0.0
(.venv) $ deactivate
```

A **virtual environment** is the `.venv` folder that you've had in every project since Project 1: a `site-packages` of its own, and a `python` that looks there. **Activating** it puts its `bin` folder, or `Scripts` on Windows, at the front of your `PATH`, so that `python` and `beeb` mean *its* `python` and `beeb`, until you `deactivate`. `uv run` does the same for one command, which is why you've never had to. **pip** is the installer. `python -m pip` is the careful way to call it, since it leaves no doubt about *which* Python's pip you're talking to, and a great many hours have been lost to that doubt.

| With uv | Before uv | |
|---|---|---|
| `uv init` | write `pyproject.toml` by hand, or `poetry new`, or `hatch new` | |
| `uv python install 3.14` | python.org's installer, or pyenv, or the deadsnakes PPA | |
| `uv sync` | `python -m venv .venv`, activate, `pip install -e . -r requirements-dev.txt` | `-e` is "editable" |
| `uv add rich` | edit `pyproject.toml`, then `pip install -e .` | |
| `uv run pytest` | activate, then `pytest` | |
| `uv.lock` | `pip freeze > requirements.txt`, or pip-tools | a list of `name==version` lines |
| `uv tool install`, `uvx` | pipx | |
| `uv build`, `uv publish` | `python -m build`, `twine upload` | |

When a project has a **`requirements.txt`** and no `pyproject.toml`, it's an application, in the older style: `python -m pip install -r requirements.txt`, inside an environment, installs what it needs. uv will read such a file (`uv pip install -r requirements.txt`, or `uv add -r requirements.txt` to adopt it), and will write one for somebody who wants it:

```console
$ uv export --no-dev --no-hashes --no-emit-project
pygame-ce==2.5.8
    # via beeb-yourname
```

You'll also meet **Poetry**, **Hatch** and **PDM**, which are project managers in the way that uv is, and all of which read `pyproject.toml`. And you'll meet **conda**, which is a different world, with its own packages and its own index, popular in science because it can install things that aren't Python at all. It's best not to mix it with the others inside one environment.

## Type-in listing

`python -m zipfile -l` showed you the files in a wheel. This shows you what an installer sees. Save it as `inside.py`, and run it with `uv run inside.py dist/*.whl`. Then find a wheel that isn't yours: there are hundreds under `uv cache dir`.

<!-- listing: projects/27-ship-it/inside.py -->
```python title="inside.py" linenums="1"
"""What's in a wheel?    uv run inside.py dist/*.whl"""

import sys
import zipfile
from email.parser import Parser

SHOWN = {"Name", "Version", "Requires-Python", "Requires-Dist", "License-Expression"}

for path in sys.argv[1:]:
    with zipfile.ZipFile(path) as wheel:
        files = [item for item in wheel.infolist() if not item.is_dir()]
        print(f"{path}\n")
        for item in files:
            print(f"  {item.file_size:>6,}  {item.filename}")
        total = sum(item.file_size for item in files)
        print(f"  {total:>6,} bytes, in {len(files)} files\n")

        (metadata,) = [item for item in files if item.filename.endswith("/METADATA")]
        message = Parser().parsestr(wheel.read(metadata).decode("utf-8"))
        for name, value in message.items():
            if name in SHOWN:
                print(f"  {name + ':':<20}{value}")
        words = len((message.get_payload() or "").split())
        print(f"  ... and a README of {words} words")
```

1. `METADATA` is read with a parser from the `email` package. Why does that work? What's the "body" of the message?
2. Find `Requires-Dist` in the output for your wheel, and then in `pyproject.toml`. Where's pytest? Where's `uv.lock`?
3. What does the comma do in `{item.file_size:>6,}`? And `name + ':'`, inside an f-string's curly brackets?
4. `(metadata,) = [...]`, with a comma and brackets. What happens if a wheel has two `METADATA` files, or none? Why is that better than `[...][0]`?
5. Run it on pygame-ce's wheel. How big is it? What are the files that end in `.so`, or `.pyd`?

## Bug hunt

A colleague has written a little package, `shout`, which says things in a box. It's in the tutorial's repository, as `projects/27-ship-it/bughunt/shout/`. They're pleased with it:

```console
$ cd bughunt/shout
$ uv run pytest
1 passed
$ uv run shout ship it
╭──────────╮
│ SHIP IT! │
╰──────────╯
```

They built it, and sent the wheel to a friend, whose reply was short: "Doesn't work. `ModuleNotFoundError`." "It works on my machine", says your colleague, and it does.

1. **Reproduce it.** You need to be the friend: somebody who has the wheel, and nothing else. Stage 7 has the command.
2. **Explain it.** Why do the tests pass? `uv tree` will show you where everything in the environment came from.
3. **Make it fail in the tests**, without changing the tests.
4. **Fix it**, without touching a line of Python.

??? success "Solution"
    ```console
    $ uv build
    $ uv run --isolated --no-project --with dist/shout-0.1.0-py3-none-any.whl shout ship it
    ...
    ModuleNotFoundError: No module named 'rich'
    ```

    ```console
    $ uv tree
    shout v0.1.0
    ├── pytest v9.1.1 (group: dev)
    ├── rich v15.0.0 (group: dev)
    ...
    ```

    `shout` imports Rich, and Rich is in the **`dev` group**. Somebody typed `uv add --dev rich`, perhaps on the same line as pytest. On your colleague's machine, `uv sync` installs the dev group, and so Rich is there, and everything works: the program, the tests, CI. But dependency groups are never published. The wheel's `METADATA` has no `Requires-Dist` at all, and a user's installer brings nothing with it.

    The failing test is Stage 7's `wheel` job, which runs the *same* tests, where only the wheel is installed:

    ```console
    $ uv run --isolated --no-project --with dist/shout-0.1.0-py3-none-any.whl --with pytest pytest tests
    ERROR tests/test_shout.py
    ```

    And the cure is two commands, which move one line of TOML from one table to another:

    ```console
    $ uv remove --dev rich
    $ uv add rich
    ```

    **What to take from it.** "It works on my machine" is nearly always true, and nearly always beside the point: your machine has a history, and your user's hasn't. The only honest test of a package is to install *what you ship*, *where nothing else is*, and try it. A fresh environment costs uv about a tenth of a second, and so there's no reason not to do it every time.

## Challenges

**Tweak**

1. Add a `[project.urls]` entry called `Documentation`, pointing at your README on GitHub. Build, and find it in `METADATA`.
2. `uv version --bump patch --dry-run`, then `--bump minor --bump rc`. What would each release be for?
3. Add a hook from `pre-commit-hooks` that refuses a commit made directly on `main`. It's called `no-commit-to-branch`.

**Extend**

1. **Change your mind, politely.** `cli.py` has a useful function, `block`. Promote it to the public interface, as `beeb.block`. Then suppose that it had been published as `beeb.rectangle`: keep the old name working, with `@warnings.deprecated`, test the warning with `pytest.warns`, and write the changelog entry, under the right heading. Which number changes now? And when `rectangle` finally goes?
2. **An extra.** Project 11 had a challenge to work out whole notes at once with NumPy. Offer it as `beeb-yourname[fast]`: an optional dependency, imported inside a `try`, with the pure-Python version as the fall-back. How will you test both, in CI?
3. **Ship your BASIC.** Give Project 17's `tiny-basic` the same treatment: a name, metadata, a README with a listing in it, a changelog, a licence and the two workflows. It's an *application*, and not a library. What's different about its dependency bounds, and about what `1.0.0` promises?
4. **A badge.** GitHub will draw a little image that says whether your checks are passing: it's in the "…" menu of a workflow's page. Put it at the top of the README. Then find out what [shields.io](https://shields.io) can say about a project on an index.

**Invent**

1. **Release notes from commits.** Some projects go the other way, and write the changelog *from* the commits, by keeping to a convention for messages, such as "feat:", "fix:" and "feat!:". It's called Conventional Commits. Write the program that reads `git log` between two tags, and drafts the section. What do you gain, and what do you lose?
2. **Your own index, properly.** An index is a folder of static pages, in a layout that's described in a PEP numbered 503. Write a generator, in Project 19's manner, that turns a folder of wheels into one, and publish it with GitHub Pages. You'd have a private shelf, for yourself and your friends, that costs nothing.
3. **What's in my environment?** With `importlib.metadata.distributions()`, draw a Rich tree of everything that's installed: each distribution, its version, its licence, and what requires it. Which of your projects has the most dependencies that you never asked for? Are all of their licences ones that you can live with?

A solution to the first Extend, and the bug hunt's test, are in the project's `solutions/` folder.

## Recap

You can now:

- [x] say what's in a wheel and an sdist, read a wheel's file name, and explain what installing does
- [x] tell a distribution's name from a package's, and give yours a name that's free
- [x] fill in every field of `[project]`, with a licence expression, classifiers and links
- [x] write dependency bounds that are tested facts, and say why a library shouldn't cap them, and an application should lock them
- [x] choose between dependencies, optional dependencies and dependency groups
- [x] keep the version number in one place, read it with `importlib.metadata`, and change it with `uv version`
- [x] read and write every form of version number, and say what 1.0.0 promises, and about what
- [x] publish your type hints with `py.typed`
- [x] write a README that answers a stranger's questions in order, with links that survive the journey to an index
- [x] keep a changelog for users, and have a program cut release notes from it
- [x] choose a licence, and say what having none means
- [x] guard your commits with pre-commit hooks, and know why CI must check the same things
- [x] test the oldest dependencies that you claim to support, and the built wheel in an empty environment
- [x] release by pushing a tag: checks, then publishing without a stored secret, then a release page
- [x] run a package index of your own, publish to it, and install from it as a stranger would
- [x] explain dependency confusion and typosquatting, and how to avoid both
- [x] read, and use, venv, pip and `requirements.txt`

**Read more:** [The Python Packaging User Guide](https://packaging.python.org/) · [Writing your `pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) · [Version specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/), which is PEP 440 as it stands today · [uv: building and publishing a package](https://docs.astral.sh/uv/guides/package/) · [Keep a Changelog](https://keepachangelog.com/) · [Semantic Versioning](https://semver.org/) · [Choose a License](https://choosealicense.com/) · [pre-commit](https://pre-commit.com/) · [Trusted publishers, on PyPI](https://docs.pypi.org/trusted-publishers/) · [Should you use upper bound version constraints?](https://iscinumpy.dev/post/bound-version-constraints/), by Henry Schreiner, which is long, and settles the matter

You can build things, and you can ship them. One project remains, and it uses nearly everything. In Project 28 you'll build a computer: a little micro, in Pygame, that boots to a `>` prompt, runs the BASIC that you wrote in Project 17, draws with `MOVE` and `DRAW`, plays `SOUND` and `ENVELOPE`, has sprites that the real one never had, and ends with a game, typed in from a listing, in a language of your own, on a machine of your own.
