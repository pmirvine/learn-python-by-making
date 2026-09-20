# The toolkit

A BBC Micro came with everything in the box: language, editor, graphics, sound. Switch on, and there was the `>` prompt. Today you assemble the box yourself. It takes about half an hour, you do it once, and what you end up with is the same kit professional Python developers use.

There are four things to set up.

| Tool | What it's for |
|---|---|
| **A terminal** | Where you type commands. You already have one. |
| **uv** | Installs Python, creates projects, fetches libraries, and runs your programs. |
| **Git** | Keeps the history of your code, so you can experiment without fear. |
| **Visual Studio Code** | The editor: where you'll write, run and debug. |

!!! bug "Not yet verified first-hand"
    The macOS instructions on this page have been tested. The Windows and Linux instructions are taken from each tool's official documentation and have not yet been run by the author. If something doesn't match what you see, the linked installation pages are the authority, and a correction would be very welcome.

## A terminal

The terminal is a window where you type commands and read replies. If you grew up with a `>` prompt, you're home.

=== "macOS"

    Open **Terminal**: press ++cmd+space++, type `Terminal`, press ++enter++.

=== "Windows"

    Open **Terminal**: press the ++windows++ key, type `Terminal`, press ++enter++. It opens PowerShell, which is what these instructions assume. On Windows 10, install *Windows Terminal* from the Microsoft Store first, or use the *PowerShell* app.

=== "Linux"

    Open your distribution's terminal. On most desktops, ++ctrl+alt+t++ does it.

You need five commands, and they're the same on all three systems.

| Command | What it does |
|---|---|
| `pwd` | Print the folder you're in ("print working directory") |
| `ls` | List what's in it |
| `cd making` | Change into the folder `making` |
| `cd ..` | Go up to the folder above |
| `mkdir making` | Make a new folder called `making` |

Two habits will save you a lot of typing. Press ++tab++ part-way through a file or folder name and the terminal finishes it for you. Press ++up++ to bring back previous commands.

Make a folder to hold everything you build in this tutorial, and go into it:

```console
$ mkdir making
$ cd making
```

Throughout the tutorial the `$` stands for your prompt, whatever it looks like. Don't type it.

## uv, and Python

You might expect the first step to be "install Python". It isn't, quite. You install **uv**, and uv installs Python, along with everything else Python-related you'll need.

=== "macOS"

    ```console
    $ curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    If you use [Homebrew](https://brew.sh), `brew install uv` works too.

=== "Windows"

    ```console
    $ powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

    Or, with the Windows package manager: `winget install --id=astral-sh.uv -e`.

