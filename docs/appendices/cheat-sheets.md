# Cheat sheets

The commands that this tutorial used, in one place, with the project that introduced each. It's for the day, six months from now, when you know that there *is* a command, and can't remember what it's called. A few useful relations of those commands, which the tutorial didn't need, are here as well, and are marked *new*.

## uv

| | | |
|---|---|---|
| `uv init name` | a new project, as a package, in a folder called `name` | [0](../part-0-switching-on/p00-hello-beeb.md), [5](../part-1-console/p05-colossal-cupboard.md) |
| `uv init --no-package name` | a new project with one flat `main.py` | [0](../part-0-switching-on/p00-hello-beeb.md) |
| `uv run file.py`, `uv run pytest`, `uv run name` | run something, in the project's environment, making or mending the environment first | [0](../part-0-switching-on/p00-hello-beeb.md) |
| `uv run python` | the REPL, with your project importable | |
| `uv add rich`, `uv add "textual>=8,<9"` | add a dependency | [4](../part-1-console/p04-codebreaker.md) |
| `uv add --dev pytest ruff pyright` | add something that's for working on the project, and isn't shipped | [3](../part-1-console/p03-dice-lab.md) |
| `uv add --editable ../beeb` | depend on a project of your own, in a folder | [11](../part-2-pygame/p11-sound-and-envelope.md) |
| `uv remove rich` | | |
| `uv sync`, `uv sync --locked` | make `.venv` match `uv.lock`. In CI: fail if the lock is out of date | [17](../part-3-interpreters/p17-tiny-basic.md) |
| `uv lock --upgrade`, `uv lock --upgrade-package rich` | move to newer versions | |
| `uv tree` | what depends on what, and why it's here | [27](../part-6-shipping/p27-ship-it.md) |
| `uv python install 3.14`, `uv python list` | Pythons | [The toolkit](../part-0-switching-on/toolkit.md) |
| `uv run --python 3.14t file.py` | run with another Python: here, the free-threaded one | [25](../part-5-tui/p25-newsroom.md) |
| `uv run --isolated --resolution lowest-direct pytest` | test against the oldest versions that you claim to support | [27](../part-6-shipping/p27-ship-it.md) |
| `uv run --isolated --no-project --with dist/*.whl --with pytest pytest tests` | test the wheel, and not the folder | [27](../part-6-shipping/p27-ship-it.md) |
| `uvx ruff check`, `uvx --from pkg command` | run a tool without installing it | [27](../part-6-shipping/p27-ship-it.md) |
| `uv tool install .`, `uv tool list`, `uv tool uninstall name` | install a program as a command, for good | [17](../part-3-interpreters/p17-tiny-basic.md) |
| `uv version`, `uv version --bump minor` | read, or change, the project's version | [27](../part-6-shipping/p27-ship-it.md) |
| `uv build`, `uv publish --index testpypi` | make a wheel and an sdist; upload them | [17](../part-3-interpreters/p17-tiny-basic.md), [27](../part-6-shipping/p27-ship-it.md) |
| `uv export --no-dev --no-hashes` | a `requirements.txt`, for somebody who wants one | [27](../part-6-shipping/p27-ship-it.md) |

### uv, and what came before it

| With uv | Before uv |
|---|---|
| `uv init` | write `pyproject.toml` by hand, or `poetry new`, or `hatch new` |
| `uv python install 3.14` | python.org's installer, or pyenv |
| `uv sync` | `python -m venv .venv`, activate it, `python -m pip install -e . -r requirements-dev.txt` |
| `uv add rich` | edit `pyproject.toml`, then `pip install -e .` |
| `uv run pytest` | activate the environment, then `pytest` |
| `uv.lock` | `pip freeze > requirements.txt`, or pip-tools |
| `uv tool install`, `uvx` | pipx |
| `uv build`, `uv publish` | `python -m build`, `twine upload` |

To activate an environment by hand: `source .venv/bin/activate` on macOS and Linux, `.venv\Scripts\activate` on Windows, and `deactivate` to leave.

## Git

### Every day

| | | |
|---|---|---|
| `git status` | where am I, and what's changed? **Run it constantly** | [1](../part-1-console/p01-hi-lo.md) |
| `git diff`, `git diff --staged` | what exactly have I changed? | [1](../part-1-console/p01-hi-lo.md) |
| `git add .`, `git add file` | choose what goes in the next commit | [0](../part-0-switching-on/p00-hello-beeb.md) |
| `git commit -m "Say what it does"` | | [0](../part-0-switching-on/p00-hello-beeb.md) |
| `git log --oneline`, `git log --oneline --graph --all` | history, and its shape | [1](../part-1-console/p01-hi-lo.md), [5](../part-1-console/p05-colossal-cupboard.md) |
| `git log --oneline -- path` | the history of one file | [26](../part-5-tui/p26-adventure-third-edition.md) |
| `git show abc123` | one commit | *new* |

