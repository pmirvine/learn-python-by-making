# Learn Python by Making — plan

*Status: complete. Plan approved 20 September 2026; the pilot (Stage A) was reviewed and approved; every chapter, the briefs and the appendices are now written. See §10 for what the pilot changed, `LEDGER.md` for what each chapter actually taught, and the README for what hasn't been verified first-hand.*

A project-based Python tutorial for people who can already program a little but are new to Python, and who want a thorough grasp of the language *and* of professional practice (Git, VS Code, uv, testing, typing, packaging). Every project produces something you can see or hear, in the spirit of typing `MOVE`, `DRAW` and `SOUND` into a BBC Micro.

## 1. Decisions so far

| Question | Your answer |
|---|---|
| Delivery | Markdown chapters + runnable project code in this repo, plus a docs site |
| Platforms | macOS, Windows and Linux |
| Scale | 20+ projects (this plan has 28, plus a side quest and unguided briefs) |
| Retro flavour | Strong BBC Micro thread throughout |
| Audience | Public, open source (GitHub + GitHub Pages) |
| Spelling | British English in prose; code follows library conventions (`color`) |
| Cadence | Pilot first → your review → then I write everything else straight through |
| Capstone | Guided "boot to BASIC" fantasy micro, **and** a chapter of unguided briefs |

## 2. What the research found

Three research passes (tooling, visual libraries, pedagogy), plus first-hand checks on this Mac.

**The gap.** No existing resource combines all four of: pacing for experienced programmers; one project spine running across console → Pygame → web → TUI; Fluent-Python-level idiom; and professional workflow from the first project. *Python Crash Course* is novice-paced with three disconnected projects; *Fluent Python* and *Python Distilled* have the depth but no projects or tooling; Pygame YouTube tutorials have the fun but global state and no tests. Nothing targets Python 3.14+.

**Pedagogy worth adopting** (each has decent evidence and suits written, self-paced material):

- **PRIMM** (Predict–Run–Investigate–Modify–Make): open sections with "predict the output" snippets — ideally the classic gotchas.
- **Language-transfer callouts**: a study of Stack Overflow questions found most confusion in a second language comes from assumptions carried over from the first. Hence "Coming from BBC BASIC / JavaScript / C# / C…" boxes.
- **Expertise reversal**: heavy scaffolding *slows* competent learners. Keep walkthroughs brisk, mark basics skippable, fade guidance within each part.
- **Use–Modify–Create** → three challenge tiers. **Debugging exercises** → a deliberately broken file per chapter: write a failing test, then fix it.
- **Spiral curriculum**: revisit the same idea in each medium (see "spiral projects" below).

**Tooling facts that change what a 2026 tutorial should say:**

- **Python**: 3.14.7 is current; 3.15 final is due 1 October 2026. Target **3.14**, `requires-python = ">=3.13"`, with "new in 3.15" sidebars. 3.13/3.14 bring the new colour REPL, far better error messages, t-strings and deferred annotations — all learner-relevant.
- **uv** is the right default (with a "pip and venv, for when you meet them" appendix). ⚠️ Since uv 0.12 (July 2026) `uv init` creates a *packaged* `src/` project by default; the flat `main.py` layout now needs `--no-package`. The tutorial must state a minimum uv version. This Mac has 0.11.7, so I'd update it first.
- **ruff** 0.16 (July 2026) raised its default rule set from 59 to 413 rules. I'd start learners on a small explicit rule set and widen it at marked points.
- **Type checking**: Pylance in VS Code (`basic` → `standard` → `strict` as the tutorial progresses). Astral's `ty` is still beta with no stable API — a sidebar, not the main tool.
- **pytest 9** (config now lives in `[tool.pytest]`), **Git** taught with `switch`/`restore`, `main` as default branch, and the `gh` CLI to skip SSH-key pain.
- **VS Code**: the Python extension now bundles Pylance, the debugger and the Python Environments extension (which uses uv automatically). Add Ruff, Error Lens, Even Better TOML; later Jinja, Textual and GitHub extensions as they become relevant.

