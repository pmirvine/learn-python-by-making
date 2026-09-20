# Project 3 · Dice Lab

Roll two dice and add them up. Everybody knows that 7 comes up more than 2 does. But how much more? And what if you roll four dice and throw away the lowest, as players of a certain sort of game do when they're inventing a hero? You could work it out with probability theory. Or you could roll the dice five thousand times and look.

```text
Four dice, adding up the best three, 5,000 times:

  3  0.0%
  4 █ 0.4%
  5 ██ 0.5%
  6 ██████ 1.6%
  7 ██████████ 2.6%
  8 ██████████████████ 4.9%
  9 ████████████████████████████ 7.4%
 10 ████████████████████████████████████ 9.8%
 11 ████████████████████████████████████████████ 11.8%
 12 ███████████████████████████████████████████████ 12.8%
 13 ██████████████████████████████████████████████████ 13.5%
 14 █████████████████████████████████████████████ 12.1%
 15 ███████████████████████████████████ 9.3%
 16 ███████████████████████████ 7.4%
 17 ███████████████ 4.1%
 18 ██████ 1.7%

Average: 12.23
Longest streak: 5 in a row, of 11
```

Thousands of results need somewhere to live, and that makes this the chapter about Python's two workhorse collections, the **list** and the **dictionary**, and about the tools that make them such a pleasure: comprehensions, slices, `enumerate`, `zip` and `Counter`. If you've only ever had arrays and index variables to work with, some of this is going to feel like cheating.

It's also the chapter in which you stop *hoping* that your code works. You'll add type hints, write your first automated tests, and let a linter read your code, and it will find something.

| | |
|---|---|
| **You'll learn** | Lists and dictionaries; `Counter`; list and dict comprehensions; slicing; `enumerate`, `zip` and `sorted`; functions as values in a dict; type hints |
| **New tool skill** | pytest: writing and running tests, reading a failure, VS Code's Testing panel. Ruff on the command line. |
| **Time** | 3 to 4 hours |
| **Before you start** | [Project 2](p02-turtle-sketchbook.md) |

## Predict

!!! question "Predict"
    ```python
    letters = ["a", "b", "c", "d", "e"]
    print(letters[1:3], letters[-2:], letters[::2])
    print(letters[10:], letters[2:2])
    ```

??? success "Answer"
    ```text
    ['b', 'c'] ['d', 'e'] ['a', 'c', 'e']
    [] []
    ```

    A *slice* takes a run of items out of a list. It follows the `range` convention, start included and end excluded, and it counts backwards from the end if you give it negative numbers. Unlike a plain index, a slice is never out of range: ask for more than there is and you get what there is. Stage 3.

!!! question "Predict"
    ```python
    rolls = [3, 1, 2]
    result = rolls.sort()
    print(result, rolls)
    print(sorted("dice"))
    ```

??? success "Answer"
    ```text
    None [1, 2, 3]
    ['c', 'd', 'e', 'i']
    ```

    `rolls.sort()` sorts the list where it stands and returns `None`. `sorted(…)` leaves its argument alone and returns a *new* list, and it will take anything you can loop over, even a string. Mixing them up, with `rolls = rolls.sort()`, is a rite of passage. Stage 1.

!!! question "Predict"
    ```python
    counts = {"six": 2}
    counts["one"] = counts.get("one", 0) + 1
    print(counts)
    print(counts["two"])
    ```

??? success "Answer"
    ```text
    {'six': 2, 'one': 1}
    Traceback (most recent call last):
      ...
    KeyError: 'two'
    ```

    Looking up a key that isn't in a dictionary is an error: you don't get `None`, or 0, or `undefined`. `.get()` is the polite way of asking, with a fallback for when the key is missing. Stage 2.

!!! question "Predict"
    ```python
    def double(n: int) -> int:
        return n * 2


    print(double("ha"))
    ```

??? success "Answer"
    ```text
    haha
    ```

    The `: int` and `-> int` are *type hints*. They say that `double` takes an `int` and returns one. Python itself pays them no attention whatever. So what are they for? Stage 4.

## Build

### Stage 1: A list of rolls

```console
$ cd making
$ uv init --no-package dice-lab
$ cd dice-lab
$ code .
```

Clear out `main.py`, and start with a script, as you did in Project 1:

<!-- listing: projects/03-dice-lab/stages/stage1.py -->
```python title="main.py"
import random

TIMES = 20

totals = []
for _ in range(TIMES):
    total = random.randint(1, 6) + random.randint(1, 6)
    totals.append(total)

print(totals)
print(f"Lowest {min(totals)}, highest {max(totals)}")
print(f"Average {sum(totals) / len(totals):.2f}")
print(f"Sevens: {totals.count(7)}")
print(f"In order: {sorted(totals)}")
```

!!! example "Run it"
    ```console
    $ uv run main.py
    [7, 7, 8, 10, 6, 6, 7, 7, 8, 9, 9, 10, 4, 8, 9, 7, 7, 7, 4, 4]
    Lowest 4, highest 10
    Average 7.20
    Sevens: 7
    In order: [4, 4, 4, 6, 6, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10]
    ```

    Yours will differ, of course.

