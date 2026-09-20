# Project 6 · Life

In 1970 the mathematician John Conway invented a game with no players. There's a grid of cells, each of them alive or dead. At every tick of the clock, each cell looks at its eight neighbours, and:

- a live cell with two or three live neighbours **survives**;
- a dead cell with exactly three live neighbours **comes to life**;
- every other cell dies, or stays dead.

That's the whole of it, and out of it come things that crawl, things that blink, things that build other things, and, as was eventually proved, anything that a computer can compute. Here's one of them: a *glider gun*, which goes on firing little five-cell spaceships across the universe for ever.

```text
                                                    ██
                                                    ██  ██
                  ████                                    ████        ████
              ██      ██                                  ████        ████
  ████      ██          ██                                ████
  ████    ████  ██      ██                ██        ██  ██
            ██          ██                  ██      ██
              ██      ██          ██    ██████
                  ████




                                                          ██
                                                      ██  ██
                                                        ████




                                                                        ██
                                                                          ██
                                                                      ██████
Generation 75, population 52
```

Life was the first program that thousands of people ever typed into a home computer, where it ran at about one generation a second, on a board the size of a postage stamp. Yours will be twelve lines long, will run as fast as you like, and will have **no edges at all**.

It gets away with that by using the right data structure, a **set of tuples**, and that's one of the chapter's subjects. The other is one of Python's best ideas: the **generator**, which lets you describe a sequence that never ends, and then use as much of it as you need.

This is also the first of the tutorial's projects that comes back. In Project 13 you'll give Life a Pygame window, with a mouse to draw on it, *without touching the rules you write today*. So you'll be careful about what goes where. And at the end, your work goes up on GitHub.

| | |
|---|---|
| **You'll learn** | Sets of tuples as a data structure; set comprehensions; generators and `yield`; generator expressions; `itertools`; `frozenset`; command-line arguments with `argparse`; ANSI animation; `_private` names and a package's public face |
| **New tool skill** | Parametrised tests. GitHub: `gh`, remotes, `push`, and a README. |
| **Time** | 4 hours |
| **Before you start** | [Project 5](p05-colossal-cupboard.md) |

## Predict

!!! question "Predict"
    ```python
    cells = {(0, 0), (1, 0), (0, 0)}
    moved = {(x + 1, y) for x, y in cells}
    print(len(cells), sorted(moved))
    print(cells & moved)
    ```

??? success "Answer"
    ```text
    2 [(1, 0), (2, 0)]
    {(1, 0)}
    ```

    A set holds each thing once, so there are two cells, and not three. The braces with a `for` inside are a *set comprehension*. Tuples can be members of a set because they can't change, as Project 4 promised. Stage 1.

!!! question "Predict"
    ```python
    def countdown(n):
        print("starting")
        while n > 0:
            yield n
            n -= 1


    numbers = countdown(3)
    print("made it")
    print(next(numbers))
    print(list(numbers))
    print(list(numbers))
    ```

??? success "Answer"
    ```text
    made it
    starting
    3
    [2, 1]
    []
    ```

    Three surprises. Calling `countdown(3)` runs *none* of its code: `made it` comes out before `starting`. The function runs only when somebody asks for a value, and then only as far as the next `yield`. And once the values have been used, they're gone: the second `list(numbers)` is empty. Stage 2.

!!! question "Predict"
    ```python
    squares = (n * n for n in range(4))
    print(sum(squares))
    print(sum(squares))
    ```

??? success "Answer"
    ```text
    14
    0
    ```

    Round brackets make a *generator expression*: a comprehension that doesn't build a list, but hands its values over one at a time, as they're asked for. It too can be gone through only once. That's this chapter's bug hunt. Stage 2.

!!! question "Predict"
    ```python
    from itertools import islice, product

    print(list(product((-1, 0, 1), repeat=2))[:4])


    def evens():
        n = 0
        while True:
            yield n
            n += 2


    print(list(islice(evens(), 5)))
    ```

??? success "Answer"
    ```text
    [(-1, -1), (-1, 0), (-1, 1), (0, -1)]
    [0, 2, 4, 6, 8]
    ```

    `product` gives every combination, in the way that nested `for` loops would. `evens()` is an endless sequence, and `islice` takes the first five of it. `list(evens())` would never finish. Stages 1 and 2.

## Build

### Stage 1: A universe in a set

```console
$ cd making
$ uv init life
$ cd life
$ uv add --dev pytest ruff
$ code .
```

How would you store a Life board? The obvious way, and the way everyone did it in BASIC, is a two-dimensional array: `DIM board%(39, 23)`. In Python that's a list of lists. It works, up to a point. The board has edges, and the patterns break when they reach them. You must decide its size before you begin. And every generation costs the same, however little is going on: a 1,000 by 1,000 board with one glider on it means a million cells to look at, to move five.

Langton's ant, at the end of the last chapter, suggested something better. **Store only the cells that are alive, as a set of `(x, y)` tuples.** Anything that isn't in the set is dead.

```pycon
>>> glider = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
>>> (1, 0) in glider
True
>>> (500, -3000) in glider
False
>>> len(glider)
5
```

This universe has no edges, since a tuple can hold any integers, negative ones included. A generation costs in proportion to the number of live cells, and not to the size of the board. "Is this cell alive?" is `in`, which for a set is instant. And `len` is the population. Often the hard part of a program is finding the data structure that makes the code easy, and once you have it, the code is short.

