# Roadmap

Twenty-eight projects in six parts. Do them in order: each leans on the ones before, and some come back later in a new form.

Projects marked :material-check: are written. The rest are on their way.

## Three projects that keep coming back

The same ideas return in each medium, so you feel what good structure buys you.

- **Life** runs in the terminal (Project 6), then in Pygame (13), reusing the same core untouched.
- **The text adventure** starts in the console (5), moves to the web (21), then to a full-screen terminal app (26). One engine, three front ends.
- **Teletext**: one page model is rendered as HTML (19–20), in the terminal (24), and finally as the text screen of the capstone computer (28).

## Part 0 · Switching on

| | Project | What it's for |
|---|---|---|
| :material-check: | [How to use this tutorial](part-0-switching-on/how-to-use.md) | The furniture: callouts, challenges, and a word on AI assistants |
| :material-check: | [The toolkit](part-0-switching-on/toolkit.md) | uv, Python, Git and VS Code, on macOS, Windows and Linux |
| :material-check: | [0 · Hello, Beeb](part-0-switching-on/p00-hello-beeb.md) | First project, first run, first commit |

## Part 1 · Console: the core of the language

| | Project | Python you learn | Tool skill |
|---|---|---|---|
| :material-check: | [1 · Hi-Lo](part-1-console/p01-hi-lo.md) — guess the number | Names and objects, core types, f-strings, `while`, truthiness, first exceptions | The commit rhythm; reading tracebacks |
| :material-check: | [2 · Turtle Sketchbook](part-1-console/p02-turtle-sketchbook.md) — spirographs and fractal trees | `for` and `range`, functions in depth, tuples, recursion | The debugger |
| :material-check: | [3 · Dice Lab](part-1-console/p03-dice-lab.md) — probability with text histograms | Lists, dicts, `Counter`, comprehensions, slicing, type hints | pytest; ruff |
| :material-check: | [4 · Codebreaker](part-1-console/p04-codebreaker.md) — Mastermind meets Wordle, in colour | Strings and Unicode, sets, mutability and aliasing, `is` and `==` | Undoing things in Git; first bug hunt |
| :material-check: | [5 · The Colossal Cupboard](part-1-console/p05-colossal-cupboard.md) — a text adventure | Dataclasses, enums, `match`, modules, exceptions, files and JSON | Packaged layout; branches |
| :material-check: | [6 · Life](part-1-console/p06-life.md) — Conway's Game of Life in the terminal | Sets of tuples, generators, itertools, command-line arguments | GitHub; parametrised tests |
| :material-check: | [7 · Fractal Factory](part-1-console/p07-fractal-factory.md) — Mandelbrot and friends, to PNG | Numbers in depth, first-class functions, closures, `*args` and `**kwargs` | Profiling; tags |

## Part 2 · Pygame: objects in motion

| | Project | Python you learn | Tool skill |
|---|---|---|---|
| :material-check: | [8 · Mode 2 Sketchpad](part-2-pygame/p08-mode2-sketchpad.md) — your own `MOVE` and `DRAW` | The game loop, events, surfaces; module-level state and why it hurts | Debugging a running game |
| :material-check: | [9 · Snake](part-2-pygame/p09-snake.md) | First classes, `deque`, enums, game states | Stash; `.gitignore` |
| :material-check: | [10 · Breakout](part-2-pygame/p10-breakout.md) | Classes in depth: composition, properties, class methods, frozen dataclasses | Refactoring tools |
| :material-check: | [11 · SOUND & ENVELOPE](part-2-pygame/p11-sound-and-envelope.md) — a tone synth and piano | Binary data, generators as oscillators, packages that depend on packages | Path dependencies; workspaces |
| | 12 · Asteroids | The data model: a `Vector` with dunder methods; duck typing and `Protocol` | Merge conflicts |
| | 13 · Life in Pixels | Reusing Project 6; parsing; profiling and optimisation | `git bisect` |
| | 14 · Wireframe — a rotating 3D ship viewer | Matrices from `zip` and comprehensions, `@`, `__slots__`, `tomllib` | Snippets and tasks |
| | 15 · Sprite Editor — with undo and redo | Event architecture, the command pattern, inheritance and ABCs, logging | Conditional breakpoints |
| | ★ Side quest: Pyxel | A fantasy console in fifty lines | |

## Part 3 · Interpreters: Python looks at language

| | Project | Python you learn | Tool skill |
|---|---|---|---|
| | 16 · Logo — a turtle language | Tokenisers as generators, recursive descent, decorators, `raise … from` | Pull requests |
| | 17 · Tiny BASIC — `10 PRINT "HELLO"` | ASTs with dataclasses and structural `match`, typing in depth, context managers | Coverage; CI; building and installing a tool |

## Part 4 · Web: pages as pictures

| | Project | Python you learn | Tool skill |
|---|---|---|---|
| | 18 · SVG Plotter — `MOVE` and `DRAW` for the browser | f-strings, t-strings and escaping; writing a context manager | Live Preview |
| | 19 · PyFax — a teletext-style site generator | The 40×25 page model, bit operations, Jinja2, CSS basics | GitHub Pages |
| | 20 · PyFax Live — Flask | Routes, forms, sqlite3, fetching live data, configuration and secrets | Fixtures; debugging Flask |
| | 21 · Adventure Online — Flask and htmx | Sessions, partial pages, reusing the Project 5 engine, web security basics | Rebase |
| | 22 · High Score Server — FastAPI | Type hints at runtime, first `async def`; your games post their scores | API tests; releases |
| | ★ Bonus: Share it | Python in the browser with PyScript and pygbag | |

## Part 5 · TUI: the terminal strikes back

| | Project | Python you learn | Tool skill |
|---|---|---|---|
| | 23 · Rich Dashboard — statistics across all your projects | `subprocess`, `datetime`, `collections`, sort keys | |
| | 24 · Teletext Viewer — Textual | Widgets, messages, reactive attributes, and the descriptors behind them | Snapshot tests |
| | 25 · Newsroom — an async feeds client | asyncio properly: tasks, `TaskGroup`, exception groups; threads, processes and the GIL | Async tests |
| | 26 · Adventure, Third Edition — Textual | One engine, three front ends: `Protocol` or ABC, and which way dependencies point | |

## Part 6 · Shipping it

| | Project | What happens |
|---|---|---|
| | 27 · Ship It | `pyproject.toml` in depth, versioning, building, publishing, releases, CI on three operating systems |
| | 28 · Capstone: boot to BASIC | A Pygame computer with a teletext-style screen that boots to a `>` prompt. Your Project 17 BASIC gains `MOVE`, `DRAW`, `PLOT`, `SOUND` and `ENVELOPE`, plus sprites with collision detection, loaded from your Project 15 sprite editor. Type in a game and `RUN` it. |
| | Where next | Unguided briefs: a roguelike, a multiplayer game server, a deployed news service, and a 6502 emulator for the brave |

## Appendices

Python for BBC BASIC programmers · sheets for people coming from JavaScript, C#, Java and C · the gotchas gallery · Git, uv and VS Code cheat sheets · an index of which project teaches what · troubleshooting · glossary.
