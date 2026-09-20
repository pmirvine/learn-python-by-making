# Which project teaches what

An index of ideas, by theme, with the project in which each is properly taught. Where there are two, the first introduces it, and the second goes deeper, or uses it in anger. **P12** means Project 12, **SQ** is the Pyxel side quest, and **B** is the "Share it" bonus chapter.

## The language

| | |
|---|---|
| Names as labels; assignment never copies | [P1], [P4] |
| Aliasing, copying, shallow and deep | [P4], [P26] |
| Truthiness | [P1] |
| `if`, `elif`, conditional expressions, chained comparisons | [P1] |
| `while`, `break`, `continue`, `while`/`else` | [P1] |
| `for`, `range`, `enumerate`, `zip` | [P2], [P3] |
| `match`: literals, captures, guards, sequences | [P5] |
| `match`: mappings, types, classes, nested data | [P14], [P16], [P17] |
| The walrus, `:=` | [P12] |
| Indentation, `pass`, `...` | [P0], [P6] |
| `__name__` and `"__main__"` | [P4] |
| Scope: LEGB, `global`, `nonlocal` | [P7], [P8] |
| Exceptions: `try`, `except`, `else`, `finally`, `raise`, `raise … from` | [P1], [P5], [P13], [P16] |
| Exceptions of your own | [P5], [P13] |
| Exception groups, and `except*` | [P25] |
| EAFP, and asking forgiveness | [P1], [P5] |
| `with`, and context managers | [P5] |
| Writing a context manager: `@contextmanager`, `__enter__` and `__exit__` | [P17], [P18] |
| `assert` | [P3] |

## Numbers, text and bytes

| | |
|---|---|
| `int`, `float`, `/`, `//`, `%`, `**` | [P1] |
| Floats in depth: `isclose`, rounding, `inf`, `nan` | [P7] |
| `Decimal`, `Fraction`, `complex` | [P7] |
| `math` | [P7], [P12] |
| `random`: `randint`, `choice`, `seed`, `Random(seed)` | [P1], [P3], [P6], [P9] |
| Strings: slices, methods, immutability, `join`, `split` | [P4] |
| f-strings, and format specifications | [P1], [P3] |
| Unicode, `ord`, `chr`, encoding, UTF-8 | [P4] |
| Unicode's blocks: sextants, Braille, box drawing; `unicodedata` | [P24], [P26] |
| t-strings, and escaping | [P18] |
| Regular expressions | [P13], [P16] |
| `bytes`, `bytearray`, `array`, endianness | [P11] |
| Bits: `&`, `\|`, `^`, `~`, `<<`, `>>`, masks | [P19] |
| `datetime`, `timedelta`, time zones, ISO 8601 | [P23] |
| `time.perf_counter`, `time.monotonic` | [P7], [P13], [P20] |

## Collections

| | |
|---|---|
| Tuples, unpacking, `*rest` | [P2] |
| Lists, slices, `sorted` and `sort` | [P3] |
| Dictionaries, `get`, `items`, merging with `\|` | [P3], [P5] |
| Sets, `frozenset`, hashability | [P4], [P6] |
| Comprehensions: list, dict, set, nested | [P3], [P6] |
| `Counter`, `defaultdict`, `deque`, `ChainMap` | [P3], [P23], [P9], [P16] |
| Sorting with `key=`, `itemgetter`, `attrgetter`, stability | [P7], [P23] |
| Choosing a data structure | [P6] |
| Breadth-first and depth-first search | [P15], [P26] |

## Functions

| | |
|---|---|
| `def`, `return`, `None`, docstrings | [P1] |
| Default and keyword arguments | [P2] |
| The mutable default | [P4] |
| Recursion | [P2] |
| `*args`, `**kwargs`, keyword-only and positional-only | [P7] |
| Functions as values; dispatch tables | [P3], [P7] |
| Closures, factories, late binding | [P7], [P15] |
| `lambda` | [P7] |
| `functools`: `partial`, `cache`, `wraps` | [P7], [P11], [P16] |
| Decorators: registering, wrapping, factories | [P16], [P17] |
| Decorators as plain calls, and inside functions | [P28] |
| Generators, `yield`, laziness | [P6] |
| Generators as a pipeline | [P11] |
| Generator expressions; `itertools` | [P6], [P3], [P11] |
| Async generators | [P22] |

## Classes, and the data model

