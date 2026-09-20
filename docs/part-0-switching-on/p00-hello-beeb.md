# Project 0 · Hello, Beeb

Switch on a BBC Micro and it greets you with its name, how much memory it has, and a prompt. Your first Python program does the same for your computer. The program is tiny. The point of the project is everything around it: creating a project, running it, poking at Python interactively, and saving your work in Git. It's the loop you'll go round in every project from here on.

```text
Python 3.14.4 Computer

Darwin arm64

Ready
>
```

| | |
|---|---|
| **You'll learn** | How a Python project is laid out; running code with uv; the interactive prompt; a first look at functions, imports and f-strings |
| **New tool skill** | `uv init` and `uv run`; your first Git commits, from the terminal and from VS Code |
| **Time** | 45 minutes |
| **Before you start** | [The toolkit](toolkit.md) is installed |

## Predict

You haven't written any Python yet, which makes this the ideal moment to guess. What do you think each line prints? Decide, then look.

!!! question "Predict"
    ```python
    print(2 ** 10)
    print("Beeb" * 3)
    print(7 / 2)
    ```

??? success "Answer"
    ```text
    1024
    BeebBeebBeeb
    3.5
    ```

    `**` is "to the power of" (BBC BASIC's `^`). Multiplying a string repeats it. And `/` is true division: it gives `3.5`, where C, Java, and BASIC's `DIV` would give `3`. Python's whole-number division is `//`. More on all three in Project 1.

## Build

### Stage 1: Create the project

Open a terminal and go to your `making` folder. Then ask uv for a new project:

```console
$ uv init --no-package hello-beeb
Initialized project `hello-beeb` at `/Users/you/making/hello-beeb`
$ cd hello-beeb
$ code .
```

That last command opens the folder in VS Code. (The `.` means "this folder".) VS Code will ask whether you trust the authors of the files in this folder. You *are* the author, so say yes.

In VS Code's Explorer, on the left, you'll find that uv has made you five files.

| File | What it is |
|---|---|
| `main.py` | Your program. Python files end in `.py`. |
| `pyproject.toml` | The project's description: its name, the Python version it needs, the libraries it depends on. Every modern Python project has one. |
| `.python-version` | The Python version this project uses. uv reads it. |
| `README.md` | For telling other people, and future you, what this project is. Empty for now. |
| `.gitignore` | A list of files that Git should take no notice of. |

There's also a hidden folder, `.git`. uv has made this project a Git repository for you, all ready for your first commit.

!!! note "Under the bonnet"
    Without `--no-package`, uv sets a project up as an installable *package*, with your code in a `src` folder and a little more ceremony in `pyproject.toml`. That's the right shape for anything substantial, and you'll move to it in Project 5, when there's enough code to need organising. For a program that's a single file, the simpler layout is the right one.

Open `main.py`. uv has written you a starter program:

<!-- listing: none -->
```python title="main.py"
def main():
    print("Hello from hello-beeb!")


if __name__ == "__main__":
    main()
```

Reading from the top: `def` defines a function, here called `main`, and the function's body is the indented line beneath it. There are no braces and no `ENDPROC`. **The indentation is the block structure.** Everyone indents their code anyway; Python makes it mean something. The convention is four spaces, and VS Code puts them in for you when you press ++tab++.

The last two lines are an idiom you'll see at the bottom of a great many Python files. It means "if this file is being run as a program, call `main()`". Project 4 explains how it works. Until then, the rule is: your code goes inside `main()`.

!!! example "Run it"
    VS Code has a terminal built in. Open it with **Terminal → New Terminal**, or ++ctrl+grave++. It starts in your project folder. Type:

    ```console
    $ uv run main.py
    Using CPython 3.14.4
    Creating virtual environment at: .venv
    Hello from hello-beeb!
    ```

    The first two lines appear only this once. uv has noticed the project has no *virtual environment*, a private folder holding this project's Python and libraries, and has made one, in `.venv`. It has also written `uv.lock`, which records the exact version of every library the project uses. There aren't any yet. Run the command again and you get only the greeting.

Now save your work, which, in this tutorial, always means a Git commit. Ask Git how things stand:

```console
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore
	.python-version
	README.md
	main.py
	pyproject.toml
	uv.lock

nothing added to commit but untracked files present (use "git add" to track)
```

Git can see six files it isn't yet keeping track of. It can't see `.venv`, because `.gitignore` tells it not to look: a virtual environment is large, and uv can rebuild it at any time from `pyproject.toml` and `uv.lock`. You commit the recipe, not the cake.

A commit takes two steps. First you choose what goes into the snapshot, which Git calls *staging*. Then you take the snapshot, with a message saying what it is.

```console
$ git add .
$ git commit -m "Start the hello-beeb project"
[main (root-commit) 8612d4b] Start the hello-beeb project
 6 files changed, 32 insertions(+)
```

`git add .` stages everything in this folder. The `-m` is for *message*. Write your messages as instructions, "Start the project", "Add the banner", which is the convention. It reads well in a list, as you'll see.

!!! success "Checkpoint"
    Your first commit is made. `git status` now reports `nothing to commit, working tree clean`. That's the state you want to be in whenever you stop work.

### Stage 2: Talk to Python

Before changing the program, meet the part of Python that's most like a BBC Micro: the interactive prompt. Python people call it the *REPL*, for read–evaluate–print loop, because that is all it does. In the terminal:

```console
$ uv run python
```

You get a banner and a `>>>` prompt. Type an expression and Python prints its value.

```pycon
>>> 2 ** 10
1024
>>> 7 / 2
3.5
>>> "Beeb" * 3
'BeebBeebBeeb'
>>> 2 ** 100
1267650600228229401496703205376
```

BBC BASIC would have answered `1.2676506E30`: the right size, but only the first eight digits of it. An `int` in C or Java would have overflowed. Python's integers are exact, and as big as they need to be.

Python's standard library is large, and `import` brings a piece of it within reach. The `platform` module knows about the machine you're on:

<!-- no-doctest -->
```pycon
>>> import platform
>>> platform.python_version()
'3.14.4'
>>> platform.system()
'Darwin'
>>> platform.machine()
'arm64'
```

Yours will say something different, of course: `'Windows'` and `'AMD64'`, perhaps, or `'Linux'`. (`'Darwin'` is the name of the core of macOS.)

A few things worth knowing about this prompt:

- Type `platform.` and press ++tab++ to see everything the module offers.
- `help(platform.system)` shows the documentation for anything. Press ++q++ to leave it.
- ++up++ brings back earlier lines, and a multi-line block comes back as one piece, ready to edit.
- `exit` gets you out. So does ++ctrl+d++ (++ctrl+z++ then ++enter++ on Windows).

The REPL is the quickest way to find out how Python behaves, and this tutorial will send you there often. Whenever you catch yourself wondering "what happens if…?", that's the place to find out.

!!! info "Coming from BBC BASIC"
    The `>>>` prompt is the nearest thing Python has to BASIC's `>`. It's an *immediate mode*: what you type is run at once. What it lacks is line numbers. You can't build a program up at the prompt and then `RUN` it. Programs live in files, and the prompt is for experiments.

### Stage 3: The boot banner

Time to make the program your own. Change `main.py` to this:

<!-- listing: projects/00-hello-beeb/main.py -->
```python title="main.py"
import platform


def main():
    print(f"Python {platform.python_version()} Computer")
    print()
    print(f"{platform.system()} {platform.machine()}")
    print()
    print("Ready")
    print(">")


if __name__ == "__main__":
    main()
```

Two new things. Imports go at the top of the file, by convention. And the strings with an `f` in front of the opening quote are *f-strings*: inside one, anything in `{braces}` is worked out as Python and its value dropped into the string. You'll use them constantly.

Save with ++ctrl+s++ (++cmd+s++). If your spacing was untidy, watch it snap into line: that's Ruff, formatting on save.

!!! example "Run it"
    ```console
    $ uv run main.py
    Python 3.14.4 Computer

    Darwin arm64

    Ready
    >
    ```

Now try breaking it. Change `platform.machine()` to `platform.machin()`, and save. Two things happen before you run anything: a squiggle appears under `machin`, and Error Lens writes the complaint at the end of the line. That's Pylance, reading your code as you type. Run it anyway:

```text
Python 3.14.4 Computer

Traceback (most recent call last):
  File "/Users/you/making/hello-beeb/main.py", line 14, in <module>
    main()
    ~~~~^^
  File "/Users/you/making/hello-beeb/main.py", line 7, in main
    print(f"{platform.system()} {platform.machin()}")
                                 ^^^^^^^^^^^^^^^
AttributeError: module 'platform' has no attribute 'machin'. Did you mean: 'machine'?
```

The first `print` worked; then Python reached the bad line and stopped. What follows is a *traceback*, and you read it from the bottom. The last line says what went wrong, and even suggests the cure. The lines above say where: line 7, in `main`, which was called from line 14. Python's error messages have become very good in the last few versions. Get into the habit of reading them properly; most of the time, the answer is there.

Put the `e` back, check that the program runs, and commit. This time, do it from VS Code:

1. Click the **Source Control** icon in the left-hand bar, the one like a branching track. It's wearing a badge with a `1` on it: one changed file.
2. Click `main.py` in the list. VS Code shows you the old and new versions side by side, with the differences coloured. Looking over your changes before committing them is a habit worth forming now.
3. Hover over `main.py` and click the **+** to stage it.
4. Type a message in the box at the top, `Show a boot banner`, and click **Commit**.

Terminal or editor, it's the same two steps underneath, and you can mix them freely. This tutorial mostly gives the terminal commands, because they're easier to write down. Use whichever you like.

!!! success "Checkpoint"
    Two commits. See them with:

    ```console
    $ git log --oneline
    3f2a91c Show a boot banner
    8612d4b Start the hello-beeb project
    ```

    Your code numbers, called *hashes*, will differ. Newest is at the top.

### Stage 4: A script that brings its own libraries

Python's standard library is big, but the wider world of Python libraries is enormous: over half a million packages on the [Python Package Index](https://pypi.org/), all free. One of them, [Rich](https://rich.readthedocs.io/), puts colour, tables and panels in the terminal. Let's use it for a better banner.

Normally you add a library to a project with `uv add`, and you'll do that in Project 4. But for a single-file program there's a neat alternative: the file itself can say what it needs. In the terminal:

```console
$ uv init --script banner.py
Initialized script at `banner.py`
$ uv add --script banner.py rich
Resolved 4 packages in 150ms
```

Open `banner.py` and look at the top:

<!-- listing: projects/00-hello-beeb/banner.py -->
```python title="banner.py"
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "rich>=15.0.0",
# ]
# ///
```

To Python, those lines are comments, and it ignores them. To uv, they're instructions. It's a standard format, so other tools understand it as well. Now replace everything *below* that block, so that the whole file reads:

<!-- listing: projects/00-hello-beeb/banner.py -->
```python title="banner.py"
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "rich>=15.0.0",
# ]
# ///

import platform

from rich.console import Console
from rich.panel import Panel


def main() -> None:
    console = Console()
    banner = (
        f"[bold yellow]Python {platform.python_version()} Computer[/]\n\n"
        f"[cyan]{platform.system()} {platform.machine()}[/]\n\n"
        "[green]Ready[/]\n[bold white]>[/][blink]_[/]"
    )
    console.print(Panel(banner, width=44, border_style="red"))


if __name__ == "__main__":
    main()
```

A few things to notice:

- `from rich.console import Console` is the other form of import. It fetches one name out of a module, so that you can write `Console` rather than `rich.console.Console`.
- The `[bold yellow]…[/]` tags are Rich's own markup for styling text.
- Three strings sitting next to each other inside the parentheses, with nothing between them, are joined into one. It's a tidy way to write a long string over several lines. `\n` is a new line.
- The `-> None` after `main()` is a *type hint*, saying that this function doesn't return anything. uv put it there. Hints start in earnest in Project 3.

!!! example "Run it"
    ```console
    $ uv run banner.py
    ```

    The first time, uv fetches Rich, which takes a second or so. Then you get your banner in a red box, in colour, with a blinking cursor if your terminal is willing. Rich hasn't been installed into your project, or anywhere else you need to think about. uv keeps a hidden environment for this script and reuses it next time.

    You could email `banner.py` to a friend who has uv, and `uv run banner.py` would work for them, straight away. For small tools, that's a very handy trick.

!!! success "Checkpoint"
    ```console
    $ git add banner.py
    $ git commit -m "Add a colour banner script"
    ```

## Type-in listing

Here's the first of the type-in listings. Make a new file called `bars.py`, type this in, and run it with `uv run bars.py`. Type it exactly, and mind the eight spaces before the second quote on line 5.

<!-- listing: projects/00-hello-beeb/bars.py -->
```python title="bars.py" linenums="1"
NAMES = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]

for row in range(6):
    for colour in range(8):
        print(f"\033[4{colour}m        ", end="")
    print("\033[0m")

for name in NAMES:
    print(f"{name:^8}", end="")
print()
```

You should get a test card: eight coloured bars, each with its name underneath. Now work out how.

1. What does `end=""` do? Take one out and see.
2. `\033` is the *escape* character, and `\033[41m` tells a terminal "red background from here on". So what does `\033[0m` do, and what goes wrong if you leave it out?
3. What does the `:^8` in `{name:^8}` do? Try `:<8`, `:>8` and `:*^8`.

Those eight colours, in that order, are the eight colours of the BBC Micro. You'll be seeing them again.

## Challenges

**Tweak**

1. Add a line to the banner in `main.py` with your own name in it.
2. At the REPL, type `import this`. It's an Easter egg: nineteen aphorisms about how Python likes to be written. You'll see what several of them mean by the end of Part 1.

**Extend**

1. `platform` has other functions. Find one that reports your operating system's version, and add it to the banner. (Remember `platform.` then ++tab++ at the REPL, and `help()`.)
2. Make `bars.py` print the names *in* their own colours. The code for coloured text is `\033[3` then the colour number then `m`.

??? tip "Hint for the second one"
    The loop `for name in NAMES:` gives you each name but not its number. One fix is to loop over the numbers instead, `for colour in range(8):`, and look the name up with `NAMES[colour]`. Project 3 has a better way.

Commit when you're done. In fact, commit whenever something works. Commits are free.

## Recap

You now know how to:

- [x] create a project with `uv init`, and say what each file in it is for
- [x] run a program with `uv run`, without ever having to ask which Python you're using
- [x] try things out at the REPL, and find your way around a module with ++tab++ and `help()`
- [x] read a traceback from the bottom up
- [x] write a function, import a module, and build a string with an f-string
- [x] stage and commit changes, from the terminal and from VS Code
- [x] write a single-file script that declares its own dependencies

**Read more:** [uv: working on projects](https://docs.astral.sh/uv/guides/projects/) · [uv: running scripts](https://docs.astral.sh/uv/guides/scripts/) · [the Python tutorial on the interpreter](https://docs.python.org/3/tutorial/interpreter.html) · [VS Code: source control](https://code.visualstudio.com/docs/sourcecontrol/overview)

The toolkit works, and you know the loop: edit, run, commit. On to a proper program: [Project 1 · Hi-Lo](../part-1-console/p01-hi-lo.md).
