# Troubleshooting

When something doesn't work, it's usually one of a small number of things, and it's usually not your program. This page lists the ones that are about the computer, the tools and the set-up. For surprises in Python itself, see [the gotchas gallery](gotchas.md).

!!! bug "Not yet verified first-hand"
    This tutorial was written, and every command in it run, on macOS. Its code is tested on Windows and Linux as well, automatically, on every change. But the advice on this page about Windows and Linux comes from those tools' own documentation, and from experience of other people's computers, and hasn't been tried by the author on a fresh machine. If something here is wrong, or missing, please open an issue.

## First, always

1. **Read the last line of the error**, and then the line above it that mentions a file of yours. [Project 1](../part-1-console/p01-hi-lo.md).
2. **`git status`, and `git diff`.** What did you change since it last worked?
3. **Are you where you think you are?** `pwd` (or `cd`, alone, on Windows) and `ls` (`dir`). Half of all "file not found" errors are a terminal in the wrong folder.
4. **Close the terminal, and open a new one.** Anything that changed your `PATH` won't be seen by a terminal that was already open.
5. **Make it smaller.** Copy the few lines that misbehave into the REPL, or a new file, and take things away until it works.
6. **Search for the exact message**, in quotation marks, leaving out anything that's particular to you, such as file names.

## uv and Python

| What you see | What's probably happened | What to do |
|---|---|---|
| `uv: command not found`, or `'uv' is not recognized…` | uv isn't on your `PATH`, or this terminal is older than the installation | Open a new terminal. Then `uv self update`, or install it again, from [The toolkit](../part-0-switching-on/toolkit.md). On Windows, VS Code itself may need restarting |
| `python: command not found` | Nothing's wrong. With uv you don't need a `python` command | `uv run python`, and `uv run file.py` |
| On Windows, `python` opens the Microsoft Store | It's a shortcut that Windows provides | Ignore it, and use `uv run`. It can be switched off under **Settings → Apps → Advanced app settings → App execution aliases** |
| `No solution found when resolving dependencies` | Two things that you've asked for can't both be had, often because of `requires-python` | Read the message slowly. It's long, and it's precise: it says which requirement rules out which. [Project 27](../part-6-shipping/p27-ship-it.md) |
| `ModuleNotFoundError: No module named 'pygame'` | You ran the file with some other Python, and not the project's | `uv run file.py`, and not `python file.py`. In VS Code: **Python: Select Interpreter**, and choose the one in `.venv` |
| `ModuleNotFoundError` for your *own* package | The project isn't a package, or you're outside it, or the folder was renamed | Is there a `[build-system]` table in `pyproject.toml`? Then `uv sync`. [Project 5](../part-1-console/p05-colossal-cupboard.md) |
| `ImportError: cannot import name … (most likely due to a circular import)` | Two of your modules import each other | [Project 5](../part-1-console/p05-colossal-cupboard.md), on layering |
| `AttributeError: module 'random' has no attribute 'randint'`, with a hint about a file of yours | You have a file called `random.py` | Rename it, and delete any `__pycache__` beside it. [Project 2](../part-1-console/p02-turtle-sketchbook.md) |
| Everything about `.venv` is strange | It's been damaged, or moved, or made by another Python | Delete the `.venv` folder, and `uv sync`. It's disposable: "commit the recipe, and not the cake" |
| The project is inside OneDrive, Dropbox or iCloud Drive, and everything's slow, or files are "in use" | The syncing program is fighting over thousands of small files in `.venv` and `.git` | Keep your projects in a folder that isn't synced. Git and GitHub are your back-up |
| On Windows, a path is "too long" | Windows's old limit of 260 characters | Keep `making` near the top of the drive, such as `C:\making`. Long paths can be enabled, in Windows's settings, and in Git with `git config --global core.longpaths true` |

## VS Code