**Library choices:**

| Area | Choice | Why |
|---|---|---|
| Games | **pygame-ce** 2.5.8 | Classic `pygame` has had no release in two years and has no wheels past 3.13. pygame-ce is active, same `import pygame`, and adds `FRect`, `flood_fill` etc. Must never be installed alongside `pygame`. |
| First graphics | stdlib **turtle** | Zero install; the closest thing to `MOVE`/`DRAW`. Verified working with uv's Python 3.14 / Tk 9 here. |
| Side quest | **Pyxel** 2.9 | A 16-colour, 4-channel "fantasy console" — very BBC Micro in spirit. One short optional chapter. |
| Excluded | Pygame Zero, Arcade, Django | pgzero is unmaintained and conflicts with pygame-ce; Arcade is mid-rewrite; Django is too heavy for "visual feedback". |
| TUI | **Rich** 15 → **Textual** 8.x (pinned `>=8,<9`) | Best in class. Note: Textualize the company wound down in 2025 and releases have been quiet since June 2026 — still the right choice, but worth pinning. |
| Web | SVG → Jinja2 static pages → **Flask** 3.1 → **htmx 2** → **FastAPI** | A gentle ramp. htmx 4 exists (Aug 2026) but is tagged `next`; teach 2.x, pinned. PyScript/pygbag only as a flagged-fragile "share it" bonus. |
| Images/sound | **Pillow** 12, **numpy** 2.5, `pygame.mixer` | Verified: tones can be synthesised from arrays with or without numpy. |
| Docs site | **Zensical** | Successor to Material for MkDocs by the same team (Material is maintenance-only, end of life May 2027). Still alpha (0.0.63; 0.1.0 due 5 Nov 2026) but I scaffolded and built a site here without trouble. Fallback: the content is standard Python-Markdown and also builds with mkdocs-material. |

Verified installing and importing together on Python 3.14.4 on this machine: pygame-ce 2.5.8, Textual 8.2.8, Rich 15.0.0, Flask 3.1.3, pytest 9.1.1, numpy 2.5.3, Pillow 12.3.0. Pygame renders headlessly (SDL dummy driver), so game code can be tested automatically.

## 3. Suggestions

1. **Three spiral projects.** The same ideas return in each medium, so the reader feels the payoff of good structure:
   - *Life*: terminal (P6) → Pygame (P13), reusing the same core package.
   - *Text adventure*: console (P5) → web (P21) → TUI (P26). One engine, three front ends.
   - *Teletext*: one page model rendered as HTML (P19–20), in Textual (P24), and as the Mode 7 screen of the capstone (P28).
2. **A `beeb` module.** In P8 the reader writes `MOVE`, `DRAW`, `PLOT`, `GCOL`, `CLS` on top of Pygame — complete with the BBC's 1280×1024 bottom-left-origin coordinates. P11 adds `SOUND` and `ENVELOPE`. The capstone wires both into their own BASIC interpreter.
3. **Type-in listings.** Each chapter ends with a ≤30-line "magazine listing" to type in, run and puzzle out — the PRIMM "Investigate" step, in period costume.
4. **"Pythonic" before/after boxes.** Show the code an experienced programmer would naturally write (index loops, getters, flag variables), then the idiomatic version, and say *why*.
5. **Tooling is threaded, not front-loaded.** Part 0 installs things; after that each chapter introduces exactly one new Git skill and one new editor/tool skill, when the project needs it (see §5).
6. **A stance on AI assistants.** A short section in "How to use this tutorial": switch off inline AI completions while working through chapters and challenges; use an assistant as a tutor that explains errors, not one that writes the answer.
7. **CI on three operating systems.** I can only run things on your Mac. Since the repo will be public, a GitHub Actions matrix (macOS/Windows/Linux) can test every project's code on all three. Setup *instructions* for Windows/Linux will still come from official docs rather than first-hand testing, and I'll mark them so.
8. **Names and trademarks.** "BBC", "Ceefax" and "Elite" are trademarks. I'd refer to the originals by name where describing history, but give our projects their own names ("PyFax", "Wireframe") and use original ship models rather than Elite's blueprint data.
9. **Licence.** CC BY-SA 4.0 for prose, MIT for code — say if you'd prefer something else.