Here it is. Create `src/life/core.py`:

<!-- listing: projects/06-life/stages/stage1_core.py -->
```python title="src/life/core.py"
"""The rules of Conway's Game of Life, and nothing else.

A universe is a set of the cells that are alive, each an (x, y) tuple. There
are no edges, and no grid: anywhere that isn't in the set is dead. Nothing in
this module prints, sleeps or knows how big your screen is.
"""

from collections import Counter
from itertools import product

type Cell = tuple[int, int]

_OFFSETS = [(dx, dy) for dx, dy in product((-1, 0, 1), repeat=2) if (dx, dy) != (0, 0)]


def neighbours(cell: Cell) -> list[Cell]:
    """Return the eight cells that surround a cell."""
    x, y = cell
    return [(x + dx, y + dy) for dx, dy in _OFFSETS]


def step(live: set[Cell]) -> set[Cell]:
    """Return the next generation. The set you pass in is left as it was."""
    counts = Counter(neighbour for cell in live for neighbour in neighbours(cell))
    return {
        cell
        for cell, count in counts.items()
        if count == 3 or (count == 2 and cell in live)
    }
```

That's Conway's Game of Life, complete. Read the docstring's last sentence again, because it's a promise that will matter in Project 13. Now the code, from the top.

`type Cell = tuple[int, int]` is a *type alias*: a name for a type, so that the hints can say `set[Cell]` and mean something to the reader. It's a statement for the type checker's benefit, and does nothing at run time.

`itertools.product` gives every combination of its arguments, as nested loops would. `product((-1, 0, 1), repeat=2)` is all nine pairs from `(-1, -1)` to `(1, 1)`, and the comprehension drops `(0, 0)`, since a cell isn't its own neighbour. It's worked out once, when the module is imported.

**The leading underscore** in `_OFFSETS` keeps a promise from Project 5. It's a convention, with nothing to enforce it, and it means: *this is private. It's here for this module's own use, so don't rely on it from outside, because it may change.* Every experienced Python programmer reads it that way, and so do the tools. Anything without an underscore is part of the module's public face.

Now `step`, which is two statements long. The trick is to turn the question round. Don't ask, of every cell in the universe, "how many live neighbours have you got?" Go through the live cells only, and have each of them nudge all eight of its neighbours, saying "there's a live one next to you". Then count the nudges.

```python
counts = Counter(neighbour for cell in live for neighbour in neighbours(cell))
```

There are two `for`s in that comprehension, and they read in the same order as nested loops would: *for each live cell, for each of its neighbours, give me the neighbour*. The `Counter`, from Project 3, tallies them. When it's done, `counts[cell]` is the number of live neighbours that `cell` has, for every cell that has any at all. A cell with no live neighbours isn't mentioned, and quite right, since it's going to be dead.

```python
return {
    cell
    for cell, count in counts.items()
    if count == 3 or (count == 2 and cell in live)
}
```

That's a *set comprehension*: like a list comprehension, but with braces, and giving a set. And the condition *is* Conway's rules. With three neighbours, a cell is alive next time, whether that's a birth or a survival. With two, it's alive only if it was alive already. Anything else is dead, and so isn't in the set.

Notice, too, that `step` builds a new set, and doesn't touch the one it was given. That's Project 4's policy again, and here it isn't only good manners. Every cell of the new generation has to be worked out from the *old* one. Change the board while you're still reading from it, and you get the wrong answer. It's the classic Life bug, and it can't happen here.

Try it at the REPL, with `uv run python`. A row of three, the *blinker*, should turn into a column of three, and back:

```pycon
>>> from life.core import step
>>> blinker = {(0, 1), (1, 1), (2, 1)}
>>> sorted(step(blinker))
[(1, 0), (1, 1), (1, 2)]
>>> step(step(blinker)) == blinker
True
```

(The `sorted` is there because a set has no order, and might print its members any way round.)

!!! success "Checkpoint"
    ```console
    $ git add .
    $ git commit -m "Add the rules of Life, as a function from set to set"
    ```

### Stage 2: For ever, one generation at a time

A universe goes on for ever. How do you write that down? `step(step(step(…)))` won't do. A function that returned a list of the first thousand generations would be wasteful if you wanted ten, and useless if you wanted a thousand and one. What you'd like to say is: *here are all the generations, every one of them. Take as many as you want.*

#### Generators

You can say exactly that. Add this to `core.py`, with `from collections.abc import Iterator` among the imports:

<!-- listing: projects/06-life/stages/stage2_core.py -->
```python title="src/life/core.py"
def generations(live: set[Cell]) -> Iterator[set[Cell]]:
    """Yield the universe as it is now, and then every generation after it, for ever."""
    while True:
        yield live
        live = step(live)
```

A function with a `yield` in it is a *generator function*, and it behaves in a way that nothing you've met so far prepares you for. Look at the second Predict again:

```pycon
>>> def countdown(n):
...     print("starting")
...     while n > 0:
...         yield n
...         n -= 1
...
>>> numbers = countdown(3)
>>> next(numbers)
starting
3
>>> next(numbers)
2
```

**Calling it runs none of it.** You get back a *generator object*, straight away, and the function's body hasn't begun. Then, each time somebody asks for a value, which is what `next()` does, the function runs *as far as the next `yield`*, hands that value over, and **freezes**, with its local variables and its place in the code kept exactly as they were. The next request wakes it up, and it carries on from where it stopped. If the function ever returns, the sequence is over.