`totals = []` makes an empty *list*, and `totals.append(total)` adds an item to the end of it. A list is an ordered collection that grows and shrinks as you please. You don't say in advance how big it's going to be, and you don't say what type of thing it holds. In the REPL:

```pycon
>>> rolls = [4, 6, 1]
>>> rolls.append(5)
>>> rolls
[4, 6, 1, 5]
>>> len(rolls)
4
>>> rolls[0]
4
>>> rolls[-1]
5
>>> 6 in rolls
True
>>> rolls[1] = 2
>>> rolls
[4, 2, 1, 5]
```

Most of that you met in Project 2, on tuples: `len`, indexing from nought, `for … in`. Lists do everything tuples do. The news is in the last two lines: **a list can be changed**. You can replace items, add them and remove them. A tuple is a fixed record, like a coordinate or a colour. A list is a collection of things of the same kind that you expect to vary.

Negative indexes count from the end: `rolls[-1]` is the last item and `rolls[-2]` the one before. You'll never write `rolls[len(rolls) - 1]` again.

`in` tests for membership. And `min`, `max`, `sum`, `len` and `sorted` are built-in functions that work on any collection, not methods peculiar to lists. They'll work just as well on the tuples, dictionaries, sets and generators to come.

!!! warning "Gotcha"
    There are two ways to sort, and the second Predict was about telling them apart.

    `sorted(rolls)` **returns a new, sorted list** and leaves `rolls` untouched. `rolls.sort()` **sorts `rolls` itself, in place**, and returns `None`.

    That `None` is deliberate, and it's a convention you can rely on across Python: a method that changes an object in place returns `None`, so that you can't mistake it for one that gives you a new object. `append` follows it too. So `rolls = rolls.sort()` sorts your list and then throws it away, leaving you with `None`. The symptom arrives a line or two later, and looks like `TypeError: 'NoneType' object is not subscriptable`.

!!! info "Coming from BBC BASIC"
    `DIM totals%(19)` gave you twenty numbered boxes, of one type, for ever. A list needs no `DIM`. It starts empty and grows, it'll hold anything, and it knows its own length. What BASIC never had is all the things you can do with a list *without a loop*: `sum`, `max`, `sorted`, `in`, `.count()`.

!!! success "Checkpoint"
    ```console
    $ git add .
    $ git commit -m "Roll two dice twenty times and summarise"
    ```

### Stage 2: Counting things, and a histogram

Twenty numbers you can take in at a glance. For a thousand, you need to count how often each total came up. `totals.count(7)` would do it, one total at a time, but it reads through the whole list for every question you ask. What you want is a table, of totals against counts, filled in with a single pass. Python's table is the *dictionary*.

#### Dictionaries

A dictionary, a `dict`, maps *keys* to *values*. You write one with braces and colons, and look things up with square brackets:

```pycon
>>> counts = {7: 3, 6: 1}
>>> counts[7]
3
>>> counts[8] = 2
>>> counts
{7: 3, 6: 1, 8: 2}
>>> len(counts)
3
>>> 6 in counts
True
```

Assigning to a new key adds it, and assigning to an existing one replaces its value. `in` asks about *keys*. A dictionary remembers the order in which its keys were added.

Looking up a key that isn't there is an error, as you saw in the third Predict:

```pycon
>>> counts[2]
Traceback (most recent call last):
  ...
KeyError: 2
```

So a tally can't simply say `counts[total] += 1`, because the first time each total turns up there's nothing there to add to. `.get()` looks a key up and gives you a default if it's missing:

```pycon
>>> counts.get(2, 0)
0
>>> counts[2] = counts.get(2, 0) + 1
>>> counts
{7: 3, 6: 1, 8: 2, 2: 1}
```

Looping over a dictionary gives you its keys. More often you want both halves, and `.items()` gives you `(key, value)` tuples to unpack, just like the `for x, height in …` loop in your garden:

```pycon
>>> for total, count in counts.items():
...     print(f"{total} came up {count} times")
...
7 came up 3 times
6 came up 1 times
8 came up 2 times
2 came up 1 times
```

Keys can be numbers, strings or tuples; in fact anything that can't change. (Project 4 explains why.) Values can be anything at all.

!!! info "Coming from JavaScript"
    A `dict` is what you've been using objects, or a `Map`, for. Two differences will catch you out. Keys aren't turned into strings, so `1` and `"1"` are different keys. And a missing key raises `KeyError`, where JavaScript would have quietly handed you `undefined`.

#### `Counter`

Counting things is so common that the standard library has a dictionary made for the job. Give a `Counter` a collection, and it counts it:

```pycon
>>> from collections import Counter
>>> counts = Counter([7, 6, 7, 8, 7, 8])
>>> counts
Counter({7: 3, 8: 2, 6: 1})
>>> counts[7]
3
>>> counts[2]
0
>>> counts.most_common(2)
[(7, 3), (8, 2)]
```

