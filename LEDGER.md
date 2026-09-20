# Ledger

What each chapter *actually* taught, what it promised later chapters would explain, and what it handed on for reuse. `PLAN.md` is the intention; this is the record. Update it as each chapter is finished, and read it before writing the next.

Rules it exists to enforce:

- **Nothing is used before it's taught.** If a chapter needs a concept that isn't in an earlier "Taught" list, it teaches it or does without.
- **Every promise is kept.** When a chapter says "Project N explains this", it goes in N's "Owes" list here.
- **Reused code keeps its shape.** When a later project depends on an earlier one's package, the API recorded here is the contract.

## Project 0 · Hello, Beeb

**Taught:** `uv init --no-package`, `uv run`, what each generated file is; `.venv` and `uv.lock` ("commit the recipe, not the cake"); the REPL (`uv run python`, Tab, `help()`, `exit`); `def main()` and indentation as block structure, lightly; `import platform`; f-strings, first look; reading a traceback bottom-up; `git status`/`add`/`commit -m`/`log --oneline`; committing from VS Code's Source Control panel; imperative commit messages; PEP 723 scripts (`uv init --script`, `uv add --script`); `from x import y`; adjacent string literals; `\n`; `-> None` noticed but not explained. Type-in: ANSI colour bars (`end=""`, `{name:^8}`, nested `for` over `range`, a list literal, all unexplained).

**Owes:** P1 `**`, `/`, `//`. P3 type hints; `enumerate` as the "better way" than indexing `NAMES[colour]`. P4 `if __name__ == "__main__"` in full; `uv add` to a project. P5 packaged layout. P2 the debugger. P27 pip, venv and the older tools.

## Project 1 · Hi-Lo

**Taught:** names are labels, not boxes (assignment binds, never copies); dynamic but strong typing; everything is an object, methods with a dot; `type()`; `int()`, `float()`, `str()` conversions and `ValueError`; `input()` always returns `str`; `random.randint` is inclusive at both ends (flagged as the exception); `if`/`elif`/`else`; comparison and `and`/`or`/`not`; chained comparisons; f-strings with expressions, `:.2f`, `:,`, `!r`; `while True` + `break`; `continue`; augmented assignment, no `++`; `while`/`else`; conditional expressions; UPPER_CASE constants by convention; truthiness and the falsy values; `try`/`except ValueError`, never bare `except`; EAFP named and briefly justified; `/` vs `//` vs `%`, flooring towards minus infinity; `.bit_length()`; simple functions, `return`, implicit `None`; docstrings and `help()`; local vs global names, reading only; importing your own file at the REPL; `None`, `is None`/`is not None`; method chaining (`.lower().startswith()`); single vs double quotes. Git: `git diff`, `git add <file>`, `commit -am`, `git show`, `git diff A B`; the run–diff–commit rhythm. Type-in: tuple assignment and swap (`low, high = 1, 100`), binary search.

**Owes:** P2 ranges include the start and exclude the end; `for`; functions in depth. P3 tests for functions. P4 aliasing with mutable objects (two names, one list); `is` vs `==` in depth; `__name__` mechanism. P5 EAFP's full rationale. P7 scope, the rest of the story (LEGB, closures). Part 2: `%` for wrapping round screen edges (paid in P8).

## Project 8 · Mode 2 Sketchpad

**Assumes (so these must be taught by P7):** packages, `src` layout, editable installs and `[project.scripts]` (P5/P6); `_private` naming convention (P6); `__init__.py` re-exports (P6); `match` (P5); `*` unpacking in calls (P7); `zip` and comprehensions (P3); slices and `del` on a slice (P3); type hints incl. `X | None`, `tuple[int, int]` (P3 onwards); pytest, fixtures-as-parameters, `parametrize`, `pytest.raises(match=)`, `tmp_path` (P3–P6); `conftest.py` (introduced *here*); aliasing bug (P4); profiling, "measure before you optimise" (P7); the debugger basics (P2); dataclasses exist (P5) though unused here.

**Taught:** pygame-ce vs pygame (`IS_CE`); the game loop: events, update, draw, `flip`, `Clock.tick`; `Surface`; `pygame.draw.*`; top-left origin; off-screen surfaces and `blit`; palettised (8-bit) surfaces, `set_palette`, `get_at_mapped`, `set_palette_at`; flags with `|`; `SystemExit`; `global`, and the rule that assignment makes a name local (`UnboundLocalError`); mutation needs no `global`; pure functions vs stateful ones; `divmod`; `match` on ints; tuple shuffle `_previous, _cursor = _cursor, (x, y)`; `type X = ...` alias, first sight; `zip(strict=True)`; `__all__`; SDL dummy driver for headless tests; test interdependence via shared state; the update–clear–draw–vsync frame shape; `event.unicode`; `"" in "abc"` gotcha. Tools: `launch.json`, conditional breakpoints, logpoints, Debug Console.

**Hands on (the `beeb` package, v0.1.0):** `mode(n)`, `gcol(action, colour)`, `clg()`, `move(x, y)`, `draw(x, y)`, `plot(k, x, y)` (k: 0–7 lines, 64–71 points, 80–87 triangles), `point(x, y)`, `vsync()`, `inkey()`, `mouse()` → `(x, y, (left, middle, right))`, `screenshot(path)`, `WIDTH`, `HEIGHT`; `beeb.screen.to_pixel`/`to_units`; `uv run beeb` shows a test card. Solutions add `colour(logical, physical)`, flashing colours, `fill`, `circle`. Used again by P11 (adds sound) and P28 (the capstone).

**Owes:** P9 classes as the cure for module-level state (the chapter's five complaints: growing `global` lists, `None` checks, interdependent tests, action at a distance, only one screen). P17 type aliases in depth. P19 bit operations in depth.