| | |
|---|---|
| Dataclasses: fields, `field`, `replace`, `asdict` | [P5] |
| `frozen=True`, `slots=True` | [P10], [P14] |
| Classes: `__init__`, `self`, attributes, methods | [P9] |
| Class attributes, and the shared-list trap | [P9] |
| When *not* to write a class | [P9], [P15] |
| `@property` | [P10] |
| `@classmethod`, alternative constructors, `@staticmethod` | [P10] |
| `__repr__` and `__str__` | [P10] |
| Operators: `__add__`, `__mul__`, `__rmul__`, `__matmul__`, `NotImplemented` | [P12], [P14] |
| `__eq__` and `__hash__` | [P12] |
| Containers: `__len__`, `__getitem__`, `__setitem__`, `__contains__`, `__iter__` | [P12], [P15] |
| `__slots__`, and measuring memory | [P14] |
| Inheritance, `super()`, overriding, template methods | [P15] |
| Abstract base classes | [P15], [P26] |
| Composition, and "has a" | [P9], [P28] |
| Duck typing, and `Protocol` | [P12], [P16] |
| `Protocol` or ABC? `runtime_checkable` | [P26] |
| Descriptors; where `self` comes from | [P24] |
| `Enum`, `auto`, enums with methods | [P5], [P9] |
| `IntEnum`, `IntFlag` | [P19], [P28] |
| The command pattern; undo and redo | [P15] |
| Undo as a list of values | [P26] |
| State machines | [P9], [P12] |

## Modules, packages and shipping

| | |
|---|---|
| Importing; your own modules | [P1], [P4] |
| Packages: `src/`, `__init__.py`, `__all__`, entry points | [P5], [P6] |
| Circular imports, and layering | [P5] |
| Data files inside a package; `importlib.resources` | [P10], [P14], [P28] |
| Depending on your own package; path sources; workspaces | [P11], [P13] |
| `argparse` | [P6], [P7] |
| `pathlib` | [P5] |
| JSON | [P5] |
| TOML, `tomllib` | [P14] |
| `logging` | [P15], [P23] |
| `subprocess` | [P23] |
| `sqlite3`, and SQL | [P20], [P22] |
| Environment variables, `.env`, secrets | [P20], [P21] |
| `ast`: reading code as data | [P26] |
| `pyproject.toml`, field by field | [P27] |
| Wheels, sdists, build backends | [P17], [P27] |
| Version numbers, and semantic versioning | [P11], [P22], [P27] |
| Dependency bounds; lock files; extras and groups | [P27] |
| READMEs, changelogs, licences | [P6], [P27] |
| Publishing; indexes; trusted publishing | [P27] |
| pip, venv, `requirements.txt` | [P27] |

## Types

| | |
|---|---|
| Hints on parameters, returns and variables; `X \| None` | [P3] |
| A type checker, switched on: `basic`, `standard`, `strict` | [P4], [P12], [P17] |
| `type` aliases; `Callable` | [P6], [P7] |
| `Iterator`, `Generator` | [P6], [P17] |
| `Protocol` | [P12], [P16], [P26] |
| `Self` | [P15] |
| Generics: `class Box[T]`, `def f[T]`, bounds | [P17], [P20] |
| `Literal`, unions of node types, `assert_never` | [P17] |
| `TYPE_CHECKING` | [P17] |
| `ClassVar` | [P24] |
| `TypedDict`; dataclass, `TypedDict` or pydantic model? | [P22] |
| `Annotated`; hints at run time; pydantic | [P22] |
| `py.typed` | [P20], [P27] |

## Doing several things at once

| | |
|---|---|
| A first `async def`; `await`; async generators | [P22] |
| asyncio properly: coroutines, tasks, `gather`, `TaskGroup` | [P25] |
| Cancellation, time-outs, semaphores, queues | [P25] |
| Threads, processes, `concurrent.futures` | [P25] |
| The GIL, and free-threaded Python | [P25] |
| `asyncio.to_thread`; never block the loop | [P22], [P25] |
| Textual's workers | [P25] |
| An interpreter inside a game loop; modal loops | [P28] |

## Testing

| | |
|---|---|
| pytest: tests, `assert`, reading a failure | [P3] |
| Writing the test first | [P4] |
| The bug hunt: reproduce, failing test, fix | [P4], and every project after |
| `tmp_path`, `capsys`, fixtures, factory fixtures | [P5], [P6], [P8], [P23] |
| Parametrised tests | [P6] |
| Testing randomness: seeds, and injected `Random` | [P3], [P9] |
| Testing time: an injected clock | [P20], [P23], [P24] |
| Testing a Pygame program without a window | [P8], [P9], [P13] |
| Spies, fakes and stand-ins | [P7], [P15], [P22], [P26] |
| Testing properties, and not examples | [P13], [P14] |
| Coverage | [P17] |
| Flask's and FastAPI's test clients; faking a web service | [P20], [P22] |
| `monkeypatch` | [P23] |
| Textual: the pilot; snapshot tests | [P24] |
| Async tests | [P25] |
| Tests of architecture | [P26] |
| Testing the wheel, and the oldest dependencies | [P27] |
| Testing a whole interactive program through its keyboard | [P28] |

## Tools