## 4. Curriculum

Each project is a chapter. **Bold** concepts are the chapter's main event. Guidance fades within each part: the last project of a part is more spec than walkthrough.

### Part 0 — Switching on
- **How to use this tutorial** — PRIMM, challenge tiers, callout types, AI stance.
- **The toolkit** — install uv (and Python through it), Git, VS Code + extensions; per-OS tabs; just enough terminal.
- **P0 · Hello, Beeb** — `uv init`, `uv run`, a tour of the new REPL, a single-file script with inline dependencies (PEP 723), first commit from both terminal and VS Code.

### Part 1 — Console: the core of the language
| # | Project | Python concepts | Git / tool skill |
|---|---|---|---|
| 1 | **Hi-Lo** — guess the number | **names bind to objects**, core types, `input`/f-strings, `if`/`while`, truthiness, `import`, reading tracebacks | commit rhythm; `status`/`diff`/`log` |
| 2 | **Turtle Sketchbook** — spirographs, fractal trees | `for`/`range`, **functions** (defaults, keyword args), tuples and unpacking, recursion, docstrings | VS Code debugger: step through recursion |
| 3 | **Dice Lab** — probability experiments with text histograms | **lists, dicts**, `Counter`, `enumerate`/`zip`/`sorted`, **comprehensions**, slicing, first type hints | first **pytest** tests; Test Explorer; ruff |
| 4 | **Codebreaker** — Mastermind-meets-Wordle in colour | strings and Unicode, sets, **mutability and aliasing**, `is` vs `==`, copying, Rich, `if __name__ == "__main__"` | `restore`, `commit --amend`; Pylance `basic`; first bug hunt |
| 5 | **The Colossal Cupboard** — text adventure | **dataclasses**, enums, **`match`**, modules, **exceptions and EAFP**, `with`, pathlib, JSON saves | packaged `src/` layout; **branches** and merging |
| 6 | **Life** — Conway in the terminal | sets of tuples, **generators**, itertools, argparse, packages and entry points, separating logic from display | GitHub remote, `gh`, README; parametrised tests |
| 7 | **Fractal Factory** — Mandelbrot, Julia and plasma to PNG | numbers in depth (`complex`, int/float traps), **first-class functions, closures**, late binding, `*args`/`**kwargs`, `functools.cache` | profiling (`timeit`, cProfile); tags |

### Part 2 — Pygame: objects in motion
| # | Project | Python concepts | Git / tool skill |
|---|---|---|---|
| 8 | **Mode 2 Sketchpad** — the `beeb` graphics module, bouncing lines, a paint program | the game loop, events, surfaces; module-level state and why it hurts | `launch.json`; debugging a running game |
| 9 | **Snake** | **first classes**, `__init__`, instance vs class attributes, `deque`, enums, game states | stash; `.gitignore` in depth |
| 10 | **Breakout** | **classes in depth**: composition, properties, `__repr__`, class methods as alternative constructors, frozen dataclasses, levels from files | refactoring tools (rename, extract) |
| 11 | **SOUND & ENVELOPE** — a tone synth and keyboard piano | bytes and binary data, `array`/numpy, generators as oscillators, ADSR dataclass; reuse via local package dependencies | uv workspaces / path dependencies |
| 12 | **Asteroids** | **the data model**: write a `Vector` with dunder methods, then meet `pygame.Vector2`; **duck typing and `Protocol`**; dt physics; generators for waves; scene state machine | Pylance `standard`; resolving a merge conflict |
| 13 | **Life in Pixels** | reuse the P6 core as a dependency; parsing pattern files; profiling and optimisation; numpy as a stretch | `git bisect` on a planted bug |
| 14 | **Wireframe** — a rotating 3D ship viewer | matrices with `zip` and comprehensions, `__matmul__` (`@`), `__slots__`, `tomllib`, back-face culling | snippets and tasks |
| 15 | **Sprite Editor** — with undo/redo | event architecture, callbacks, command pattern, **inheritance and ABCs** (and when not to), logging, file formats | logging vs print; conditional breakpoints |
| ★ | *Side quest: Pyxel* — a fantasy console in 50 lines | a different take on update/draw; reading unfamiliar API docs | — |