So `generations` really is an endless loop, and it's perfectly safe, because it only ever runs one turn at a time, when it's asked to. The caller is in charge. That's called *lazy* evaluation: nothing is worked out until somebody wants it.

You rarely call `next()` yourself. A generator can be used anywhere that a list could be looped over: in a `for` loop, in a comprehension, in `sum`, `max`, `sorted`, `zip`, `enumerate`, `", ".join`. Those all work by asking for the next item until there aren't any more, which is called the *iteration protocol*, and lists, tuples, strings, dictionaries, sets, files, ranges and generators all speak it. It's why `for` was never a counting loop.

!!! warning "Gotcha"
    A generator can be gone through **once**. When its values have been handed over, they're gone, and it's empty for ever after, as the second and third Predicts showed. It doesn't complain. It simply has nothing more to give.

    ```pycon
    >>> numbers = countdown(3)
    >>> list(numbers)
    starting
    [3, 2, 1]
    >>> list(numbers)
    []
    ```

    If you need to go through the values twice, turn them into a list first. This catches everybody, and it's this chapter's bug hunt.

`neighbours` builds a list of eight tuples, which its caller loops over once and throws away. It can be a generator too, and hand the tuples over as they're wanted. Change it to:

<!-- listing: projects/06-life/stages/stage2_core.py -->
```python title="src/life/core.py"
def neighbours(cell: Cell) -> Iterator[Cell]:
    """Yield the eight cells that surround a cell."""
    x, y = cell
    for dx, dy in _OFFSETS:
        yield x + dx, y + dy
```

`step` doesn't need to change, and nor does any other caller, because a loop doesn't care whether it's given a list or a generator. The return type is `Iterator[Cell]`: "something that gives you `Cell`s, one at a time".

!!! info "Coming from JavaScript or C#"
    These are JavaScript's `function*` and C#'s iterator methods, with `yield return`. If you've used either, you know the idea. The difference is how much of Python is built on it.

#### Generator expressions

Here's the promise from Project 3, where the type-in listing had "a comprehension without its square brackets". Put a comprehension in *round* brackets, and you get a *generator expression*: the same thing, but lazy, giving up its items one at a time and never building a list.

```pycon
>>> sum([n * n for n in range(1_000_000)])
333332833333500000
>>> sum(n * n for n in range(1_000_000))
333332833333500000
```

The first of those builds a list of a million numbers, adds them up, and throws the list away. The second never has more than one number in existence at a time. When a generator expression is the only argument to a function, the function call's own brackets will do, and that's what you were looking at in Project 3, and in `step` a moment ago: `Counter(neighbour for cell in live …)` counts the neighbours as they're produced, and the long list of them is never built.

So which should you use? If you're going to go through the values once, and straight away, use a generator expression. If you need to keep them, index them, take their `len` or go through them twice, make a list.

#### Taking some of for ever

You can't slice a generator, since it has no length, and no tenth item until it's been asked nine times. `itertools.islice` does the equivalent, lazily:

```pycon
>>> from itertools import islice
>>> from life.core import generations
>>> blinker = {(0, 1), (1, 1), (2, 1)}
>>> [len(universe) for universe in islice(generations(blinker), 5)]
[3, 3, 3, 3, 3]
>>> tenth = next(islice(generations(blinker), 10, None))
>>> tenth == blinker
True
```

