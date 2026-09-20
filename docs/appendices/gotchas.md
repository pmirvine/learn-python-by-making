# The gotchas gallery

Every language has places where what it does isn't what a newcomer expects. Python has fewer than most, and nearly all of them follow from two or three rules, once you know the rules. This is a gallery of the ones that this tutorial met, each with the smallest example that shows it, the reason, and the project where it's dealt with properly.

Every example on this page is run, and its output checked, whenever the tutorial is built. If it says so here, Python really does it.

## Names and objects

Most of this section is one fact, from [Project 1](../part-1-console/p01-hi-lo.md): **a name is a label tied to an object, and not a box with a value in it.** Assignment ties a label. It never copies.

### The default that remembers

```pycon
>>> def add_guess(guess, guesses=[]):
...     guesses.append(guess)
...     return guesses
>>> add_guess("red")
['red']
>>> add_guess("blue")
['red', 'blue']
```

A default value is made **once**, when the `def` runs, and not at each call. Every call that doesn't pass `guesses` shares the same list. Write `guesses=None`, and then `if guesses is None: guesses = []`. A dataclass refuses a mutable default outright, and wants `field(default_factory=list)`. [Project 4](../part-1-console/p04-codebreaker.md), and [Project 5](../part-1-console/p05-colossal-cupboard.md).

### Two names, one list

```pycon
>>> a = [1, 2, 3]
>>> b = a
>>> b.append(4)
>>> a
[1, 2, 3, 4]
>>> grid = [[0] * 3] * 2
>>> grid[0][0] = 9
>>> grid
[[9, 0, 0], [9, 0, 0]]
```

`b = a` ties a second label to the same list. `[row] * 2` is a list holding the same row twice. For a copy, say so: `a.copy()`, `a[:]` or `list(a)`. For a grid, build each row afresh: `[[0] * 3 for _ in range(2)]`. [Project 4](../part-1-console/p04-codebreaker.md).

### A copy that isn't deep enough

```pycon
>>> from dataclasses import dataclass, field, replace
>>> @dataclass(frozen=True)
... class State:
...     room: str = "hall"
...     bag: list[str] = field(default_factory=list)
>>> before = State()
>>> after = replace(before, room="attic")
>>> after.bag.append("torch")
>>> before.bag
['torch']
```

`copy()`, slicing and `dataclasses.replace` are all *shallow*: the new object holds the same inner objects as the old. `frozen=True` stops you from assigning to a field, and not from changing what the field is. Build new inner values (`state.bag + ["torch"]`), or use `copy.deepcopy`. [Project 26](../part-5-tui/p26-adventure-third-edition.md).

### `is` isn't `==`

```pycon
>>> [1, 2] == [1, 2]
True
>>> [1, 2] is [1, 2]
False
>>> best = None
>>> best is None
True
```

`==` asks whether two objects are *equal*. `is` asks whether they're *the same object*. Use `is` for `None`, of which there's only one, and `==` for everything else. `is` will sometimes seem to work for small numbers and short strings, because Python reuses them. Don't rely on it. [Project 4](../part-1-console/p04-codebreaker.md).

### One list, for every snake

```pycon
>>> class Snake:
...     body = []
...     def grow(self):
...         self.body.append("segment")
>>> first, second = Snake(), Snake()
>>> first.grow()
>>> second.body
['segment']
```

Anything assigned in the body of a class belongs to the *class*, and is shared by every instance. `self.body.append` doesn't assign, and so it finds the class's list, and changes it. Make per-object things in `__init__`: `self.body = []`. [Project 9](../part-2-pygame/p09-snake.md).

### Closures look the variable up late

```pycon
>>> buttons = [lambda: colour for colour in ["red", "green", "blue"]]
>>> [press() for press in buttons]
['blue', 'blue', 'blue']
>>> buttons = [lambda colour=colour: colour for colour in ["red", "green", "blue"]]
>>> [press() for press in buttons]
['red', 'green', 'blue']
```

A function that uses a variable from outside itself remembers the *variable*, and not the value that it had. By the time any button is pressed, the loop has finished, and `colour` is `"blue"`. A default argument is worked out at once, and so `colour=colour` takes a snapshot. `functools.partial` does the same, more readably. [Project 7](../part-1-console/p07-fractal-factory.md), and [Project 15](../part-2-pygame/p15-sprite-editor.md).