| | |
|---|---|
| uv: `init`, `run`, `add`, `sync`, lock files | [P0], [P3], [P4] |
| The REPL | [P0] |
| Reading a traceback | [P0], [P1] |
| Git: `status`, `add`, `commit`, `diff`, `log` | [P0], [P1] |
| Git: `restore`, `--amend` | [P4] |
| Git: branches, `switch`, `merge` | [P5] |
| GitHub, `gh`, `push`, remotes | [P6] |
| Git: tags | [P7], [P22] |
| Git: `stash`, `.gitignore` | [P9] |
| Git: merge conflicts | [P12] |
| Git: `bisect`, `revert` | [P13] |
| Pull requests | [P16] |
| Git: `rebase` | [P21] |
| Releases on GitHub | [P22], [P27] |
| The debugger | [P2], [P8], [P15] |
| Ruff | [P3] |
| `timeit`, `cProfile`; measuring before optimising | [P7], [P13], [P14] |
| VS Code: refactoring | [P10] |
| VS Code: snippets and tasks | [P14] |
| Continuous integration with GitHub Actions | [P17], [P27] |
| GitHub Pages | [P19] |
| pre-commit hooks | [P27] |

## Libraries

| | |
|---|---|
| turtle | [P2] |
| Pillow | [P7] |
| Pygame: the loop, surfaces, events, the clock | [P8], [P9] |
| Pygame: `Rect`, collisions, fonts, keys | [P10], [P9] |
| Pygame: sound, from samples | [P11] |
| Pygame: vectors, rotation, wrapping | [P12] |
| Pygame: cameras, zooming, big worlds | [P13] |
| Pygame: 3D, by hand | [P14] |
| Pygame: a user interface, by hand | [P15] |
| Pygame: masks, sprites, layers | [P28] |
| Pyxel | [SQ] |
| SVG, `xml.etree`, `http.server` | [P18] |
| HTML and CSS; Jinja2; a static site generator | [P19] |
| Flask; httpx; caching | [P20] |
| Sessions, htmx, CSRF, a content security policy | [P21] |
| FastAPI; pydantic; server-sent events; a little JavaScript | [P22] |
| PyScript, pygbag | [B] |
| Rich | [P23] |
| Textual | [P24], [P25], [P26] |
| `packaging`, `importlib.metadata` | [P27] |

## Ideas that outlast the language

| | |
|---|---|
| Keep the rules away from the screen | [P5], [P9], [P13], [P21], [P26] |
| A pure function at the centre: state in, state out | [P5], [P26] |
| One source of truth | [P5], [P27] |
| Inject what varies: randomness, clocks, consoles, clients | [P9], [P17], [P20], [P24] |
| Data, not code: levels, ships, worlds, feeds in files | [P10], [P14], [P25] |
| Never paste data into code: HTML, SQL, the shell | [P18], [P20], [P23] |
| Validate at the edges | [P20], [P22] |
| Expected failures are values, and not exceptions | [P20], [P25] |
| A cheap test first, and a dear one only if needed | [P28] |
| Parsing: tokens, grammars, trees | [P16], [P17] |
| Registries, and plug-ins | [P16], [P17], [P27], [P28] |
| Which way dependencies point | [P26], [P28] |
| Measure, and then decide | [P7], [P13], [P14], [P25] |
| Let the structure follow the need | [P9], [P15], [P26] |

[P0]: ../part-0-switching-on/p00-hello-beeb.md
[P1]: ../part-1-console/p01-hi-lo.md
[P2]: ../part-1-console/p02-turtle-sketchbook.md
[P3]: ../part-1-console/p03-dice-lab.md
[P4]: ../part-1-console/p04-codebreaker.md
[P5]: ../part-1-console/p05-colossal-cupboard.md
[P6]: ../part-1-console/p06-life.md
[P7]: ../part-1-console/p07-fractal-factory.md
[P8]: ../part-2-pygame/p08-mode2-sketchpad.md
[P9]: ../part-2-pygame/p09-snake.md
[P10]: ../part-2-pygame/p10-breakout.md
[P11]: ../part-2-pygame/p11-sound-and-envelope.md
[P12]: ../part-2-pygame/p12-asteroids.md
[P13]: ../part-2-pygame/p13-life-in-pixels.md
[P14]: ../part-2-pygame/p14-wireframe.md
[P15]: ../part-2-pygame/p15-sprite-editor.md
[SQ]: ../part-2-pygame/side-quest-pyxel.md
[P16]: ../part-3-interpreters/p16-logo.md
[P17]: ../part-3-interpreters/p17-tiny-basic.md
[P18]: ../part-4-web/p18-svg-plotter.md
[P19]: ../part-4-web/p19-pyfax.md
[P20]: ../part-4-web/p20-pyfax-live.md
[P21]: ../part-4-web/p21-adventure-online.md
[P22]: ../part-4-web/p22-high-score-server.md
[B]: ../part-4-web/bonus-share-it.md
[P23]: ../part-5-tui/p23-rich-dashboard.md
[P24]: ../part-5-tui/p24-teletext-viewer.md
[P25]: ../part-5-tui/p25-newsroom.md
[P26]: ../part-5-tui/p26-adventure-third-edition.md
[P27]: ../part-6-shipping/p27-ship-it.md
[P28]: ../part-6-shipping/p28-boot-to-basic.md