`islice(things, 5)` is the first five. `islice(things, 10, None)` starts at the item numbered 10 and never stops, so `next` of that is generation 10. Its arguments are those of `range`, and of slices. `itertools` is a whole module of tools for working with sequences one item at a time: you've met `pairwise` and `product`, and there are `count`, `cycle`, `chain`, `accumulate`, `takewhile`, `groupby`, `batched`, `combinations` and more. It's well worth ten minutes with [its documentation](https://docs.python.org/3/library/itertools.html).

#### Something to look at

Time to see it. Drawing gets a module of its own, `src/life/render.py`:

<!-- listing: projects/06-life/src/life/render.py -->
```python title="src/life/render.py"
"""Turning a universe into text. This is the only module that knows what a cell looks like."""

from life.core import Cell

ALIVE = "██"
DEAD = "  "


def render(live: set[Cell], width: int, height: int) -> str:
    """Draw the part of the universe from (0, 0) to (width, height), as text.

    Each cell is two characters wide, because characters in a terminal are
    about twice as tall as they are wide.
    """
    rows = []
    for y in range(height):
        rows.append("".join(ALIVE if (x, y) in live else DEAD for x in range(width)))
    return "\n".join(rows)
```

The universe has no edges, but your terminal has, so `render` draws a window onto it, and cells outside the window simply aren't shown. It *returns* a string, of course, and doesn't print it.

Next, a first version of the program. Create `src/life/cli.py`, which is short for *command-line interface*:

<!-- listing: projects/06-life/stages/stage2_cli.py -->
```python title="src/life/cli.py"
"""Animating a universe in the terminal."""

import time
from itertools import islice

from life.core import generations
from life.render import render

HOME = "\033[H"
CLEAR = "\033[2J"

GLIDER = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}


def main() -> None:
    print(CLEAR, end="")
    for number, universe in enumerate(islice(generations(GLIDER), 100)):
        print(HOME + render(universe, 40, 20))
        print(f"Generation {number}, population {len(universe)}  ")
        time.sleep(0.1)
```

In `pyproject.toml`, point the `life` command at it, and then empty `src/life/__init__.py` of everything but its docstring, since its `main` isn't wanted:

```toml
[project.scripts]
life = "life.cli:main"
```

!!! example "Run it"
    ```console
    $ uv run life
    ```

    A glider crawls down and to the right for ten seconds, and leaves.

The animation is done with the escape codes of Project 0. `\033[2J` clears the screen. `\033[H` sends the cursor *home*, to the top left, and doesn't clear anything, so that each frame is printed over the last, which is much steadier on the eye than clearing every time. The `for` line is worth reading slowly. `generations(GLIDER)` is every generation there will ever be. `islice(…, 100)` is the first hundred of those. `enumerate` numbers them. There are three generators there, one inside another, and at no point is there more than one universe in memory.

!!! success "Checkpoint"
    ```console
    $ git add .
    $ git commit -m "Generate generations, and animate a glider"
    ```

### Stage 3: Patterns, and a proper command line

A program with one glider built into it isn't much of a laboratory. This stage adds a zoo of patterns, random "soup", and a real command line: `life gun --fps 30`.

#### Patterns

Patterns ought to be written down as they look, not as lists of coordinates. Create `src/life/patterns.py`:

<!-- listing: projects/06-life/src/life/patterns.py -->
```python title="src/life/patterns.py"
"""Patterns to start a universe with: some famous ones, and random soup."""

import random

from life.core import Cell

# Drawn as they look: O is a live cell, and anything else is a dead one.
PATTERNS = {
    "block": """
        OO
        OO
    """,
    "beehive": """
        .OO.
        O..O
        .OO.
    """,
    "blinker": """
        OOO
    """,
    "toad": """
        .OOO
        OOO.
    """,
    "glider": """
        .O.
        ..O
        OOO
    """,
    "lwss": """
        .O..O
        O....
        O...O
        OOOO.
    """,
    "r-pentomino": """
        .OO
        OO.
        .O.
    """,
    "acorn": """
        .O.....
        ...O...
        OO..OOO
    """,
    "gun": """
        ........................O...........
        ......................O.O...........
        ............OO......OO............OO
        ...........O...O....OO............OO
        OO........O.....O...OO..............
        OO........O...O.OO....O.O...........
        ..........O.....O.......O...........
        ...........O...O....................
        ............OO......................
    """,
}


def parse(picture: str) -> set[Cell]:
    """Turn a picture of a pattern into the set of its live cells."""
    rows = [row.strip() for row in picture.strip().splitlines()]
    return {
        (x, y)
        for y, row in enumerate(rows)
        for x, character in enumerate(row)
        if character == "O"
    }


def shift(live: set[Cell], dx: int, dy: int) -> set[Cell]:
    """Return the same pattern, moved across by dx and down by dy."""
    return {(x + dx, y + dy) for x, y in live}


def soup(
    width: int, height: int, density: float = 0.3, seed: int | None = None
) -> set[Cell]:
    """Return a random universe, with roughly `density` of its cells alive."""
    rng = random.Random(seed)
    return {
        (x, y) for x in range(width) for y in range(height) if rng.random() < density
    }
```

Triple quotes make a string that can run over several lines. `parse` is one set comprehension, with two `for`s and an `if`: *for each row and its number, for each character and its number, if it's an O, give me the coordinates.* `enumerate` supplies the numbers.

In `soup`, `random.Random(seed)` makes a random number generator of your own, separate from the shared one behind `random.randint`. Give it a seed, and its sequence can be repeated. Give it `None`, and it can't. That's a better way of making randomness testable than Project 3's `random.seed`, because it disturbs nobody else: there's no shared, hidden state. (Hold on to that thought for Project 8.)

#### When has it all happened before?

Some patterns never change, and some repeat. It would be good to find out which. Add these to `core.py`, and add `islice` to the `itertools` import:

<!-- listing: projects/06-life/src/life/core.py -->
```python title="src/life/core.py"
def normalise(live: set[Cell]) -> frozenset[Cell]:
    """Slide a pattern so that its top-left corner is at (0, 0), and freeze it.

    Two universes that differ only in position normalise to the same value,
    and a frozenset, unlike a set, can be kept in a set or used as a key.
    """
    if not live:
        return frozenset()
    left = min(x for x, _ in live)
    top = min(y for _, y in live)
    return frozenset((x - left, y - top) for x, y in live)


def period(live: set[Cell], limit: int = 1000) -> int | None:
    """Return how many generations a pattern takes to look the same again.

    That's 1 for a pattern that never changes, 4 for a glider (which looks the
    same again, somewhere else), and 0 for a pattern that dies out. Returns
    None if nothing has repeated within the limit.
    """
    seen: dict[frozenset[Cell], int] = {}
    for number, universe in enumerate(islice(generations(live), limit)):
        if not universe:
            return 0
        shape = normalise(universe)
        if shape in seen:
            return number - seen[shape]
        seen[shape] = number
    return None
```

To notice that a universe has been seen before, you keep the ones you've seen in a dictionary, along with when you saw them. But the keys of a dictionary can't be things that change, as Project 4 explained, and a set can change. So there's **`frozenset`**, which is to `set` as `tuple` is to `list`: the same thing, except that it can't be altered, and can therefore be hashed. It completes the table from Project 4.

`normalise` slides a pattern into the corner before freezing it, so that a glider which has moved on is recognised as the same shape. Look at `min(x for x, _ in live)`: a generator expression, handed straight to `min`.

#### The package's front door

Other code, and that includes your own tests, shouldn't have to know which module each thing lives in. `src/life/__init__.py` gathers the public names together, so that `from life import step, parse` will do:

<!-- listing: projects/06-life/src/life/__init__.py -->
```python title="src/life/__init__.py"
"""Conway's Game of Life."""

from life.core import Cell, generations, neighbours, normalise, period, step
from life.patterns import PATTERNS, parse, shift, soup
from life.render import render

__all__ = [
    "PATTERNS",
    "Cell",
    "generations",
    "neighbours",
    "normalise",
    "parse",
    "period",
    "render",
    "shift",
    "soup",
    "step",
]
```

`__all__` is the package's official list of what it offers. Without it, Ruff sees imports that nothing in the file uses, and wants them removed. With it, the imports have a purpose, which is to be re-exported. `_OFFSETS` isn't on the list, and isn't meant to be. If you ever move `step` to another module, only this file changes, and nobody who uses the package will notice. That's the point of a front door: what's behind it is your own business.

#### `argparse`

Replace `src/life/cli.py`:

<!-- listing: projects/06-life/src/life/cli.py -->
```python title="src/life/cli.py"
"""The command line: choosing a pattern, and animating it in the terminal."""

import argparse
import shutil
import time
from itertools import islice

from life.core import generations
from life.patterns import PATTERNS, parse, shift, soup
from life.render import render

HOME = "\033[H"
CLEAR = "\033[2J"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="life", description="Conway's Game of Life, in the terminal."
    )
    parser.add_argument(
        "pattern",
        nargs="?",
        default="soup",
        choices=["soup", *PATTERNS],
        help="what to start with (default: random soup)",
    )
    parser.add_argument("-g", "--generations", type=int, help="stop after this many")
    parser.add_argument("--fps", type=float, default=10, help="generations a second")
    parser.add_argument("--seed", type=int, help="make the soup repeatable")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_arguments(argv)
    columns, lines = shutil.get_terminal_size()
    width, height = columns // 2, lines - 2

    if args.pattern == "soup":
        live = soup(width, height, seed=args.seed)
    else:
        live = shift(parse(PATTERNS[args.pattern]), width // 3, height // 3)

    print(CLEAR + HIDE_CURSOR, end="")
    try:
        history = islice(generations(live), args.generations)
        for number, universe in enumerate(history):
            print(HOME + render(universe, width, height))
            status = f"Generation {number}, population {len(universe)}  "
            print(status, end="", flush=True)
            time.sleep(1 / args.fps)
    except KeyboardInterrupt:
        pass
    finally:
        print(SHOW_CURSOR)
```

`argparse`, from the standard library, turns the words on the command line into an object with named attributes. You describe the arguments you expect. A name without dashes is *positional*, and `nargs="?"` makes it optional. Names that start with dashes are options, which can go anywhere. `type=int` converts, and complains on your behalf if it can't. `choices` restricts. `["soup", *PATTERNS]` is star-unpacking inside a list: `"soup"`, and then all of the dictionary's keys. In return, `argparse` checks everything, reports mistakes politely, and writes your `--help` for you:

```console
$ uv run life --help
usage: life [-h] [-g GENERATIONS] [--fps FPS] [--seed SEED]
            [{soup,block,beehive,blinker,toad,glider,lwss,r-pentomino,acorn,gun}]

Conway's Game of Life, in the terminal.

positional arguments:
  {soup,block,beehive,blinker,toad,glider,lwss,r-pentomino,acorn,gun}
                        what to start with (default: random soup)

options:
  -h, --help            show this help message and exit
  -g, --generations GENERATIONS
                        stop after this many
  --fps FPS             generations a second
  --seed SEED           make the soup repeatable
```

`main` takes an optional `argv`. Left as `None`, `argparse` reads the real command line. But a test can call `main(["blinker", "-g", "3"])`, and that's all it takes to make a command-line program testable.

The `try` has all four of its parts working for a living. The animation would run for ever, so you stop it with ++ctrl+c++, which Python turns into a `KeyboardInterrupt` exception. Catching it, and doing nothing (`pass` is the statement that does nothing), makes that a clean way out, where otherwise there'd be a traceback. And `finally` puts the cursor back *whatever* happens, because a terminal that's been left without a cursor is a very annoying thing. When `args.generations` is `None`, `islice(…, None)` means "no limit".

!!! example "Run it"
    ```console
    $ uv run life
    $ uv run life gun --fps 30
    $ uv run life r-pentomino --fps 60
    $ uv run life acorn -g 500 --fps 100
    ```

    Make the terminal window as big as you can first, and press ++ctrl+c++ to stop. The *R-pentomino* is five cells, which take 1,103 generations to settle down. The *acorn* is seven, and takes 5,206. Nobody could have guessed either from looking at them. Most of each will wander off the edge of your window, but it's still there. Nothing in this universe is ever lost for having gone out of sight.

!!! success "Checkpoint"
    ```console
    $ git add .
    $ git commit -m "Add patterns, soup, period detection and a command line"
    ```

### Stage 4: One test, many cases

In Project 5 you tested a table of replies with a loop inside a single test. It worked, but it had two faults. When one case failed, the loop stopped, and you never learned whether the rest would have passed. And the report said only that `test_replies` had failed, leaving you to work out which reply. pytest has the proper tool. Create `tests/test_core.py`:

<!-- listing: projects/06-life/tests/test_core.py -->
```python title="tests/test_core.py"
from itertools import islice

import pytest

from life import (
    PATTERNS,
    generations,
    neighbours,
    normalise,
    parse,
    period,
    shift,
    step,
)
# ...
@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("block", 1),
        ("beehive", 1),
        ("blinker", 2),
        ("toad", 2),
        ("glider", 4),
        ("lwss", 4),
    ],
)
def test_periods(name, expected):
    assert period(parse(PATTERNS[name])) == expected
```

`@pytest.mark.parametrize` is another decorator. It's given the names of some parameters and a list of values for them, and it runs the test **once for each**, as a separate test, with a name of its own:

```console
$ uv run pytest -v -k periods
tests/test_core.py::test_periods[block-1] PASSED
tests/test_core.py::test_periods[beehive-1] PASSED
tests/test_core.py::test_periods[blinker-2] PASSED
tests/test_core.py::test_periods[toad-2] PASSED
tests/test_core.py::test_periods[glider-4] PASSED
tests/test_core.py::test_periods[lwss-4] PASSED
```

Six tests, which pass or fail independently, and adding a seventh is one line. (`-v` is for *verbose*, and `-k` runs only the tests whose names contain the word that follows.) Whenever you catch yourself copying a test and changing the numbers, you want `parametrize`. Go back to Project 5 and convert `test_replies_to_things_that_do_not_work`, for practice.

You can parametrise over anything that can be looped over, and a dictionary gives its keys. In `tests/test_patterns.py`:

<!-- listing: projects/06-life/tests/test_patterns.py -->
```python title="tests/test_patterns.py"
@pytest.mark.parametrize("name", PATTERNS)
def test_every_pattern_has_some_cells_and_starts_in_the_corner(name):
    cells = parse(PATTERNS[name])
    assert cells
    assert min(x for x, _ in cells) == 0
    assert min(y for _, y in cells) == 0
```

That's a test of the data, as in Project 5, and it grows a new case of its own accord whenever you add a pattern.

The rest are tests of the usual kind. These are the ones that matter most:

<!-- listing: projects/06-life/tests/test_core.py -->
```python title="tests/test_core.py"
def test_step_leaves_its_argument_alone():
    blinker = parse(PATTERNS["blinker"])
    before = blinker.copy()
    step(blinker)
    assert blinker == before
# ...
def test_a_glider_moves_one_cell_diagonally_every_four_generations():
    glider = parse(PATTERNS["glider"])
    later = next(islice(generations(glider), 4, None))
    assert later == shift(glider, 1, 1)


def test_the_gun_fires_a_five_cell_glider_every_thirty_generations():
    gun = parse(PATTERNS["gun"])
    populations = [len(universe) for universe in islice(generations(gun), 0, 121, 30)]
    assert populations == [36, 41, 46, 51, 56]
    assert period(gun, limit=100) is None
```

Look at the last of them. It checks a contraption of 36 cells, through 120 generations, against a fact that you can look up in any book about Life: the gun fires one glider, of five cells, every thirty generations. If your `step` were wrong in any particular, that test would fail. And `islice` takes a step, like `range`: every thirtieth generation.

Testing the command line needs no tricks, since `main` takes its arguments as a list, and pytest's `capsys` fixture captures whatever gets printed. In `tests/test_render.py`:

<!-- listing: projects/06-life/tests/test_render.py -->
```python title="tests/test_render.py"
def test_the_program_runs_and_reports_each_generation(capsys):
    main(["blinker", "--generations", "3", "--fps", "1000"])
    out = capsys.readouterr().out
    assert "Generation 0, population 3" in out
    assert "Generation 2, population 3" in out
    assert "Generation 3" not in out
```

Write the others yourself: that a cell has eight neighbours, and isn't one of them. That a lonely cell dies. That `render` draws what it should. That a seeded soup can be repeated. The project in the tutorial's repository has thirty-eight, of which eighteen come from three uses of `parametrize`.

!!! success "Checkpoint"
    Run, test, lint, diff, commit.

    ```console
    $ git add .
    $ git commit -m "Test the rules against known patterns"
    ```

### Stage 5: GitHub

So far, the whole history of every project you've written has been on one computer. If its disk dies tonight, that's that. And nobody else can see your work, use it, or help with it. Git was made for sharing, and the place where most of the world's open-source code is shared is [GitHub](https://github.com).

You'll need an account, which is free. Then install GitHub's command-line tool, `gh`, which saves you a morning of fiddling with keys and passwords:

=== "macOS"

    ```console
    $ brew install gh
    ```

    Without Homebrew, there's an installer at [cli.github.com](https://cli.github.com/).

=== "Windows"

    ```console
    $ winget install --id GitHub.cli
    ```

    Then open a new terminal.

=== "Linux"

    See [the instructions for your distribution](https://github.com/cli/cli/blob/trunk/docs/install_linux.md). On Debian and Ubuntu, `sudo apt install gh` will give you a version that's old, but will do.

Log in. It asks a few questions, for which the suggested answers are fine, and then opens your browser to confirm that it's you:

```console
$ gh auth login
```

#### A README

A repository's front page on GitHub is its `README.md`. uv gave you an empty one. It's written in *Markdown*, a way of marking up plain text that you can pick up in five minutes: `#` for a heading, `**bold**`, backticks for `code`, three backticks round a block of code, and `-` for a bullet. Say what the thing is, show how to run it, and stop:

````markdown title="README.md"
# Life

Conway's Game of Life, in the terminal. The universe has no edges.

```console
$ uv run life            # random soup
$ uv run life gun        # Gosper's glider gun
$ uv run life --help
```

The rules are in `src/life/core.py`, which knows nothing about terminals.
A universe is a set of `(x, y)` tuples, and `generations()` yields them for ever.

To run the tests: `uv run pytest`.
````

Commit it. Then:

```console
$ gh repo create life --public --source=. --push
✓ Created repository yourname/life on GitHub
✓ Added remote https://github.com/yourname/life.git
✓ Pushed commits to https://github.com/yourname/life.git
```

That's made a repository on GitHub, told your local repository about it, and sent your whole history up. (Use `--private` if you'd sooner keep it to yourself for now.) `gh browse` opens it in your browser. There's your README, your code, and every commit you've made, with its message. This is where well-chosen messages earn their keep.

Here's what happened. Your repository has gained a *remote*: a named link to another copy of itself. `git remote -v` shows it, and by convention it's called `origin`. Your `main` branch now *tracks* `origin/main`. From here on, the rhythm has one more beat:

```console
$ git push
```

sends any commits that GitHub hasn't got. Commits are still local, instant, and private until you push them. `git status` will tell you, `Your branch is ahead of 'origin/main' by 2 commits`, when you have some that haven't been sent. `git pull` goes the other way, fetching commits that GitHub has and you haven't, which matters once you work on two computers, or with other people.

!!! warning "Gotcha"
    Now you can see the point of Project 4's warning about `git commit --amend`. Amending makes a *new* commit to replace the old one. If the old one has already been pushed, your history and GitHub's no longer agree, and Git will refuse your next push. Amend only what you haven't pushed. For anything that has been, make a new commit that puts it right.

Two things that must never go into a repository, public or private: **passwords and keys**, because Git's history is for ever, and deleting the file later doesn't take it out of the history; and big generated files, such as `.venv`. uv's `.gitignore` deals with the second. The first is up to you, and Project 20 will show you how to manage it.

Go back now and put your earlier projects on GitHub as well. It's one command in each: `gh repo create --public --source=. --push`.

!!! success "Checkpoint"
    `git status` says `Your branch is up to date with 'origin/main'`, and your code is safe from your own hard disk.

## Type-in listing

Life has two dimensions. Here's the one-dimensional version: a single row of cells, in which each cell's fate depends on itself and its two neighbours. Each new row is printed under the last, so that you see the whole history at once. Save it as `rule.py`, in the project folder.

<!-- listing: projects/06-life/rule.py -->
```python title="rule.py" linenums="1"
import sys

RULE = int(sys.argv[1]) if len(sys.argv) > 1 else 90
WIDTH = 79


def rows(rule, width):
    cells = [0] * width
    cells[width // 2] = 1
    while True:
        yield cells
        cells = [
            rule >> (4 * cells[i - 1] + 2 * cells[i] + cells[(i + 1) % width]) & 1
            for i in range(width)
        ]


for number, row in enumerate(rows(RULE, WIDTH)):
    print("".join("█" if cell else " " for cell in row))
    if number == 39:
        break
```

Run it with `uv run rule.py`, and then with `uv run rule.py 30`, and `110`, and `184`.

1. `sys.argv` is the command line as a plain list of strings, with no help from `argparse`. What's in `sys.argv[0]`?
2. There are 256 possible rules, since a cell and its two neighbours can be in eight states, and a rule says "alive" or "dead" for each of the eight. Line 13 looks the answer up *in the bits of the rule number itself*. `4 * a + 2 * b + c` makes a number from 0 to 7 out of three cells. What do `>>` and `& 1` do with it? (Project 19 has much more about bits.)
3. What happens at the two ends of the row? Look at `cells[i - 1]` when `i` is 0, and at the `% width`.
4. Rule 90 draws a triangle named after Sierpiński, which you may have drawn with a turtle in Project 2. Rule 30 is so unpredictable that it has been used as a random number generator. Rule 110 can compute anything that a computer can, as Life can. All from one line of arithmetic.

## Bug hunt

A colleague has written `census.py`, which charts a pattern's population over time, and then reports its peak. It's in the project's `bughunt/` folder. Copy it to a `bughunt` folder of your own. It imports `life`, as any other program could, because your package is installed.

```console
$ uv run bughunt/census.py
Traceback (most recent call last):
  ...
  File "bughunt/census.py", line 19, in peak
    return max(len(universe) for universe in history)
ValueError: max() iterable argument is empty
```

"It *can't* be empty," says your colleague. "I've only just printed forty rows of it."

1. **Reproduce it.** Then call `chart` and `peak` separately, at the REPL or in a test, each with a plain list of two or three small sets. Do they work?
2. **Write a failing test** for `report`, in `bughunt/test_census.py`.
3. **Fix it.** There are at least three ways of doing so. Which is best, and what does each cost, for a history of a million generations?

??? tip "Hint"
    What *type* of thing is `history`, in `report`? Look at the second and third Predicts.

??? success "Solution"
    `history = islice(generations(live), count)` is an **iterator**, and an iterator can be gone through once. `chart` goes through it, to the end. When `peak` comes to ask for the values, there are none left, and `max` of nothing is a `ValueError`.

    Both functions are correct. Each passes every test you can write for it *with a list*, because a list can be gone through as often as you like. The bug is in the three lines that join them. The type hint, `Iterable`, was telling the truth all along: it promises only that you can loop over the thing, and not that you can do it twice.

    The simplest fix is to make a list, once:

    ```python
    history = list(islice(generations(live), count))
    ```

    For forty generations, or forty thousand, that's the right answer. It costs memory in proportion to the length of the history. For a million generations of a big universe, you'd do better to work out both results in **one pass**, keeping the largest population seen so far as you go along, and never holding more than one universe at a time. (`itertools.tee` makes two iterators from one, but it does so by remembering everything that one has seen and the other hasn't, which here is all of it, so it would save nothing.)

    The lesson for your own functions: if you're going to go through an argument more than once, either ask for a `Sequence`, or turn it into a list yourself at the top.

## Challenges

Make a branch for each, and push when you've merged.

**Tweak**

1. Try some different characters for a live cell, in `render.py`: `"● "`, `"▓▓"`, `"[]"`. Only one line needs to change, which is a sign that the line was in the right place.
2. Add a `--density` option for the soup, a float from 0 to 1. What's the thinnest soup that still has anything in it after a hundred generations?
3. Add a pattern of your own to the zoo. The *pulsar* and the *pentadecathlon* are good ones to look up. If it oscillates, add it to `test_periods`.

**Extend**

1. **Round the world.** Add a `--wrap` option, under which the universe is the size of the window, and anything leaving by one edge comes in at the opposite one. A glider should go round for ever.
2. **Twice the resolution.** The characters `▀`, `▄` and `█` are the top half, the bottom half, and both halves of a character cell. Write `render_fine`, which draws *two* rows of the universe in each line of text, and compare.
3. **Until it settles.** Add `--until-stable`, to stop when the universe starts repeating itself, and report the period. `period` does nearly what's needed, but it runs the whole history before you've seen any of it. How would you check *as you go*?

??? tip "Hint for round the world"
    It's tempting to take an ordinary `step`, and then wrap every cell's coordinates with `% width` and `% height`. It looks right, and it's wrong. Think about a cell on the left-hand edge: some of the nudges meant for it have been counted under `(0, y)`, and the others under `(width, y)`, and neither count is the true one. It's the **neighbours** that have to be wrapped, *before* they're counted. You'll need a `step` of your own, which the main one needn't know about.

**Invent**

1. **Other rules.** Life is "B3/S23": a birth on 3 neighbours, survival on 2 or 3. *HighLife*, B36/S23, has a pattern that copies itself. *Seeds*, B2/S, in which nothing ever survives, explodes from almost any start. *Day & Night*, B3678/S34678, is symmetrical between alive and dead. Give `step` a rule, as two sets of numbers, and let the command line choose it.
2. **A pattern library.** The Life community shares its patterns in a format called RLE, in which the glider is `bob$2bo$3o!`. Write a parser for it, and help yourself to the thousands of patterns on [the LifeWiki](https://conwaylife.com/wiki/).
3. **How long does soup last?** For each of a hundred random soups, how many generations does it take to settle, and what's left when it has? Draw the histogram. You have the tool for that, in another project. How could `life` and `dice-lab` share it?

Solutions to the first two Extends are in the project's `solutions/` folder, and they import the `life` package from outside, as any other project would.

## Recap

You can now:

- [x] choose a set of tuples over a grid of lists, and say what it buys you
- [x] write set comprehensions, and comprehensions with more than one `for`
- [x] write a generator function, and explain what happens when you call it, and when it runs
- [x] explain laziness, and why an endless `while True` inside a generator is safe
- [x] predict what happens when a generator is gone through twice, and avoid being caught by it
- [x] choose between a list comprehension and a generator expression
- [x] use `islice`, `product` and `pairwise`, and know where to find the rest
- [x] use a `frozenset` where a set has to be hashable
- [x] mark private names with an underscore, and give a package a front door with `__all__`
- [x] describe a command line with `argparse`, and make `main` testable
- [x] animate in the terminal, and tidy up with `finally`, whatever happens
- [x] run one test over many cases with `parametrize`, and capture output with `capsys`
- [x] put a repository on GitHub, write its README, and `push`

**Read more:** [Generators](https://docs.python.org/3/tutorial/classes.html#generators) and [generator expressions](https://docs.python.org/3/tutorial/classes.html#generator-expressions) · [`itertools`](https://docs.python.org/3/library/itertools.html) · [The `argparse` tutorial](https://docs.python.org/3/howto/argparse.html) · [How to parametrize tests](https://docs.pytest.org/en/stable/how-to/parametrize.html) · [GitHub's quickstart](https://docs.github.com/en/get-started/start-your-journey/hello-world) · [The LifeWiki](https://conwaylife.com/wiki/), for when you've lost a weekend to this

One project of Part 1 remains, and it makes pictures: the Mandelbrot set, as PNG files, in colour. Project 7 is about numbers, which hold more surprises than you'd think, and about what functions can do when you stop thinking of them as subroutines and start treating them as values.