A `Counter` *is* a dictionary, and everything above still works. It differs in two ways. A missing key counts as 0, with no `KeyError`. And it has `most_common`, which returns a list of `(item, count)` tuples, biggest first.

It was worth doing the tally by hand first, because `.get(key, 0) + 1` is an idiom you'll meet in other people's code. But when there's a tool that fits, use it. There's the whole program:

<!-- listing: projects/03-dice-lab/stages/stage2.py -->
```python title="main.py"
import random
from collections import Counter

TIMES = 1000
WIDTH = 50

totals = []
for _ in range(TIMES):
    total = random.randint(1, 6) + random.randint(1, 6)
    totals.append(total)

counts = Counter(totals)
biggest = max(counts.values())

for total in range(2, 13):
    count = counts[total]
    bar = "█" * round(count / biggest * WIDTH)
    print(f"{total:>3} {bar} {count / TIMES:.1%}")

value, count = counts.most_common(1)[0]
print(f"\nMost common: {value}, which came up {count} times.")
```

!!! example "Run it"
    ```text
      2 █████████ 2.7%
      3 ██████████████████ 5.5%
      4 ████████████████████████ 7.6%
      5 ██████████████████████████████████████ 11.9%
      6 ██████████████████████████████████████████████████ 15.6%
      7 ██████████████████████████████████████████████████ 15.7%
      8 █████████████████████████████████████████████ 14.1%
      9 ███████████████████████████████████████ 12.1%
     10 ██████████████████████████ 8.1%
     11 █████████████ 4.1%
     12 ████████ 2.6%

    Most common: 7, which came up 157 times.
    ```

    There's the famous triangle. Seven wins because there are six ways of making it (1+6, 2+5, 3+4, and the same the other way round), and only one way of making 2. Make `TIMES` a million. It takes a second or two, and the triangle is perfect.

To type the `█`, copy it from this page. It's an ordinary character as far as Python is concerned, and you can multiply a string, as you know from Project 0.

Some details:

- `counts.values()` is all of the counts without their keys. There's a `.keys()` as well, though you rarely need it, since looping over the dictionary itself gives you the keys.
- The histogram loops over `range(2, 13)` and not over `counts`. A dictionary's keys come in the order they were first seen, which here is random. And a total that never came up wouldn't be in there at all, though its row should still be shown.
- The bars are scaled so that the longest of them is exactly `WIDTH` characters, however many rolls there were.
- Two more from the format mini-language: `:>3` pads to three characters, aligned right, and `:.1%` multiplies by a hundred and adds a percent sign.
- `counts.most_common(1)` is a list holding one tuple. `[0]` takes the tuple out, and the assignment unpacks it.

!!! success "Checkpoint"
    ```console
    $ git commit -am "Count the totals and draw a histogram"
    ```

### Stage 3: Comprehensions, slices and friends

The lab should run more than one experiment, so it's time for functions. This stage is also where the code starts to look like *Python*, and not like some other language wearing Python's clothes. Here's the whole of the new `main.py`. Read it through, and then we'll take it apart.

<!-- listing: projects/03-dice-lab/stages/stage3.py -->
```python title="main.py"
"""Dice Lab: roll a lot of dice and see what happens."""

import random
from collections import Counter

BAR = "█"
TIMES = 2000


def roll(dice=2, sides=6):
    """Roll some dice and return a list of what each of them shows."""
    return [random.randint(1, sides) for _ in range(dice)]


def two_dice():
    """Two ordinary dice, added together."""
    return sum(roll())


def advantage():
    """Two twenty-sided dice, keeping the higher."""
    return max(roll(2, 20))


def ability_score():
    """Four dice, adding up the best three."""
    return sum(sorted(roll(4))[1:])


def histogram(results, width=50):
    """Return a bar chart of how often each result came up, as a list of lines."""
    counts = Counter(results)
    biggest = max(counts.values())
    lines = []
    for value in range(min(counts), max(counts) + 1):
        count = counts[value]
        bar = BAR * round(count / biggest * width)
        lines.append(f"{value:>3} {bar} {count / len(results):.1%}")
    return lines


def longest_streak(results):
    """Return the longest run of identical results, as (value, length)."""
    if not results:
        return None, 0
    best = (results[0], 1)
    length = 1
    for previous, current in zip(results, results[1:]):
        length = length + 1 if current == previous else 1
        if length > best[1]:
            best = (current, length)
    return best


def main():
    results = [ability_score() for _ in range(TIMES)]

    for line in histogram(results):
        print(line)

    print(f"\nThe first ten: {results[:10]}")
    print(f"Average: {sum(results) / len(results):.2f}")

    heroes = [score for score in results if score >= 16]
    print(f"Scores of 16 or more: {len(heroes)} ({len(heroes) / TIMES:.1%})")

    value, length = longest_streak(results)
    print(f"Longest streak: {length} in a row, of {value}")


if __name__ == "__main__":
    main()
```