| What you see | What's probably happened | What to do |
|---|---|---|
| Imports are underlined, and the program runs perfectly well | VS Code is looking at a different Python from uv's | ++ctrl+shift+p++, **Python: Select Interpreter**, and choose `.venv`. Open the *project's* folder, and not the folder above it |
| No underlines at all, anywhere | The Python extension isn't installed, or the file isn't saved as `.py` | Look at the bottom right-hand corner: it should say "Python" |
| The Testing panel finds no tests | pytest isn't installed in this project, or there's an error when the tests are imported | `uv add --dev pytest`. Then `uv run pytest` in the terminal, which will show the real error |
| The debugger stops inside files that you didn't write | It's stepping into libraries | `"justMyCode": true` in `launch.json`, which is the default |
| Format on save does nothing | The Ruff extension isn't installed, or isn't the chosen formatter | [The toolkit](../part-0-switching-on/toolkit.md) has the settings |
| `code .` isn't found, on a Mac | The command has to be installed once | ++cmd+shift+p++, **Shell Command: Install 'code' command in PATH** |

## Git and GitHub

| What you see | What's probably happened | What to do |
|---|---|---|
| `Author identity unknown` | Git doesn't know your name | `git config --global user.name "Your Name"`, and the same for `user.email`. GitHub will give you a private `noreply` address to use there |
| `fatal: not a git repository` | You're in the wrong folder | `cd` into the project |
| `Updates were rejected because the remote contains work that you do not have` | Somebody, possibly you, on GitHub's web site, has committed there | `git pull`, and then `git push`. If it says that the histories have diverged, [Project 21](../part-4-web/p21-adventure-online.md) |
| You're asked for a user name and password, and your password is refused | GitHub stopped taking passwords in 2021 | `gh auth login`, and let `gh` set Git up. [Project 6](../part-1-console/p06-life.md) |
| `LF will be replaced by CRLF` | Windows ends lines differently, and Git is translating | It's a warning, and harmless. To stop it, a `.gitattributes` file with `* text=auto eol=lf` in it keeps line endings the same for everybody |
| You're in a strange editor, and can't get out | Git has opened Vim, for a commit message | ++esc++, then `:wq`, then ++enter++. And then `git config --global core.editor "code --wait"` |
| `detached HEAD` | You've checked out a commit, and not a branch | `git switch main`. If you've made commits there that you want, `git switch -c rescue` first. [Project 13](../part-2-pygame/p13-life-in-pixels.md) |
| You've committed something enormous, or secret | | Don't push. `git reset --soft HEAD~1` undoes the last commit and keeps your files. If it's been pushed, and it's a secret, **change the secret**. [Project 21](../part-4-web/p21-adventure-online.md) |

## Pygame

| What you see | What's probably happened | What to do |
|---|---|---|
| `AttributeError: module 'pygame' has no attribute 'FRect'`, or other oddities | Both `pygame` and `pygame-ce` are installed | `uv remove pygame`, and `uv add pygame-ce`. [Project 8](../part-2-pygame/p08-mode2-sketchpad.md) |
| The window opens, and "isn't responding" | The event queue isn't being read | Every frame must call `pygame.event.get()`. [Project 8](../part-2-pygame/p08-mode2-sketchpad.md) |
| A window opens behind everything, on a Mac | macOS doesn't always bring a new program's window to the front | Click its icon in the Dock |
| No sound | The mixer opened before your settings reached it. Or, on Linux, there's no sound server. Or, on WSL, there's no sound at all | [Project 11](../part-2-pygame/p11-sound-and-envelope.md). On WSL, run the games from Windows's own Python |
| In WSL, no window appears | Older WSL has no display | Windows 11's WSL shows Linux windows without any set-up. On Windows 10, use Windows's own Python for Part 2 |
| On Linux, `error: XDG_RUNTIME_DIR not set`, or Wayland complaints | SDL can't find the display server | `SDL_VIDEODRIVER=x11 uv run …` is the usual way round it |
| Tests open windows, or fail in CI with "No available video device" | The tests are using a real display | `SDL_VIDEODRIVER=dummy` and `SDL_AUDIODRIVER=dummy`, set in `conftest.py` before Pygame is imported. [Project 8](../part-2-pygame/p08-mode2-sketchpad.md) |
| It's slow | You're drawing text, or loading an image, in every frame | Make it once, and keep it. Then measure. Projects [9](../part-2-pygame/p09-snake.md) and [13](../part-2-pygame/p13-life-in-pixels.md) |