### Branches

| | | |
|---|---|---|
| `git switch -c idea` | a new branch, and move to it | [5](../part-1-console/p05-colossal-cupboard.md) |
| `git switch main` | move | [5](../part-1-console/p05-colossal-cupboard.md) |
| `git merge idea` | bring a branch's work into the one that you're on | [5](../part-1-console/p05-colossal-cupboard.md) |
| `git branch -d idea` | delete a merged branch | [5](../part-1-console/p05-colossal-cupboard.md) |
| Conflict: edit the file, take out the `<<<<<<<` markers, `git add`, `git commit` | | [12](../part-2-pygame/p12-asteroids.md) |
| `git merge --abort` | I've changed my mind | [12](../part-2-pygame/p12-asteroids.md) |
| `git rebase main` | replay my branch on top of `main`. **Never on commits that anybody else has** | [21](../part-4-web/p21-adventure-online.md) |

### Undoing

| | | |
|---|---|---|
| `git restore file` | throw away my uncommitted changes to a file. **For ever** | [4](../part-1-console/p04-codebreaker.md) |
| `git restore --staged file` | un-add it | [4](../part-1-console/p04-codebreaker.md) |
| `git commit --amend` | mend the last commit, **if it hasn't been pushed** | [4](../part-1-console/p04-codebreaker.md) |
| `git revert abc123` | a new commit that undoes an old one. Safe on shared history | [13](../part-2-pygame/p13-life-in-pixels.md) |
| `git stash`, `git stash pop` | put my changes aside for a moment; bring them back | [9](../part-2-pygame/p09-snake.md) |
| `git rm --cached file` | stop tracking a file, and keep it on disc. Then add it to `.gitignore` | [9](../part-2-pygame/p09-snake.md) |
| `git reflog` | everywhere that `HEAD` has been. Nearly nothing that was committed is ever truly lost | *new* |

### Finding out

| | | |
|---|---|---|
| `git bisect start`, `git bisect bad`, `git bisect good v1.0`, … `git bisect reset` | find the commit that broke it, by halving | [13](../part-2-pygame/p13-life-in-pixels.md) |
| `git bisect run uv run pytest tests/test_x.py` | the same, automatically | [13](../part-2-pygame/p13-life-in-pixels.md) |
| `git blame file` | who last changed each line, and in which commit | *new* |

### GitHub

| | | |
|---|---|---|
| `gh repo create name --public --source=. --push` | put this project on GitHub | [6](../part-1-console/p06-life.md) |
| `git push`, `git pull` | | [6](../part-1-console/p06-life.md) |
| `git tag -a v1.0.0 -m "Version 1.0.0"`, `git push origin v1.0.0` | mark a version | [7](../part-1-console/p07-fractal-factory.md), [22](../part-4-web/p22-high-score-server.md) |
| `gh pr create`, `gh pr view --web`, `gh pr merge` | pull requests | [16](../part-3-interpreters/p16-logo.md) |
| `gh run list`, `gh run watch`, `gh run view --log-failed` | how is CI getting on? | [17](../part-3-interpreters/p17-tiny-basic.md) |
| `gh release create v1.0.0 dist/* --notes-file notes.md` | a release, with files attached | [22](../part-4-web/p22-high-score-server.md), [27](../part-6-shipping/p27-ship-it.md) |

### The release ritual

```console
$ uv version --bump minor                 # or major, or patch
$ code CHANGELOG.md                       # "Unreleased" becomes "[1.1.0] - the date"
$ uv run pytest
$ git commit -am "Release 1.1.0"
$ git tag -a v1.1.0 -m "Version 1.1.0"
$ git push origin main v1.1.0             # and the release workflow does the rest
```

**Patch**: a fix. **Minor**: something new, and nothing broken. **Major**: somebody's program might break. [Project 27](../part-6-shipping/p27-ship-it.md).

## Testing and checking