!!! example "Run it"
    You get a histogram like the one at the top of the chapter, and then something like:

    ```text
    The first ten: [12, 15, 11, 12, 15, 15, 10, 15, 13, 7]
    Average: 12.15
    Scores of 16 or more: 262 (13.1%)
    Longest streak: 3 in a row, of 16
    ```

    Change `ability_score()` to `advantage()` in `main`, and see a very different shape. Keeping the better of two dice is a big help.

#### List comprehensions

Twice now you've written the same four lines: make an empty list, loop, work something out, append it. Python has a single expression for that:

```python
totals = []
for _ in range(TIMES):
    totals.append(two_dice())
```

becomes

```python
totals = [two_dice() for _ in range(TIMES)]
```

That's a *list comprehension*. Read it from the middle outwards: *for each of these, give me this, and make a list of them all*. The expression at the front is the thing you'd have appended.

```pycon
>>> [n * n for n in range(6)]
[0, 1, 4, 9, 16, 25]
>>> [word.upper() for word in ("roll", "the", "dice")]
['ROLL', 'THE', 'DICE']
```

An `if` on the end filters, keeping only the items that pass:

```pycon
>>> [n * n for n in range(10) if n % 2 == 0]
[0, 4, 16, 36, 64]
```

`roll` builds its list of dice with one. `main` builds its results with another, and picks out the heroes with a third, a filter that doesn't change the items at all.

There are dictionary comprehensions as well, with braces and a colon:

```pycon
>>> counts = Counter([7, 6, 7, 8])
>>> {total: count / 4 for total, count in counts.items()}
{7: 0.5, 6: 0.25, 8: 0.25}
```

A comprehension isn't just shorter than the loop. It says what you mean. `[… for … in …]` tells the reader at a glance *this builds a list, and does nothing else*, where a loop has to be read to the end to make sure it isn't up to something on the side. It's the biggest single difference between Python written by a Python programmer and Python written by a visitor.

!!! tip "Pythonic"
    Comprehensions are for building collections. If you aren't going to use the list, don't build one. This works, but it's a loop in fancy dress:

    ```python
    [print(line) for line in histogram(results)]
    ```

    Write the `for` loop. And when a comprehension gets too long to take in at one look, with two `for`s and an `if`, say, turn it back into a loop. Nobody will think less of you.

#### Slices

`ability_score` is the chapter's best line:

```python
return sum(sorted(roll(4))[1:])
```

Roll four dice. Sort them, smallest first. Take everything from position 1 onwards, which drops the lowest. Add up what's left. `[1:]` is a *slice*.

A slice is written `[start:stop]`, and if you understood `range`, you understand slices: start included, stop excluded. Leave either end out and it means "from the beginning" or "to the end".

```pycon
>>> results = [14, 11, 12, 9, 13, 13, 11, 15]
>>> results[2:5]
[12, 9, 13]
>>> results[:3]
[14, 11, 12]
>>> results[-3:]
[13, 11, 15]
>>> results[1:]
[11, 12, 9, 13, 13, 11, 15]
```

The first three, the last three, everything but the first. The convention pays off again: `results[:3]` has three items in it, and `results[:3]` and `results[3:]` between them are the whole list, with nothing missed and nothing twice. There can be a step as well, and it can be negative:

```pycon
>>> results[::2]
[14, 12, 13, 11]
>>> results[::-1]
[15, 11, 13, 13, 9, 12, 11, 14]
```

A slice is always a **new list**, so `results[:]` is a quick way of copying one. And slices are forgiving: `results[:100]` is simply the whole list, where `results[100]` would be an `IndexError`. Tuples and strings can be sliced too, giving tuples and strings.

#### `enumerate`: the item and its number

Now to keep two promises. In Project 0 you wanted each colour's name *and* its number, and had to resort to `range(8)` and indexing. Project 2 told you not to write `range(len(…))`, and said there was something better. It's this:

```pycon
>>> for position, result in enumerate(results[:3]):
...     print(position, result)
...
0 14
1 11
2 12
```

`enumerate` wraps any collection and hands you `(number, item)` tuples to unpack. To count from 1, as people do, give it a `start`:

```pycon
>>> for place, result in enumerate(sorted(results, reverse=True)[:3], start=1):
...     print(f"{place}. {result}")
...
1. 15
2. 14
3. 13
```

#### `zip`: two lists in step

`zip` takes two collections, or more, and hands you their items in pairs: the first of each, then the second of each, and so on, like the two sides of a zip fastener.

```pycon
>>> players = ["Ann", "Bob", "Cy"]
>>> scores = [14, 9, 17]
>>> for player, score in zip(players, scores, strict=True):
...     print(f"{player} rolled {score}")
...
Ann rolled 14
Bob rolled 9
Cy rolled 17
```

If the lists are of different lengths, plain `zip` stops without complaint at the end of the shorter one, and a missing score passes unnoticed. `strict=True` turns that into an error. When the lists are *supposed* to match, always say so.

`longest_streak` uses a well-known trick: zip a list with *itself, moved along by one*. `results[1:]` is the list without its first item, so pairing `results` with it gives you each item alongside its successor:

```pycon
>>> list(zip([1, 2, 2, 3], [2, 2, 3]))
[(1, 2), (2, 2), (2, 3)]
```