## turtle

| What you see | What's probably happened | What to do |
|---|---|---|
| `ModuleNotFoundError: No module named '_tkinter'` | This Python was built without Tk. It happens with some Linux distributions' own Pythons, and with Homebrew's | Use uv's Python, which has Tk in it: `uv python install 3.14`, and `uv run` |
| The window vanishes at once | The program ended | Finish with `screen.mainloop()`, or `turtle.done()`. [Project 2](../part-1-console/p02-turtle-sketchbook.md) |

## The web

| What you see | What's probably happened | What to do |
|---|---|---|
| `Address already in use` | Another program, probably an earlier run of yours, has the port | Find its terminal, and press ++ctrl+c++. Or choose another: `flask run --port 5001`. On a Mac, port 5000 is taken by AirPlay Receiver, which can be switched off in **System Settings → General → AirDrop & Handoff** |
| A firewall asks whether Python may accept connections | It's your own server | For these projects, which only your own computer visits, either answer will do |
| You changed the CSS, and nothing happened | The browser is showing you the copy that it kept | Reload with ++ctrl+shift+r++. Or open the developer tools, and tick "Disable cache" |
| `TemplateNotFound` | The `templates` folder isn't where Flask is looking | It belongs *inside* the package, beside `__init__.py`. [Project 20](../part-4-web/p20-pyfax-live.md) |
| 403 on every form | The CSRF token is missing from the form, or the session cookie isn't being kept | [Project 21](../part-4-web/p21-adventure-online.md) |
| htmx does nothing, and the console mentions a Content Security Policy | The policy is doing its job | [Project 21](../part-4-web/p21-adventure-online.md), on `allowEval` |

## The terminal

| What you see | What's probably happened | What to do |
|---|---|---|
| Empty boxes, or question marks, where Project 24's graphics should be | Your terminal's font hasn't those characters | `--glyphs quadrant`, or `--glyphs braille`. Or a font that has them: recent versions of Cascadia Code, and Iosevka, do. [Project 24](../part-5-tui/p24-teletext-viewer.md) |
| Colours are wrong, or missing, in Rich or Textual | An old terminal. macOS's own Terminal had only 256 colours for many years | Windows Terminal, iTerm2, WezTerm, Ghostty and VS Code's own are all good |
| On Windows, `é` comes out as `Ã©`, or a `UnicodeEncodeError` on `print` | An old console, in an old code page | Use Windows Terminal. Always pass `encoding="utf-8"` when opening files. From Python 3.15 this goes away |
| Textual's keys do nothing in VS Code's terminal | VS Code has taken the key for itself | Run it in a terminal of its own, or press the key after ++ctrl+k++. Function keys on a laptop may need ++fn++ |
| A snapshot test fails on somebody else's computer, and looks identical | It isn't, quite: a different version of Textual draws a pixel differently | Pin Textual, as [Project 24](../part-5-tui/p24-teletext-viewer.md) did, and update the snapshots together with the version |

## Still stuck?

Write the problem down, for somebody else, in full: what you did, what you expected, and what happened, with the complete error. Most of the time you'll see the answer before you've finished writing. It's called *rubber-duck debugging*, and it works on a duck.

If it doesn't, you now have a good question, and the places to ask it are the [Python Discourse](https://discuss.python.org/), in its Help category, the Python Discord, and, for a problem with this tutorial, its issues page on GitHub.