### Part 3 — Interpreters: Python looks at language
| # | Project | Python concepts | Git / tool skill |
|---|---|---|---|
| 16 | **Logo** — a turtle language | tokeniser as generator, recursive descent, **decorators** (a command registry, `functools.wraps`), `raise … from`, a renderer `Protocol` (turtle, Pygame or SVG) | pull requests against your own repo |
| 17 | **Tiny BASIC** — `10 PRINT "HELLO"` / `20 GOTO 10` | AST as dataclasses + **structural `match`**, precedence climbing, **typing in depth** (unions, `type` aliases, PEP 695 generics, `TypedDict`), class-based iterators, context managers with `contextlib` | coverage; **GitHub Actions CI**; `uv build`, `uv tool install`; Pylance `strict` |

### Part 4 — Web: pages as pictures
| # | Project | Python concepts | Git / tool skill |
|---|---|---|---|
| 18 | **SVG Plotter** — `MOVE`/`DRAW` for the browser | string building, f-strings vs **t-strings** and escaping, writing a `@contextmanager`, `http.server`, `webbrowser` | Live Preview |
| 19 | **PyFax** — a teletext-style static site generator | the 40×25 page model, **bit operations** (2×3 block graphics), Jinja2, CSS basics, TOML/Markdown content, pathlib globbing | GitHub Pages deployment |
| 20 | **PyFax Live** — Flask | routes (decorators in the wild), forms, **sqlite3** and transactions, app factory, `httpx` + a keyless weather API, caching, config and secrets | pytest fixtures and test client; debugging Flask |
| 21 | **Adventure Online** — Flask + htmx | sessions, partial rendering, reusing the P5 engine, web security basics | `.env` handling; rebase |
| 22 | **High Score Server** — FastAPI | **type hints at runtime** (pydantic), first `async def`, OpenAPI docs; Pygame games post scores; leaderboard on a `<canvas>` | API tests; releases |
| ★ | *Bonus: Share it* — PyScript / pygbag | running Python in the browser (flagged: fragile tooling) | — |

### Part 5 — TUI: the terminal strikes back
| # | Project | Python concepts | Git / tool skill |
|---|---|---|---|
| 23 | **Rich Dashboard** — stats across all your tutorial repos | `subprocess`, `datetime`, `collections`, sort keys and `operator`, Rich tables/Live | — |
| 24 | **Teletext Viewer** — Textual | App/compose/TCSS, messages, key bindings, reactive attributes → **descriptors** explained | `textual run --dev`; snapshot tests |
| 25 | **Newsroom** — async feeds client | **asyncio** properly: tasks, `TaskGroup`, **exception groups**, workers, async `httpx`; threads vs processes vs async, the GIL and free-threading | Pilot tests with pytest-asyncio |
| 26 | **Adventure, Third Edition** — Textual | one engine, three front ends: `Protocol` vs ABC, dependency direction, what good structure buys you | — |