| | | |
|---|---|---|
| `uv run pytest` | run all the tests | [3](../part-1-console/p03-dice-lab.md) |
| `uv run pytest -k word`, `-v`, `-q` | tests whose names match; more detail; less | [3](../part-1-console/p03-dice-lab.md) |
| `uv run pytest -x`, `--lf` | stop at the first failure; run only what failed last time | *new* |
| `uv run pytest tests/test_x.py::test_name` | one test | [3](../part-1-console/p03-dice-lab.md) |
| `uv run pytest -s` | let `print` show | *new* |
| `uv run pytest --cov=package --cov-branch --cov-report=term-missing` | coverage | [17](../part-3-interpreters/p17-tiny-basic.md) |
| `uv run pytest --snapshot-update` | accept new Textual snapshots, after looking at them | [24](../part-5-tui/p24-teletext-viewer.md) |
| `@pytest.mark.parametrize(("a", "b"), [(1, 2), (3, 4)])` | one test, many cases | [6](../part-1-console/p06-life.md) |
| `tmp_path`, `capsys`, `@pytest.fixture`, `caplog`, `monkeypatch` | things that a test can ask for | [5](../part-1-console/p05-colossal-cupboard.md), [6](../part-1-console/p06-life.md), [8](../part-2-pygame/p08-mode2-sketchpad.md), [15](../part-2-pygame/p15-sprite-editor.md), [23](../part-5-tui/p23-rich-dashboard.md) |
| `pytest.raises(ValueError, match="…")`, `pytest.approx(0.3)`, `pytest.warns(…)` | an error, a float, a warning | [5](../part-1-console/p05-colossal-cupboard.md), [3](../part-1-console/p03-dice-lab.md), [27](../part-6-shipping/p27-ship-it.md) |
| `uv run ruff check`, `uv run ruff check --fix`, `uv run ruff format` | lint; mend what can be mended; format | [3](../part-1-console/p03-dice-lab.md) |
| `uv run pyright` | check the types | [4](../part-1-console/p04-codebreaker.md), [17](../part-3-interpreters/p17-tiny-basic.md) |
| `uvx pre-commit install`, `uvx pre-commit run --all-files` | hooks | [27](../part-6-shipping/p27-ship-it.md) |
| `uv run python -m timeit "…"`, `uv run python -m cProfile -s cumtime file.py` | how fast, and where's the time going? | [7](../part-1-console/p07-fractal-factory.md) |
| `uv run python -X dev file.py` | Python's development mode: more warnings, and asyncio's debugger | [25](../part-5-tui/p25-newsroom.md) |

## VS Code

++cmd++ on a Mac is ++ctrl++ everywhere else.

| | |
|---|---|
| ++ctrl+shift+p++ | the Command Palette: every command there is, by name. If you learn one shortcut, learn this |
| ++ctrl+p++ | open a file by typing part of its name |
| ++ctrl+grave++ | the terminal |
| ++f12++, ++alt+f12++ | go to the definition; peek at it without leaving |
| ++shift+f12++ | find every reference |
| ++f2++ | rename a symbol, everywhere, safely. [Project 10](../part-2-pygame/p10-breakout.md) |
| ++ctrl+period++ | quick fixes, and refactorings: extract a method, add an import |
| ++ctrl+shift+o++, ++ctrl+t++ | go to a symbol in this file; in the project |
| ++alt+up++, ++alt+down++; ++shift+alt+down++ | move a line; copy it |
| ++ctrl+d++; ++ctrl+shift+l++ | select the next occurrence; all of them |
| ++ctrl+slash++ | comment, and uncomment |
| ++f5++, ++f9++, ++f10++, ++f11++, ++shift+f11++ | debug: start, breakpoint, step over, step in, step out. [Project 2](../part-1-console/p02-turtle-sketchbook.md) |
| Right-click a breakpoint | conditions, hit counts and logpoints. [Project 8](../part-2-pygame/p08-mode2-sketchpad.md) |
| The flask icon | the Testing panel: run, and debug, one test. [Project 3](../part-1-console/p03-dice-lab.md) |
| The branch icon | Source Control: stage lines, commit, and see diffs side by side. [Project 0](../part-0-switching-on/p00-hello-beeb.md) |
| **Python: Select Interpreter** | when imports are underlined and shouldn't be: choose the project's `.venv` |
| `.vscode/launch.json`, `tasks.json`, `*.code-snippets` | how to run, what to run, and what to type for you. Projects [8](../part-2-pygame/p08-mode2-sketchpad.md) and [14](../part-2-pygame/p14-wireframe.md) |

## A new project, from nothing

```console
$ uv init thing && cd thing
$ uv add --dev pytest ruff pyright
$ git add . && git commit -m "Start"
$ gh repo create thing --public --source=. --push
$ code .
```

Then, in `pyproject.toml`:

```toml
[tool.pytest]
testpaths = ["tests"]

[tool.pyright]
include = ["src"]
typeCheckingMode = "strict"
```

And, when there's something to show: a README with a picture, a licence, a changelog, `.github/workflows/check.yml`, and `.pre-commit-config.yaml`, from [Project 27](../part-6-shipping/p27-ship-it.md).