### Hiding a built-in

```pycon
>>> list = [3, 1, 2]
>>> list("abc")
Traceback (most recent call last):
  ...
TypeError: 'list' object is not callable
>>> del list
>>> list("abc")
['a', 'b', 'c']
```

`list`, `max`, `sum`, `id`, `type`, `input` and the rest aren't reserved words. They're ordinary names, in the outermost scope, and a name of yours, nearer in, hides them. Ruff will tell you. [Project 7](../part-1-console/p07-fractal-factory.md).

## Numbers

### A tenth isn't a tenth

```pycon
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
>>> import math
>>> math.isclose(0.1 + 0.2, 0.3)
True
```

Floats are binary fractions, and a tenth has no exact one, as a third has no exact decimal. It's true of every language that uses the hardware's floating point. Don't compare floats with `==`. Use `math.isclose`, or `pytest.approx` in tests, and for money use whole pence, or `decimal`. [Project 7](../part-1-console/p07-fractal-factory.md).

### Division

```pycon
>>> 7 / 2, 6 / 2
(3.5, 3.0)
>>> 7 // 2, -7 // 2
(3, -4)
>>> round(0.5), round(1.5), round(2.5)
(0, 2, 2)
```

`/` always gives a float, even when it divides exactly. `//` rounds *down*, which for a negative number is away from nought, and isn't what C or JavaScript does. And `round` sends a half to the nearest *even* number, which is what statisticians want, and not what you were taught at school. [Project 1](../part-1-console/p01-hi-lo.md), and [Project 7](../part-1-console/p07-fractal-factory.md).

### `True` is a number

```pycon
>>> True + True
2
>>> sum([True, False, True])
2
>>> isinstance(True, int)
True
```

`bool` is a kind of `int`, for historical reasons. It's occasionally handy, as in the `sum` there, which counts. It's also why a function that's given `True` where it expected a number won't complain.

### Version numbers aren't strings, or numbers

```pycon
>>> "1.10.0" > "1.9.0"
False
>>> from packaging.version import Version
>>> Version("1.10.0") > Version("1.9.0")
True
```

Strings compare character by character, and `"1"` comes before `"9"`. [Project 27](../part-6-shipping/p27-ship-it.md).

## Truth, and strings

### Nearly everything is true

```pycon
>>> bool("0"), bool("False"), bool(" ")
(True, True, True)
>>> bool(""), bool(0), bool([]), bool(None)
(False, False, False, False)
```

A string is false only when it's empty. Whatever comes back from `input()` is a string, and so it's true unless the user pressed ++enter++ and nothing else. Compare it with something: `answer.lower() == "y"`. [Project 1](../part-1-console/p01-hi-lo.md).

### The empty string is in everything

```pycon
>>> "" in "01234567"
True
>>> "7" in "01234567"
True
```

`in`, for strings, looks for a *substring*, and the empty string is a substring of every string. If the thing that you're testing may be empty, test for that first. [Project 8](../part-2-pygame/p08-mode2-sketchpad.md).

### Strings don't change

```pycon
>>> name = "ada"
>>> name.upper()
'ADA'
>>> name
'ada'
>>> name = name.upper()
>>> name
'ADA'
```

Strings are immutable, and every string method returns a *new* string. Calling one and throwing the result away does nothing at all. [Project 4](../part-1-console/p04-codebreaker.md).

## Collections

### `sort` gives you nothing back

```pycon
>>> rolls = [3, 1, 2]
>>> print(rolls.sort())
None
>>> rolls
[1, 2, 3]
>>> sorted([3, 1, 2])
[1, 2, 3]
```

Methods that change a list in place, such as `sort`, `append`, `reverse` and `extend`, return `None`, precisely so that you can't mistake them for functions that make a new one. `rolls = rolls.sort()` throws your list away. [Project 3](../part-1-console/p03-dice-lab.md).

### `{}` is a dictionary

```pycon
>>> type({})
<class 'dict'>
>>> type(set())
<class 'set'>
>>> type((5)), type((5,))
(<class 'int'>, <class 'tuple'>)
```

