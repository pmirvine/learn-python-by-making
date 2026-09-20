# What's new in Python 3.15

This tutorial was written with Python 3.14, in September 2026. **Python 3.15 is due on 1 October 2026**, a few days after these words. Everything in the tutorial runs on it unchanged. This page is about what it adds that a reader of this tutorial would care about.

Every example here was run on the second release candidate, 3.15.0rc2, which is as near to the final version as makes no difference. You can do the same today, without disturbing anything:

```console
$ uv python install 3.15
$ uv run --python 3.15 python
```

The examples aren't run by the tutorial's own checks, which use 3.14, and so they're shown as plain listings.

## An immutable dictionary: `frozendict`

```python
>>> places = frozendict(torch="kitchen", key="garden")
>>> places["torch"] = "player"
TypeError: 'frozendict' object does not support item assignment
>>> places | {"torch": "player"}
frozendict({'torch': 'player', 'key': 'garden'})
>>> hash(places) is not None
True
```

It's to `dict` what `frozenset` is to `set`, and what a tuple is to a list: it can't be changed, and so it can be hashed, shared and cached without fear. `|` makes a new one.

You've wanted this three times. In [Project 4](../part-1-console/p04-codebreaker.md), where dictionaries couldn't be keys. In [Project 11](../part-2-pygame/p11-sound-and-envelope.md), where `functools.cache` needed arguments that could be hashed. And most of all in [Project 26](../part-5-tui/p26-adventure-third-edition.md), where the whole design rested on a `State` that nobody changed, and whose `places` dictionary anybody *could*. With `places: frozendict[str, str]`, that chapter's bug hunt is a `TypeError` on the line that's at fault.

## Imports that wait: `lazy import`

```python
lazy import pygame
lazy from rich.console import Console

print("This runs at once.")       # pygame hasn't been loaded
pygame.init()                      # now it has
```

An ordinary `import` runs the module there and then. A **lazy** one makes a note, and the module is loaded at the moment that the name is first *used*. If it never is, it's never loaded.

That's what a command-line program wants. `micro --version`, in [Project 28](../part-6-shipping/p28-boot-to-basic.md), imports the whole of Pygame in order to print eleven characters. People have been getting round this for years by putting imports inside functions, which is ugly, and which ruff complains about. Two things to know. An error in a lazily imported module turns up where it's first used, and not at the top of the file, which can be a long way from the cause. And `lazy` is allowed only at the top level of a module: inside a function, a class or a `try`, it's a `SyntaxError`.

## Unpacking in comprehensions

```python
>>> rows = [[1, 2], [3], [4, 5]]
>>> [*row for row in rows]
[1, 2, 3, 4, 5]
>>> {**d for d in [{"a": 1}, {"b": 2}]}
{'a': 1, 'b': 2}
```

Flattening a list of lists used to be `[x for row in rows for x in row]`, with its two `for`s in the order that everybody gets wrong, from [Project 6](../part-1-console/p06-life.md), or `itertools.chain.from_iterable`. Now a star does it.

## UTF-8, everywhere, by default

```python
>>> open("notes.txt").encoding
'utf-8'
```

[Project 5](../part-1-console/p05-colossal-cupboard.md) told you always to write `encoding="utf-8"`, since the default used to depend on the computer, and on Windows it usually wasn't UTF-8. From 3.15, it's UTF-8 on every computer. **Keep writing it**, for as long as anybody might run your program on 3.14 or earlier, and `requires-python` says that they might.

## A profiler that doesn't slow you down

```console
$ uv run --python 3.15 python -m profiling.sampling run fractal.py
$ uv run --python 3.15 python -m profiling.sampling attach 12345
```

`cProfile`, from [Project 7](../part-1-console/p07-fractal-factory.md), measures every function call, and in doing so makes a program several times slower, and distorts what it measures. The new **sampling** profiler looks at the program a few thousand times a second, from outside, and asks where it is. It costs almost nothing, and it can be attached to a program that's already running, such as a game that's just begun to stutter. `cProfile` has a new home beside it, as `profiling.tracing`, and the old name still works.

## Smaller things

- **`math.integer`** is a new module, which gathers the functions that are about whole numbers: `gcd`, `lcm`, `isqrt`, `comb`, `perm`, `factorial`. The old names in `math` remain.
- **`TypedDict`** can be *closed*: `class Score(TypedDict, closed=True)` tells the type checker that there are no keys but the ones listed, and `extra_items=int` says what any others must be. It would have tightened up [Project 22](../part-4-web/p22-high-score-server.md)'s `ScoreRow`.
- **Error messages** go on getting better, as they have in every version since 3.10. More of them now suggest what you probably meant.
- **The free-threaded build**, from [Project 25](../part-5-tui/p25-newsroom.md), is quicker in one thread than it was, and more of the packages that you use have wheels for it.
- **The JIT compiler**, which is still experimental and switched off by default, has moved on. It's not something to rely on yet.

## What to do about it

Nothing, at first. Then:

1. Add `"3.15"` to the matrix in your `check.yml`, from [Project 27](../part-6-shipping/p27-ship-it.md), and see whether everything passes. It should.
2. Add the classifier `Programming Language :: Python :: 3.15`.
3. **Don't** raise `requires-python`, and don't use `lazy import` or `frozendict` in a package that you publish, until 3.15 is the oldest Python that you're willing to support. For a library, that's years away. For a program that only you run, it's today.

The full list is in [What's New in Python 3.15](https://docs.python.org/3.15/whatsnew/3.15.html). Reading that page, every October, is a good habit, and you now know enough to follow all of it.