Here the lists differ in length by design, and stopping at the shorter one is what's wanted. Each pair is a `(previous, current)`, and the function counts how long `current` goes on being equal to `previous`.

Notice, too, how `longest_streak` starts: `if not results:`. An empty list counts as false, as Project 1 promised it would. That's the idiomatic way to ask "is there anything in it?"

!!! success "Checkpoint"
    ```console
    $ git commit -am "Add experiments, comprehensions and the longest streak"
    ```

### Stage 4: Hints, tests and a second opinion

The program works. You know it works, because you ran it and the histogram looked about right. But "about right" is as far as that gets you. Is `longest_streak` right when the streak comes at the very end? When there's only one result? You've been testing by running the program and squinting at it, and you'd have to do it all again after every change. This stage replaces hope with evidence, in three ways.

#### Type hints

A *type hint* says what type a parameter or a return value is meant to be. The syntax is a colon after a parameter, and an arrow before the `def` line's final colon:

```python
def roll(dice: int = 2, sides: int = 6) -> list[int]:
```

That reads: `dice` is an `int`, defaulting to 2. `sides` is an `int`, defaulting to 6. The function returns a list of `int`s.

And as the fourth Predict showed, **Python doesn't check them.** At run time a hint is just a note. `double("ha")` goes right ahead and returns `"haha"`. So who are they for?

- **Whoever reads the code**, including you next month. `histogram(results, width)` doesn't tell you what `results` is supposed to be. `results: list[int]` does.
- **Your editor.** Once Pylance knows that `results` is a list, typing `results.` brings up a list's methods. Hover over any call to see what it wants and what it gives back.
- **Type checkers**: tools that read the hints and find the places where your code contradicts them, without running it. You'll switch one on in Project 4.

Here are the hints for the functions you have. Add them to your own `def` lines:

```python
def two_dice() -> int:
def histogram(results: list[int], width: int = 50) -> list[str]:
def longest_streak(results: list[int]) -> tuple[int | None, int]:
def main() -> None:
```

`list[int]` is a list of ints, and `dict[str, int]` would be a dictionary from strings to ints. `tuple[int | None, int]` is a tuple of exactly two items, the first of which is either an `int` *or* `None`. The `|` means "or". `-> None` is for a function that doesn't return anything.

From here on, every function in this tutorial has hints. They cost a few seconds to write, and they repay it the first time you come back to code you've forgotten.

!!! info "Coming from C#, Java or TypeScript"
    These look like type declarations, and they aren't. Nothing is enforced when the program runs, and there's no compilation step to fail. Python's typing is *gradual*: you can hint some of your functions and not others, and unhinted code works as it always did. TypeScript is the nearest relation: checked by a separate tool, and then ignored at run time.

#### A menu made of functions

One more feature before the tests. The user should choose the experiment, so add this below the three experiment functions, and `from collections.abc import Callable` to the imports:

<!-- listing: projects/03-dice-lab/main.py -->
```python title="main.py"
EXPERIMENTS: dict[str, tuple[str, Callable[[], int]]] = {
    "1": ("Two dice, added together", two_dice),
    "2": ("Two twenty-sided dice, keeping the higher", advantage),
    "3": ("Four dice, adding up the best three", ability_score),
}
```

Look at what's in that dictionary. The keys are strings. Each value is a tuple of a description and **a function**. Not a call to a function: there are no brackets after `two_dice`. It's the function itself.

Remember Project 1: everything is an object, and a variable is a label tied to one. `def two_dice():` makes a function object and ties the name `two_dice` to it. That object can be tied to other names, put in a tuple, stored in a dictionary and passed around, like any other. When you eventually want it to *run*, you put brackets after whatever name it's going by at the time.

The hint is the fiercest you'll see for a while. `Callable[[], int]` means "something you can call, with no arguments, that returns an `int`". Hints can be put on variables as well as parameters, and this one is worth having, because it tells the reader what shape this table is.

Two small functions finish the job: `average`, because you're about to want to test it, and Project 1's `ask_for_number`, with hints and a refusal to take zero.

<!-- listing: projects/03-dice-lab/main.py -->
```python title="main.py"
def average(results: list[int]) -> float:
    """Return the mean of the results."""
    return sum(results) / len(results)
# ...
def ask_for_number(prompt: str) -> int:
    """Keep asking until the user types a whole number greater than zero."""
    while True:
        reply = input(prompt)
        try:
            number = int(reply)
        except ValueError:
            print(f"{reply!r} isn't a whole number.")
            continue
        if number > 0:
            return number
        print("It needs to be more than zero.")
```

Delete the `TIMES` constant, and replace `main`:

<!-- listing: projects/03-dice-lab/main.py -->
```python title="main.py"
def main() -> None:
    print("Welcome to the Dice Lab.\n")
    for key, (description, _) in EXPERIMENTS.items():
        print(f"  {key}. {description}")

    choice = input("\nWhich experiment? ")
    while choice not in EXPERIMENTS:
        choice = input(f"Please choose from {', '.join(EXPERIMENTS)}: ")
    description, trial = EXPERIMENTS[choice]
    times = ask_for_number("How many times? ")

    results = [trial() for _ in range(times)]

    print(f"\n{description}, {times:,} times:\n")
    for line in histogram(results):
        print(line)

    value, length = longest_streak(results)
    print(f"\nAverage: {average(results):.2f}")
    print(f"Longest streak: {length} in a row, of {value}")
```

`EXPERIMENTS[choice]` looks up a tuple, and the assignment unpacks it, so that `trial` is now one more name for whichever function was chosen. Then `trial()` calls it, inside a comprehension, thousands of times. There's no `if choice == "1": … elif choice == "2": …` anywhere. To add a fourth experiment, you write the function and add one line to the table. Project 7 takes this idea a long way further.

Two other things are new. The menu's loop unpacks a tuple *within* a tuple: each item is `(key, (description, function))`, and the pattern on the left has the same shape. And `', '.join(EXPERIMENTS)` glues a collection of strings together with `', '` between each pair. Looping over a dictionary gives its keys, so that makes `1, 2, 3`. It does look back to front, with the glue first. Project 4 explains.

!!! example "Run it"
    ```console
    $ uv run main.py
    Welcome to the Dice Lab.

      1. Two dice, added together
      2. Two twenty-sided dice, keeping the higher
      3. Four dice, adding up the best three

    Which experiment? 3
    How many times? 5000
    ```

    and the histogram from the top of the chapter follows.

#### Tests

A *test* is a small piece of code that runs a piece of your program and checks that it did the right thing. You write it once, and then run it as often as you like, in a fraction of a second, for ever. The tool everybody uses is **pytest**. It isn't in the standard library, so add it to the project:

```console
$ uv add --dev pytest
```

`--dev` marks it as a *development dependency*: something that you need in order to work on the program, which somebody who's only running it wouldn't. Look in `pyproject.toml`, and you'll find that it's been noted there.

Now create `test_main.py`, beside `main.py`:

<!-- listing: projects/03-dice-lab/test_main.py -->
```python title="test_main.py"
import random

import pytest

from main import ability_score, average, histogram, longest_streak, roll


def test_roll_gives_one_number_per_die():
    assert len(roll(5)) == 5
    assert len(roll()) == 2
# ...
def test_longest_streak():
    assert longest_streak([1, 2, 2, 3, 3, 3, 2]) == (3, 3)
    assert longest_streak([4, 4, 1, 1]) == (4, 2)
    assert longest_streak([6]) == (6, 1)


def test_longest_streak_of_nothing():
    assert longest_streak([]) == (None, 0)
```

That's all a test is. pytest looks for files called `test_*.py`, and in them for functions called `test_*`, and runs each one. `assert` is a Python statement: if what follows it is true, nothing happens, and if it's false, it raises an `AssertionError`. A test passes if it gets to the end without an exception.

Notice that `from main import …` works, and doesn't start the Dice Lab asking its questions, thanks to the `if __name__ == "__main__":` at the bottom of `main.py`. That's the second thing that line has done for you. Project 4 takes the lid off it.

!!! example "Run it"
    ```console
    $ uv run pytest
    ```

    ```text
    collected 3 items

    test_main.py ...                                              [100%]

    ==== 3 passed in 0.01s ====
    ```

    One dot for each test that passed.

**Testing what's predictable.** `longest_streak`, `average` and `histogram` are easy to test. Give them a small list made by hand, for which you can work out the right answer in your head, and check that they agree. Make your test names say what should happen, so that a failure reads as a sentence. Add these:

<!-- listing: projects/03-dice-lab/test_main.py -->
```python title="test_main.py"
def test_histogram_scales_the_longest_bar_to_the_width():
    lines = histogram([2, 3, 3, 3, 3, 4, 4], width=8)
    assert lines == [
        "  2 ██ 14.3%",
        "  3 ████████ 57.1%",
        "  4 ████ 28.6%",
    ]


def test_histogram_shows_results_that_never_came_up():
    lines = histogram([1, 3])
    assert len(lines) == 3
    assert lines[1] == "  2  0.0%"


def test_average():
    assert average([1, 2, 3, 4]) == 2.5
    assert average([0.1, 0.2]) == pytest.approx(0.15)
```

This is why `histogram` *returns* its lines and leaves the printing to `main`. A function that returns something is easy to test. A function that prints is a nuisance to test. Letting your functions work things out, and leaving the input and output to a thin layer at the edge, is one of the most useful habits there is. You'll see it again and again in this tutorial.

`pytest.approx` is for floats. At the REPL, try `0.1 + 0.2 == 0.3`. It's `False`: floats are binary fractions, and can't hold most decimal ones exactly. So never test floats with a bare `==`, unless the numbers are small whole ones or halves, like 2.5, which binary can hold exactly. Project 7 has the whole story.

**Testing what isn't.** How do you test `roll`, when you can't know what it will return? There are two answers, and both are useful.