Dictionaries had the braces first. An empty set is `set()`. And it's the *comma* that makes a tuple, and not the brackets. [Project 4](../part-1-console/p04-codebreaker.md), and [Project 2](../part-1-console/p02-turtle-sketchbook.md).

### A generator can be used once

```pycon
>>> squares = (n * n for n in range(4))
>>> sum(squares)
14
>>> sum(squares)
0
```

When a generator's values have been handed over, it's empty, for ever, and it doesn't complain. The same goes for `zip`, `map`, `enumerate`, `reversed` and an open file. If you need the values twice, make a list. [Project 6](../part-1-console/p06-life.md).

### Changing a list that you're looping over

```pycon
>>> numbers = [1, 2, 2, 3]
>>> for number in numbers:
...     if number == 2:
...         numbers.remove(number)
>>> numbers
[1, 2, 3]
```

The loop keeps its place by counting. Take an item out, and everything after it moves up one, and the next item is skipped. Build a new list: `[n for n in numbers if n != 2]`. With a dictionary or a set, Python raises `RuntimeError` for the same offence.

### A key that isn't there

```pycon
>>> scores = {"ada": 3}
>>> scores["bob"]
Traceback (most recent call last):
  ...
KeyError: 'bob'
>>> scores.get("bob", 0)
0
```

A missing key is an error, and not `undefined`, or nought. `.get` takes a default. `collections.Counter` and `defaultdict` are for when every key should start at something. [Project 3](../part-1-console/p03-dice-lab.md), and [Project 23](../part-5-tui/p23-rich-dashboard.md).

### `zip` stops at the shortest

```pycon
>>> list(zip("abc", [1, 2]))
[('a', 1), ('b', 2)]
>>> list(zip("abc", [1, 2], strict=True))
Traceback (most recent call last):
  ...
ValueError: zip() argument 2 is shorter than argument 1
```

It doesn't say that it's dropped something. When the lengths *ought* to agree, say `strict=True`, and find out when they don't. [Project 3](../part-1-console/p03-dice-lab.md). [Project 11](../part-2-pygame/p11-sound-and-envelope.md) leaves it out on purpose, once.

## Operators

### `&` and `==`

```pycon
>>> dots, mask = 0b0110, 0b0100
>>> dots & mask == 1
False
>>> dots & mask
4
>>> bool(dots & mask)
True
```