=== "Linux"

    ```console
    $ curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

**Close the terminal and open a new one**, so that it notices the new command. Then check:

```console
$ uv --version
uv 0.12.17
```

Your version number will be higher than that one. It needs to be at least **0.12**, because that release changed what a new project looks like. If yours is older, `uv self update` brings it up to date. ([uv's installation guide](https://docs.astral.sh/uv/getting-started/installation/) has more options.)

Now ask uv for a Python:

```console
$ uv python install 3.14
```

That's Python installed. It lives in a folder that uv manages, and it won't disturb, or be disturbed by, any other Python on your computer.

!!! info "Coming from an earlier encounter with Python"
    If you've used Python before, you may be wondering where `pip`, `venv`, `pyenv`, `pipx` and perhaps Poetry have gone. uv does all their jobs with one fast tool, and since 2024 much of the Python world has moved to it. Underneath, it uses the same standards they do: a `pyproject.toml` file and a `.venv` folder. Project 27 shows you the older tools, because you'll meet them in other people's projects.

!!! note "Under the bonnet"
    Notice that you won't type `python` to run things. Your system may have no command by that name, or, worse, one that starts some other, elderly Python. You'll type `uv run`, which starts the right Python for the project you're in, with the right libraries to hand. "Which Python am I actually running?" has wasted more beginners' afternoons than any feature of the language. With `uv run`, the question never comes up.

## Git

Git records snapshots of your project as you go. Every snapshot stays. You can see what changed and when, go back to any point, and try a wild idea knowing you can always get home. You'll start using it in Project 0, and by Part 2 it'll be second nature.

You may already have it. Try:

```console
$ git --version
git version 2.55.0
```

Any version from 2.28 onwards is fine. If you get an error instead, install it:

=== "macOS"

    Running `git --version` on a Mac without Git pops up an offer to install Apple's *Command Line Tools*. Accept it, wait, and try again. (Or `brew install git`, if you use Homebrew.)

=== "Windows"

    ```console
    $ winget install --id Git.Git -e --source winget
    ```

    Or download the installer from [git-scm.com](https://git-scm.com/downloads/win); its suggested settings are fine. Open a new terminal afterwards.

=== "Linux"

    On Debian, Ubuntu and relatives:

    ```console
    $ sudo apt install git
    ```

    On Fedora: `sudo dnf install git`. Others are listed at [git-scm.com](https://git-scm.com/downloads/linux).

Then introduce yourself. Git signs every snapshot with a name and an email address, and won't take one without them. Use your own:

```console
$ git config --global user.name "Ada Lovelace"
$ git config --global user.email "ada@example.com"
$ git config --global init.defaultBranch main
```

The third line asks Git to call the first branch of each new project `main`, which is what everyone now does, rather than its historical default. You'll find out what a branch is in Project 5.

## Visual Studio Code

You could write Python in Notepad. But a good editor colours your code so that mistakes stand out, completes names as you type, underlines problems before you run anything, and lets you pause a running program to look inside it. Visual Studio Code, *VS Code* from here on, is free, runs everywhere, and is what most Python developers use.

=== "macOS"

    Download it from [code.visualstudio.com](https://code.visualstudio.com/), unzip it, and drag **Visual Studio Code** into your **Applications** folder. (Or `brew install --cask visual-studio-code`.)

    Then open it, press ++cmd+shift+p++ to bring up the *Command Palette*, type `shell command`, and choose **Shell Command: Install 'code' command in PATH**. Now you can open a folder in VS Code from the terminal.

=== "Windows"

    ```console
    $ winget install -e --id Microsoft.VisualStudioCode
    ```

    Or download the installer from [code.visualstudio.com](https://code.visualstudio.com/). Leave **Add to PATH** ticked. Open a new terminal afterwards.

=== "Linux"

    Download the `.deb` or `.rpm` package from [code.visualstudio.com](https://code.visualstudio.com/) and install it, or, where snaps are available:

    ```console
    $ sudo snap install --classic code
    ```

Check that the terminal can find it:

```console
$ code --version
```

### Extensions

Out of the box, VS Code knows nothing about Python. *Extensions* teach it. Install these four from the terminal:

```console
$ code --install-extension ms-python.python
$ code --install-extension charliermarsh.ruff
$ code --install-extension usernamehw.errorlens
$ code --install-extension tamasfe.even-better-toml
```

(You can also click the Extensions icon in the left-hand bar, the four squares, and search for each by name.)

| Extension | What it does |
|---|---|
| **Python** (Microsoft) | The big one. It brings three more along with it: **Pylance**, which understands your code, and so completes names, shows documentation and finds mistakes; **Python Debugger**; and **Python Environments**, which finds the Python belonging to each project. |
| **Ruff** | Formats your code every time you save, and flags likely bugs and clumsy style. Ruff comes from the makers of uv. |
| **Error Lens** | Puts each error message at the end of the line it's about, instead of hiding it behind a squiggle you have to hover over. |
| **Even Better TOML** | Python projects are configured in TOML files. This makes them pleasant to edit. |

More will arrive as projects call for them.

### Settings

A few settings make life better. Press ++ctrl+shift+p++ (++cmd+shift+p++ on a Mac), type `user settings json`, and choose **Preferences: Open User Settings (JSON)**. Make the file look like this, keeping anything already in it:

```json
{
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },
    "editor.rulers": [88],
    "files.insertFinalNewline": true,
    "files.trimTrailingWhitespace": true,
    "chat.disableAIFeatures": true
}
```

In order, those settings:

- make Ruff tidy your Python every time you save, and sort the `import` lines at the top while it's about it. Python programmers gave up arguing about layout some time ago: you let the formatter decide, and think about something more interesting;
- draw a faint line at column 88, which is where Ruff wraps long lines;
- keep files neat in two small ways that Git cares about;
- switch off AI code completion, for the reasons in [How to use this tutorial](how-to-use.md#a-word-about-ai-assistants). To switch it off for this tutorial only, leave that line out here and put it in the *workspace* settings of each project instead: **Preferences: Open Workspace Settings (JSON)**.

## Check the box

One last look before you begin. All three of these should answer with a version number:

```console
$ uv --version
$ git --version
$ code --version
```

And this should start Python, say hello, and stop:

```console
$ uv run --no-project python -c "print('Hello from Python')"
Hello from Python
```

If anything doesn't answer, the usual cure is to close the terminal and open a new one. Failing that, check that tool's installation page, linked above.

Everything's in the box. [Time to switch on](p00-hello-beeb.md).