<!-- listing: projects/03-dice-lab/test_main.py -->
```python title="test_main.py"
def test_every_die_is_in_range():
    for _ in range(200):
        for die in roll(3, 20):
            assert 1 <= die <= 20


def test_the_same_seed_gives_the_same_rolls():
    random.seed(42)
    first = roll(10)
    random.seed(42)
    assert roll(10) == first


def test_ability_scores_run_from_3_to_18():
    scores = [ability_score() for _ in range(500)]
    assert min(scores) >= 3
    assert max(scores) <= 18
```

You can test *properties*, things that must be true whatever numbers come up: every die is in range, and no ability score is below 3. Or you can fix the dice. A computer's random numbers come from a formula, and `random.seed(n)` starts the formula off at a known place, so that the same "random" sequence follows every time.

Better still is to have as little random code as possible. In this program the randomness is all in `roll`. Everything else takes a plain list and gives a plain answer, and is as easy to test as arithmetic.

**When a test fails.** Go and break something on purpose. In `histogram`, change `count / biggest` to `count / len(results)`, which is a mistake anyone might make, and run the tests again:

```text
    def test_histogram_scales_the_longest_bar_to_the_width():
        lines = histogram([2, 3, 3, 3, 3, 4, 4], width=8)
>       assert lines == [
            "  2 ██ 14.3%",
            "  3 ████████ 57.1%",
            "  4 ████ 28.6%",
        ]
E       AssertionError: assert ['  2 █ 14.3%...  4 ██ 28.6%'] == ['  2 ██ 14.3...4 ████ 28.6%']
E
E         At index 0 diff: '  2 █ 14.3%' != '  2 ██ 14.3%'
E         Use -v to get more diff

test_main.py:34: AssertionError
==== short test summary info ====
FAILED test_main.py::test_histogram_scales_the_longest_bar_to_the_width
1 failed, 8 passed in 0.01s
```

pytest shows you the test, marks the line that failed with a `>`, and works out exactly where the two lists part company: at index 0, one block where there should have been two. That's the reason for using plain `assert`, and not some special `assertEqual` function. pytest takes the expression apart and shows you both sides of it. Put the bug right and run the tests again. Nine dots.

**In VS Code.** Click the flask icon in the left-hand bar, and then **Configure Python Tests**. Choose **pytest**, and then **. (Root directory)**. Your tests appear as a tree. You can run them all, or any one of them, with the play buttons. A green tick or a red cross appears beside each test in the editor, too, and you can right-click one and choose **Debug Test**, to stop at a breakpoint inside it with all of Project 2's machinery.

#### Ruff, on the command line

Ruff has been at work in your editor since Project 0, formatting on save and underlining things. It's also a command-line tool, which can check a whole project at once. Add it, and run it:

```console
$ uv add --dev ruff
$ uv run ruff check
```

```text
RUF007 Prefer `itertools.pairwise()` over `zip()` when iterating over successive pairs
  --> main.py:60:30
   |
58 |     best = (results[0], 1)
59 |     length = 1
60 |     for previous, current in zip(results, results[1:]):
   |                              ^^^
61 |         length = length + 1 if current == previous else 1
62 |         if length > best[1]:
   |
help: Replace `zip()` with `itertools.pairwise()`

Found 1 error.
```