Testing a bit gives you the *bit*, 4 here, and not 1. Compare with nought, or with the mask. (In C, Java and JavaScript there's a second trap in the same line, since their `==` binds tighter than `&`. Python's doesn't.) [Project 19](../part-4-web/p19-pyfax.md).

### `and` isn't `&`

```pycon
>>> 1 and 8
8
>>> 1 & 8
0
```

`and` and `or` work on truth, and hand back one of their operands. `&` and `|` work on the bits of numbers. 1 and 8 are both true, and have no bits in common. [Project 28](../part-6-shipping/p28-boot-to-basic.md), where it cost the author a bolt.

## Statements

### `match` captures a bare name

```pycon
>>> NORTH = "n"
>>> command = "s"
>>> match command:
...     case NORTH:
...         print("going north")
going north
>>> NORTH
's'
```

A bare name in a `case` isn't compared with anything. It's a *capture*: it matches whatever's there, and is assigned it. Here it has overwritten your constant as well. A dotted name, such as `Direction.NORTH`, is compared, and so is a literal. [Project 5](../part-1-console/p05-colossal-cupboard.md).

### `except:` with nothing after it

```pycon
>>> def number_from(text):
...     try:
...         return int(txet)
...     except:
...         return 0
>>> number_from("42")
0
```

There's a typing mistake in that function, and the bare `except` has hidden it: the `NameError` was caught along with everything else. Name the exception that you expect, keep the `try` as small as you can, and let everything else be heard. [Project 1](../part-1-console/p01-hi-lo.md), and [Project 5](../part-1-console/p05-colossal-cupboard.md).

### Forgetting `super().__init__()`

```pycon
>>> class Tool:
...     def __init__(self):
...         self.changes = {}
>>> class Pencil(Tool):
...     def __init__(self, colour):
...         self.colour = colour
>>> Pencil("red").changes
Traceback (most recent call last):
  ...
AttributeError: 'Pencil' object has no attribute 'changes'
```

A child's `__init__` *replaces* its parent's. If the parent's is to run as well, the child has to call it. [Project 15](../part-2-pygame/p15-sprite-editor.md).

## Time

### `.seconds` isn't the number of seconds

```pycon
>>> from datetime import timedelta
>>> gap = timedelta(days=2, hours=1)
>>> gap.seconds
3600
>>> gap.total_seconds()
176400.0
```

A `timedelta` is kept as days, seconds and microseconds, and `.seconds` is only the middle part. You nearly always want `total_seconds()`. [Project 23](../part-5-tui/p23-rich-dashboard.md).

### Two kinds of `datetime`

```pycon
>>> from datetime import UTC, datetime
>>> datetime(2026, 9, 20, 12, 0) < datetime(2026, 9, 20, 12, 0, tzinfo=UTC)
Traceback (most recent call last):
  ...
TypeError: can't compare offset-naive and offset-aware datetimes
```

A `datetime` that doesn't know its time zone is *naive*, and one that does is *aware*, and they won't mix. Work in UTC, with aware values, and convert to local time only to show it to somebody. [Project 23](../part-5-tui/p23-rich-dashboard.md).

## Async

### A coroutine that's never awaited

```pycon
>>> import asyncio
>>> async def headline():
...     return "Hedgehog wins"
>>> async def main():
...     forgotten = headline()
...     print(type(forgotten).__name__)
...     print(await forgotten)
>>> asyncio.run(main())
coroutine
Hedgehog wins
```

Calling an `async def` function doesn't run it. It makes a coroutine, which does nothing until it's awaited. And writing `async def` doesn't make what's inside it asynchronous: one `time.sleep`, or any slow call that isn't awaited, freezes every task in the program. [Project 25](../part-5-tui/p25-newsroom.md).

## Files, names and tools

These can't be shown in a REPL, and they've all cost somebody an afternoon.

| The trap | What happens | Where |
|---|---|---|
| Calling your file `turtle.py`, `random.py` or `test.py` | `import turtle` finds *your* file first, and your program imports itself | [Project 2](../part-1-console/p02-turtle-sketchbook.md) |
| Leaving out `encoding="utf-8"` | before Python 3.15, the default depended on the computer, and files filled up with `Ã©` | [Project 5](../part-1-console/p05-colossal-cupboard.md) |
| Installing `pygame` as well as `pygame-ce` | they're two distributions of one package, `pygame`, and each overwrites the other | [Project 8](../part-2-pygame/p08-mode2-sketchpad.md) |
| A run-time dependency in the `dev` group | it works on your machine, and on nobody else's | [Project 27](../part-6-shipping/p27-ship-it.md) |
| Pasting data into code: `f"… WHERE name = '{name}'"`, `shell=True`, HTML built with `+` | somebody's name has a quotation mark in it, or somebody means you harm. Pass data *as data*: `?` placeholders, a list of arguments, a template that escapes | Projects [18](../part-4-web/p18-svg-plotter.md), [20](../part-4-web/p20-pyfax-live.md) and [23](../part-5-tui/p23-rich-dashboard.md) |
| Trusting `maxlength` in a form | anybody can send your server anything. Check everything again on the server | [Project 20](../part-4-web/p20-pyfax-live.md) |
| Flask's `--debug` on a real server | its error page will run any Python, for anybody | [Project 20](../part-4-web/p20-pyfax-live.md) |
| Adding a file to `.gitignore` after committing it | Git goes on tracking it. `git rm --cached` lets go | [Project 9](../part-2-pygame/p09-snake.md) |
| `git restore file` | your uncommitted changes are gone, and there's no recycle bin. Look at `git diff` first | [Project 4](../part-1-console/p04-codebreaker.md) |
| Amending, or rebasing, commits that you've pushed | your history and everybody else's no longer agree | Projects [6](../part-1-console/p06-life.md) and [21](../part-4-web/p21-adventure-online.md) |
| Committing a secret, and deleting it in the next commit | it's in the history for ever. Change the secret | [Project 21](../part-4-web/p21-adventure-online.md) |
| 100% test coverage | it says that every line was *run*, and not that anything was checked | [Project 17](../part-3-interpreters/p17-tiny-basic.md) |
| A relative image in a README | it works on GitHub, and is broken on the package index | [Project 27](../part-6-shipping/p27-ship-it.md) |