### Part 6 — Shipping it
- **P27 · Ship It** — `pyproject.toml` in depth, versioning, changelog, `uv build`, TestPyPI, GitHub Releases, CI matrix, pre-commit hooks, licences; pip/venv for when you meet them.
- **P28 · Capstone: boot to BASIC** — a Pygame "micro" with a Mode 7 text screen and line editor that boots to a `>` prompt. The P17 interpreter gains `MOVE`, `DRAW`, `GCOL`, `PLOT`, `SOUND`, `ENVELOPE` via the `beeb` module and synth, plus `SAVE`/`LOAD`. Type in listings and `RUN` them. Packaged, tested, CI'd, released.
  - **Sprites** (added at plan review): the micro gets a hardware-style sprite layer the BBC never had. BASIC statements to define, show, move and hide sprites; sprites are drawn over the graphics screen without disturbing it; collision detection between sprites (bounding box, then pixel-perfect via `pygame.mask`) and against the screen edge, exposed to BASIC as functions (e.g. `COLLIDE(a, b)`). Sprite images are loaded from files made with the **P15 Sprite Editor**, which makes P15 load-bearing rather than a candidate to cut. The chapter ends with a complete type-in game written in the reader's own BASIC.
- **Where next: briefs** — spec-only projects: a roguelike, an asyncio multiplayer game server, a deployed teletext news service, a Pyxel demake, and (for the brave) a 6502 emulator.

### Appendices
Python for BBC BASIC programmers (a Rosetta stone: `PROC`/`FN`/`DIM`/`REPEAT…UNTIL` → Python) · "Coming from JavaScript / C# / Java / C" sheets · the gotchas gallery · Git, uv and VS Code cheat sheets · concept index (which project teaches what) · per-OS troubleshooting · glossary · what's new in 3.15.

**Concept coverage check.** Against the checklist compiled from the Python FAQ, *Fluent Python*, *Beyond the Basic Stuff* and Exercism's concept tree, every item has a home above: object model (P1, P4), data types (P3, P4, P7, P11), iteration (P3, P6), functions (P2, P7, P16), classes and data model (P9–12, P15, P24), control flow and errors (P5, P17, P25), organisation and tooling (P5, P6, P17, P27).

## 5. Chapter template

1. **Header** — screenshot of the finished thing, concepts, the new tool skill, time estimate, prerequisites.
2. **Predict** — two to four short snippets; guess the output before running. Answers collapsed.
3. **Build** — in stages. Each stage ends with *Run it*, *what you should see*, and a *Checkpoint: commit*.
4. **Callouts** along the way — *Coming from…*, *Under the bonnet* (how it really works), *Gotcha*, *Pythonic* (before/after).
5. **Type-in listing** — run it, then work out how.
6. **Bug hunt** (from P4) — a broken file: write a failing test, then fix it.
7. **Challenges** — *Tweak* (10 minutes, modify), *Extend* (an hour, new feature, hints collapsed), *Invent* (spec only).
8. **Recap** — concept checklist, what joined your toolbox, links to the official docs.

## 6. Repository layout

```
README.md  LICENSE  PLAN.md  STYLE.md
zensical.toml
docs/
  index.md
  part-0-switching-on/ … part-6-shipping/     one .md per chapter
  appendices/
  assets/                                     screenshots, generated by script
projects/
  01-hi-lo/                                   a standalone uv project, as the reader would create it
    pyproject.toml  uv.lock  src/ or main.py  tests/
    stages/                                   runnable snapshot per checkpoint
    bughunt/                                  the broken file
    solutions/                                Tweak and Extend solutions
  02-turtle-sketchbook/ …
scripts/
  check_all.py                                ruff + pytest + stage smoke tests across every project
  screenshots.py                              regenerate docs/assets headlessly
.github/workflows/                            CI on macOS/Windows/Linux; docs deploy
```

## 7. How I'll keep it correct