Your clever trick, zipping a list with itself moved along by one, is so well known that the standard library has a function that does it, and Ruff knows it. (Your line numbers may differ.) This is what a *linter* is for. It isn't looking for crashes. It reads your code as an experienced colleague would, one who has the whole standard library by heart and never tires. Each finding has a code, here `RUF007`, which you can look up in [Ruff's documentation](https://docs.astral.sh/ruff/rules/) for the reasoning.

Take the advice. Add `from itertools import pairwise` to the imports, and change the loop:

<!-- listing: projects/03-dice-lab/main.py -->
```python title="main.py, in longest_streak()"
    for previous, current in pairwise(results):
```

It's easier to read, and it doesn't copy the whole list in order to take one item off the front.

Did that change break anything? Before today you'd have run the program and squinted. Now:

```console
$ uv run pytest
$ uv run ruff check
```

Nine dots, and `All checks passed!`. **That is what tests are for.** They aren't there to prove you were right when you wrote the code. They're there so that you can *change* the code, next week or next year, and find out in a hundredth of a second whether it still works.

The third command in the family is `uv run ruff format`, which formats every file in the project, as your editor does on save.

!!! success "Checkpoint"
    Run `git status` first. You've changed `pyproject.toml` and `uv.lock` as well as your code, and there's a new file. They all belong in the commit: the tests are part of the program now.

    ```console
    $ git add .
    $ git commit -m "Add type hints, a menu, tests and ruff"
    ```

    From here on, the rhythm has two more beats in it: **run, test, lint, diff, commit**.

## Type-in listing

A *Galton board* is a triangle of pegs. You drop a ball in at the top, and at each peg it bounces left or right, at random. Drop two thousand of them and see where they pile up. Save this as `galton.py`, and run it with `uv run galton.py`.

<!-- listing: projects/03-dice-lab/galton.py -->
```python title="galton.py" linenums="1"
import random
from collections import Counter

ROWS = 12
BALLS = 2000
HEIGHT = 16

bins = Counter(sum(random.choice((0, 1)) for _ in range(ROWS)) for _ in range(BALLS))
tallest = max(bins.values())

for level in range(HEIGHT, 0, -1):
    row = ""
    for position in range(ROWS + 1):
        row += " █ " if bins[position] / tallest * HEIGHT >= level else "   "
    print(row)

print("".join(f"{position:^3}" for position in range(ROWS + 1)))
```

1. Line 8 does nearly all the work, and it has a comprehension inside a comprehension, neither with square brackets. (When a comprehension is the only argument to a function, the brackets can be left off. There's a bit more to it than that, and it's in Project 6.) Take it apart from the inside. What does the inner `sum(…)` stand for? What are the keys of `bins`, and what are the values?
2. This histogram stands upright. How? What are the two `for` loops looping over, and why does the outer one count downwards?
3. Why does the pile come out bell-shaped, when every bounce was fifty-fifty? It's the same reason that 7 is the commonest total of two dice.

## Challenges

**Tweak**

1. Add a fourth experiment: three twenty-sided dice, added together. It's one function, and one line in the table.
2. Try a different bar. `▒`, `#` and `■` all have their charms. Then make the bars 70 wide.
3. Under the histogram, print a league table of the five commonest results: `1.  13 came up 675 times`, and so on. You'll want `most_common` and `enumerate`, and they'll go nicely in a function that returns a list of lines.

**Extend**

Write tests for each of these as you go.

1. **Three of a kind.** Roll five dice. How often do at least three of them match? Write `best_group(dice)`, which returns the size of the largest group of matching dice, so that `[6, 2, 6, 2, 6]` gives 3. Then run it 20,000 times and report how often each size of group comes up.
2. **Duel.** Which is better: two six-sided dice, or one twelve-sided? Both have a top score of 12. Make each of them a list of 20,000 results, and write `wins(first, second)` to go through the two lists in step and return how often the first won, how often they drew, and how often the second won.
3. **Turn the histogram on its side.** Write `columns(results, height=15)`, which returns the lines of an upright bar chart, like the Galton board's.

??? tip "Hint for three of a kind"
    A `Counter` of one roll's five dice tells you how many of each number there are. You don't care which number, only how big the biggest group is, and that's the `max` of the `.values()`.

??? tip "Hint for the duel"
    This is the job `zip` was made for, and the lists had better be the same length: `strict=True`. Here's a trick worth knowing: `True` and `False` count as 1 and 0 in arithmetic, so `sum(a > b for a, b in pairs)` counts the pairs in which `a` won.

**Invent**

1. **The Monty Hall problem.** There are three doors, with a car behind one of them and goats behind the others. You pick a door. The host, who knows where the car is, opens one of the *other* doors, to show a goat. Should you stick with your door, or switch to the one that's left? Simulate ten thousand games each way. The answer has started arguments among professional mathematicians.
2. **Pig.** A dice game for two. On your turn you roll one die as often as you like, adding up what you roll. You can stop and bank the total at any time, but if you roll a 1, your turn is over and the total is lost. First to 100 wins. Write it for a human against the computer. Then give the computer a strategy ("hold at 20" is a good start), and use the lab to find out which number it should hold at.
3. **The birthday problem.** How many people do you need in a room before it's more likely than not that two of them share a birthday? Simulate rooms of every size from 2 to 60, a thousand times each, and draw the histogram. The answer is lower than almost anybody guesses.

Solutions to the Tweaks and Extends are in the project's `solutions/` folder.

## Recap

You can now:

- [x] create lists and change them, index them from either end, and apply `len`, `sum`, `min`, `max`, `sorted` and `in`
- [x] say which of `sorted(x)` and `x.sort()` returns a new list, and what the other one returns
- [x] build a dictionary, look things up safely with `.get()`, and loop over its `.items()`
- [x] count anything with a `Counter`, and ask for the `most_common`
- [x] write list and dict comprehensions, with and without a filter, and know when a plain loop is better
- [x] slice a list with a start, a stop and a step, and explain why the convention is the same as `range`'s
- [x] use `enumerate` when you need positions, and `zip` to go through collections in step
- [x] store functions in a dictionary, and call them later
- [x] add type hints, and explain what they do and what they don't
- [x] write pytest tests for predictable code and for random code, and read a failure report
- [x] run `ruff check` and `ruff format`, and look up what a rule code means

**Read more:** [More on lists](https://docs.python.org/3/tutorial/datastructures.html) · [Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) · [`collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) · [Get started with pytest](https://docs.pytest.org/en/stable/getting-started.html) · [The Ruff tutorial](https://docs.astral.sh/ruff/tutorial/) · [Python testing in VS Code](https://code.visualstudio.com/docs/python/testing)

You now have the core of everyday Python: numbers, strings, tuples, lists, dictionaries, functions, loops and comprehensions. Project 4 turns to a question that has been put off three times already. What happens when two names are tied to the same list, and one of them changes it?