- **Code first.** I build and test each project, then write the chapter around working code. Chapter listings are pulled from the real files (snippet includes, or a checker script if Zensical's support falls short) so prose and code cannot drift.
- **Everything runs.** Pygame under the SDL dummy driver; Textual via its Pilot harness; Flask and FastAPI via test clients; every `stages/` snapshot smoke-tested.
- **Screenshots are generated**, not hand-captured: `pygame.image.save`, Textual SVG export, Pillow output.
- **Honest labelling.** Anything I could not verify first-hand (chiefly Windows/Linux setup steps) is marked as such until CI or a reader confirms it.

## 8. Process

**Stage A — Pilot (for your review).**
1. Update uv to ≥ 0.12, `git init`, scaffold the repo and Zensical site.
2. `STYLE.md` (voice, British spelling, callout conventions) and the chapter template.
3. Part 0 in full (How to use, The toolkit, P0 Hello Beeb).
4. **P1 Hi-Lo** — shows how the very start is pitched at experienced programmers.
5. **P8 Mode 2 Sketchpad** — shows the Pygame style and the retro thread at full strength.
6. `check_all.py`, CI workflow, site building locally.

You review voice, depth, length and format. I revise until you're happy.

**Stage B — Everything else**, straight through in order: Part 1 → 2 → 3 → 4 → 5 → 6 → appendices, committing per chapter so you can read along and interject at any point.

**Scale, honestly.** Twenty-eight chapters at roughly 4,000–6,000 words each is a book: on the order of 130,000–170,000 words plus several thousand lines of tested code. It will span many working sessions. If you'd rather trade some consistency risk for speed, I can fan chapters out to parallel agents working from the style guide and the approved pilot — just say "use a workflow".

## 9. Plan review — resolved 20 September 2026

- Project list: **approved as is** (all 28 stay).
- Pilot chapters: **P1 and P8**.
- Docs site: **Zensical**.
- Web frameworks: **both Flask and FastAPI**.
- Licence: **CC BY-SA 4.0** (prose) **+ MIT** (code).
- Updating uv on this machine: **approved**.
- Addition: the capstone micro gets **sprites with collision detection** (see P28).

## 10. What the pilot taught us

Decisions made while building Stage A. Each departs from, or sharpens, something above.

- **Ruff: use the defaults.** §2 proposed starting readers on a small hand-picked rule set, because ruff 0.16 raised its defaults to 413 rules. In practice, clean tutorial code passes the new defaults untouched, so readers simply use ruff as it comes. Two defaults are worth teaching when they first fire: `zip(..., strict=True)` (B905) and `__all__` for re-exports (F401).
- **Listings are inline and checked, not included.** §7 suggested pulling listings from the real files with snippet includes. That would leave `--8<--` lines where the code should be when the Markdown is read on GitHub. Instead the code is written inline, and `scripts/check_docs.py` verifies it: marked listings must match their file, `pycon` sessions run as doctests, and every Predict snippet is executed and compared with its published answer. It has already caught real mistakes.
- **Early projects are tested from outside.** Projects 0 to 2 come before the tutorial teaches pytest, so their folders hold no tests, exactly like a reader's. Repo-level tests in `tests/` drive them with scripted input. `tests/headless.py` runs any Pygame program for N frames with no display, for all the games to come.
- **No root ruff config.** A `[tool.ruff]` table in the root `pyproject.toml` silently takes over import sorting inside every project. Each project is linted from its own folder, as a reader's copy would be.
- **`uv init` copies your Git name and email into `pyproject.toml`** for packaged projects. The reference projects omit `authors`. Project 5, where readers first meet the packaged layout, should mention it.
- **`beeb` design.** PEP 8 names (`beeb.move`, not `MOVE`), with the namespace kept (`import beeb`). The canvas is an 8-bit *palettised* surface at the mode's true resolution, scaled into a resizable window each frame: pixels hold colour numbers, as on the real hardware, which makes `POINT`, palette changes and flashing colours nearly free. `beeb.vsync()` hides the event loop. `PLOT k, x, y` is decoded with `divmod` and `match`.
- **The paint-program bug is real.** The first version of `paint.py` was written in good faith and drew fans from the corner, because the colour swatch moves the shared graphics cursor. It is kept as a stage, since it is a better demonstration of "module-level state hurts" than anything contrived.
- **Chapter length.** Project 1 is about 5,400 words and Project 8 about 8,800, listings included. Project 8 is long because it contains a 200-line module in full. Later Pygame chapters build on `beeb` and should be shorter.
- **Open for the author:** the repository's eventual URL (for `site_url` in `zensical.toml` and for links to solutions), and whether the default Zensical theme wants a more retro look.
