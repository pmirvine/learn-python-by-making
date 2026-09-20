# Project 5 · The Colossal Cupboard

```text
The Cupboard Under the Stairs
Coats press in on every side, and something with too many legs has just
walked over your hand. A crack of light shows a door to the south.

> south
The Hall
A long hall with brown swirly carpet. The kitchen is to the east and the
study to the west. Stairs lead up. The cupboard under the stairs is to
the north.

> west
The study door is locked.

> xyzzy
I don't know how to xyzzy.
```

Before home computers had graphics worth the name, they had *text adventures*: games made entirely of words, in which you typed `GO NORTH` and `TAKE LAMP`, and the computer told you what happened next. The first of them, *Colossal Cave*, was written on a mainframe in 1976. By 1983 every home micro had dozens, and everybody who owned one had tried to write their own, in BASIC, as a great tangle of `IF` statements and `GOTO`s.

Yours is set in a house, in about 1983. Somewhere in it there's a computer, and a cassette to load into it.

It's a bigger program than anything you've written so far: a world of rooms, things to carry, a parser, puzzles and saved games. It won't fit comfortably in one file, and it's the structure that this chapter is about: **modules** to divide the program up, **dataclasses** and **enums** to describe the world, the **`match`** statement to make sense of what the player types, **exceptions** done properly, and **files**. You'll also build the whole of the game's logic as a single function that never prints, never reads the keyboard, and never changes anything. That will seem an odd thing to want. In Project 21 this same game will run in a web browser, and in Project 26 as a full-screen terminal app, without a line of its logic being altered, and then you'll see why.

| | |
|---|---|
| **You'll learn** | Modules and packages; dataclasses; enums; the `match` statement; EAFP, custom exceptions, and `try` with `else` and `finally`; `with`; `pathlib`; JSON |
| **New tool skill** | The packaged project layout. Git branches: `switch`, `merge`, and the graph. |
| **Time** | 5 hours |
| **Before you start** | [Project 4](p04-codebreaker.md) |

## Predict

!!! question "Predict"
    ```python
    from dataclasses import dataclass


    @dataclass
    class Item:
        name: str
        weight: int = 1


    a = Item("torch")
    b = Item("torch", 1)
    print(a)
    print(a == b, a is b)
    ```

??? success "Answer"
    ```text
    Item(name='torch', weight=1)
    True False
    ```

    Four lines have made a new type, with named fields, a default, a readable way of printing itself, and a sensible idea of equality. Two separate objects, with equal values: `==` and `is`, from Project 4. Stage 1.

!!! question "Predict"
    ```python
    def parse(text):
        match text.split():
            case ["go", direction] | [("n" | "s") as direction]:
                return f"going {direction}"
            case ["take", *names]:
                return f"taking {len(names)} things"
            case _:
                return "eh?"


    print(parse("go north"))
    print(parse("s"))
    print(parse("take lamp key"))
    print(parse("go"))
    ```

??? success "Answer"
    ```text
    going north
    going s
    taking 2 things
    eh?
    ```

    `match` compares a value with a series of *patterns*, which describe its shape, and pulls the pieces out as it goes. `["go", direction]` matches a list of exactly two items of which the first is `"go"`, and ties the second to `direction`. `"go"` by itself is a list of one item, which matches nothing but the catch-all. Stage 2.

!!! question "Predict"
    ```python
    exits = {"north": "hall"}
    try:
        room = exits["south"]
        print("moved")
    except KeyError as error:
        print("blocked:", error)
    else:
        print("no problems")
    finally:
        print("done")
    ```

??? success "Answer"
    ```text
    blocked: 'south'
    done
    ```

    The `try` block stops at the line that fails, so `moved` is never printed. `else` runs only if there was *no* exception. `finally` runs whatever happens. Stage 3.

!!! question "Predict"
    ```python
    from enum import Enum


    class Direction(Enum):
        NORTH = "north"
        SOUTH = "south"


    heading = Direction("north")
    print(heading, heading.value, heading is Direction.NORTH)
    print(Direction.NORTH == "north")
    ```

??? success "Answer"
    ```text
    Direction.NORTH north True
    False
    ```

    An *enum* is a fixed set of named values. `Direction("north")` looks up the member with that value, and there's only ever one of each, so `is` works. But a member is not its value: `Direction.NORTH` isn't the string `"north"`, and that's the point of it. Stage 1.

## Build

### Stage 1: A package, and a world

This time, leave off `--no-package`:

```console
$ cd making
$ uv init cupboard
$ cd cupboard
$ uv add --dev pytest ruff
$ code .
```

This is the layout that Project 0 said you'd graduate to. Have a look at what's different.

```text
cupboard/
├── pyproject.toml
├── README.md
└── src/
    └── cupboard/
        └── __init__.py
```

There's no `main.py`. Your code lives in `src/cupboard/`, and that folder is a **package**: a folder of Python files that can be imported by its name. A single `.py` file is a *module*. A package is a folder of modules, and `__init__.py` is what runs when the package itself is imported.

`pyproject.toml` has grown two tables:

```toml
[project.scripts]
cupboard = "cupboard:main"

[build-system]
requires = ["uv_build>=0.12.17,<0.13.0"]
build-backend = "uv_build"
```

`[build-system]` says how to turn this project into something installable. And `[project.scripts]` creates a *command*: it says that typing `cupboard` should call the function `main`, in the package `cupboard`. Try it:

```console
$ uv run cupboard
Hello from cupboard!
```

You didn't name a file. uv has *installed your project* into the project's own virtual environment, as it would install Rich or pytest, and so `cupboard` is a command, and `import cupboard` works from anywhere: from your tests, from the REPL, from any file. It's an *editable* install, meaning that the environment points at your `src` folder and doesn't take a copy, so your changes take effect at once.

Why bother? You saw the problem at the end of Project 4, when you wanted the Dice Lab's `histogram` in another project. A loose file can be imported only by the files next to it. A package can be installed into *any* project, as you'll do in Project 11. It's also how everything on PyPI is built.

!!! warning "Gotcha"
    uv fills in `authors` in `pyproject.toml` from your Git settings, email address and all. That's the right thing for a package you mean to publish. If you'd sooner not have your address in a public repository, delete the line. Nothing depends on it.

#### Modules

The adventure will be four modules, each with one job:

| Module | Its job |
|---|---|
| `world.py` | The rooms and the things in them. Data, which never changes. |
| `engine.py` | The rules: what happens when the player does something. |
| `saves.py` | Writing a game to a file, and reading it back. |
| `__init__.py` | The front end: reading the keyboard, and printing. |

One module uses another by importing it. Inside a package, give the full name, starting from the package:

```python
from cupboard.world import ROOMS, Direction
```

An `import` *runs* the module, the first time, as you saw in Project 4, and ties names to what it defined. After that, Python keeps the module, and importing it again anywhere else costs nothing. The thing to avoid is a circle, in which `engine` imports `saves` and `saves` imports `engine`. Python can sometimes make it work, and you'll wish it hadn't. If you keep your imports pointing one way, from the front end, down through the rules, to the data, you'll never meet the problem. Here, `world` imports nothing of yours, `engine` imports `world`, `saves` imports `engine`, and `__init__` imports the lot.

#### Dataclasses

What's a room? It has a name, a description and some exits, and it may be dark. You could use a dictionary, `{"name": "The Hall", "description": …}`, and in JavaScript you would. But dictionaries have drawbacks for this. Misspell a key and nothing complains until the program runs, and perhaps not then. Your editor can't complete the keys for you. And a type hint of `dict[str, object]` tells a reader nothing at all about what's supposed to be in it.

A *dataclass* is a type of your own, with named and typed fields. Create `src/cupboard/world.py`:

<!-- listing: projects/05-colossal-cupboard/src/cupboard/world.py -->
```python title="src/cupboard/world.py"
"""The world of the Colossal Cupboard: its rooms, and the things in them.

Nothing in this module ever changes while the game is played. Everything that
does change is in engine.State.
"""

from dataclasses import dataclass, field
from enum import Enum


class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    UP = "up"
    DOWN = "down"


# What the player may type for each direction: the full word, or its initial.
DIRECTIONS = {d.value: d for d in Direction} | {d.value[0]: d for d in Direction}


@dataclass
class Room:
    name: str
    description: str
    exits: dict[Direction, str] = field(default_factory=dict)
    dark: bool = False


@dataclass
class Item:
    name: str
    description: str
    portable: bool = True
```

`@dataclass` is a *decorator*: a line beginning with `@` that modifies the definition beneath it. (In Project 16 you'll write decorators of your own, and find out how they work.) This one reads the class's fields, the names with type hints, and writes the dull parts of the class for you. At the REPL, with `uv run python`:

```pycon
>>> from dataclasses import dataclass, field
>>> @dataclass
... class Item:
...     name: str
...     description: str
...     portable: bool = True
...
>>> torch = Item("torch", "A rubber torch.")
>>> torch
Item(name='torch', description='A rubber torch.', portable=True)
>>> torch.name
'torch'
>>> torch == Item("torch", "A rubber torch.")
True
>>> torch.portable = False
>>> Item("anvil")
Traceback (most recent call last):
  ...
TypeError: Item.__init__() missing 1 required positional argument: 'description'
```

You make one by calling the class, as if it were a function, with positional or keyword arguments, and with defaults. You get at the fields with a dot, and Pylance knows what they are, and will complete them, and will underline `torch.nmae`. You get a useful `repr` for debugging, and `==` compares the fields. For the first time, the type hints are doing a job: it's the hints that tell `@dataclass` what the fields are.

This is your first *class*. For now, think of a class as a dictionary with fixed, named slots. Classes can do a great deal more, and Project 9 is where that begins.

!!! warning "Gotcha"
    `exits: dict[Direction, str] = {}` isn't allowed. `@dataclass` refuses it, with `ValueError: mutable default <class 'dict'> for field exits is not allowed`, and you know why: it's Project 4's mutable default, which would give every room the *same* dictionary of exits. `field(default_factory=dict)` says "call `dict()` to make a new one, for each new `Room`".

!!! info "Coming from C, C# or JavaScript"
    A dataclass is a `struct`, or a record, or what you'd use a plain object for in JavaScript. One difference: the fields are mutable unless you say otherwise. `@dataclass(frozen=True)` makes instances that can't be changed, and you'll meet it in Project 10.

#### Enums

A direction is one of six things. You might use the strings `"north"`, `"south"` and so on, but then nothing stops `"nroth"`, or `"North"`, getting into the data, and no tool can find it for you. An `Enum` is a type with a fixed, closed set of members.

```pycon
>>> from enum import Enum
>>> class Direction(Enum):
...     NORTH = "north"
...     SOUTH = "south"
...
>>> Direction.NORTH
<Direction.NORTH: 'north'>
>>> Direction("south")
<Direction.SOUTH: 'south'>
>>> Direction("nroth")
Traceback (most recent call last):
  ...
ValueError: 'nroth' is not a valid Direction
>>> [d.value for d in Direction]
['north', 'south']
```

Misspell `Direction.NROTH` and Pylance underlines it at once. `Direction(text)` turns a value into a member, or raises `ValueError`, which makes it a validator. You can loop over an enum. And its members are hashable, so they can be the keys of a dictionary, which is what `exits` needs.

`DIRECTIONS` is there for the parser: a dictionary from what the player might type to the member it means. It's built from two dictionary comprehensions, one for the whole words and one for their initials, joined with `|`, which merges two dictionaries into a new one.

#### The world itself

Now the data. It's long, but it's only data. Below the classes, in `world.py`:

<!-- listing: projects/05-colossal-cupboard/src/cupboard/world.py -->
```python title="src/cupboard/world.py"
ROOMS = {
    "cupboard": Room(
        "The Cupboard Under the Stairs",
        "Coats press in on every side, and something with too many legs "
        "has just walked over your hand. A crack of light shows a door "
        "to the south.",
        {Direction.SOUTH: "hall"},
    ),
    "hall": Room(
        "The Hall",
        "A long hall with brown swirly carpet. The kitchen is to the east "
        "and the study to the west. Stairs lead up. The cupboard under the "
        "stairs is to the north.",
        {
            Direction.NORTH: "cupboard",
            Direction.EAST: "kitchen",
            Direction.WEST: "study",
            Direction.UP: "landing",
        },
    ),
    "kitchen": Room(
        "The Kitchen",
        "Orange tiles, brown units, and a smell of boiled cabbage that may "
        "never leave. The back door, to the south, leads to the garden.",
        {Direction.WEST: "hall", Direction.SOUTH: "garden"},
    ),
    "garden": Room(
        "The Garden",
        "A small square of lawn, and a shed that leans. A row of flowerpots "
        "stands by the back door, which is to the north.",
        {Direction.NORTH: "kitchen"},
    ),
    "study": Room(
        "The Study",
        "Shelves of computer magazines from floor to ceiling, every one "
        "with a listing you meant to type in. The hall is to the east.",
        {Direction.EAST: "hall"},
    ),
    "landing": Room(
        "The Landing",
        "A narrow landing. A loft ladder has been pulled down, and leads up "
        "into darkness. The stairs go down.",
        {Direction.DOWN: "hall", Direction.UP: "attic"},
    ),
    "attic": Room(
        "The Attic",
        "Under a dust sheet, on an old school desk, sit a beige computer "
        "with red function keys, a portable television and a cassette "
        "recorder. The ladder leads down.",
        {Direction.DOWN: "landing"},
        dark=True,
    ),
}

ITEMS = {
    "torch": Item("torch", "A rubber torch. The batteries are nearly flat."),
    "key": Item("key", "A small rusty key, of the sort that fits a study door."),
    "cassette": Item("cassette", 'A C15 cassette, labelled "ADVENTURE" in biro.'),
    "flowerpots": Item(
        "flowerpots",
        "Terracotta, and empty. One has been moved lately.",
        portable=False,
    ),
    "magazines": Item(
        "magazines", "Hundreds of them. Far too many to carry.", portable=False
    ),
}

START = "cupboard"
PLAYER = "player"

# Where everything is when the game begins: a room, another thing, or PLAYER.
START_PLACES = {
    "torch": "kitchen",
    "key": "flowerpots",
    "flowerpots": "garden",
    "cassette": "study",
    "magazines": "study",
}
```

Write your own descriptions if you like. It's your house. Rooms are known to each other by short keys, `"hall"` and `"kitchen"`, and the long descriptions use the adjacent-strings trick from Project 0. Note where the key is: *in* the flowerpots. A thing's place can be a room, or another thing, or the player.

To walk about in it, replace `src/cupboard/__init__.py`:

<!-- listing: projects/05-colossal-cupboard/stages/stage1_init.py -->
```python title="src/cupboard/__init__.py"
"""The Colossal Cupboard: a small text adventure."""

from cupboard.world import DIRECTIONS, ROOMS, START


def main() -> None:
    location = START
    while True:
        room = ROOMS[location]
        print(f"\n{room.name}\n{room.description}")

        word = input("\n> ").strip().lower()
        if word in ("quit", "q"):
            break
        try:
            location = room.exits[DIRECTIONS[word]]
        except KeyError:
            print("You can't go that way.")
```

!!! example "Run it"
    ```console
    $ uv run cupboard
    ```

    Explore the house with `n`, `s`, `e`, `w`, `u` and `d`. Every door is open, for now, and there's nothing to pick up. `q` quits.

There's no `if __name__ == "__main__":` at the bottom, and none is needed. Nobody runs this file. They run the `cupboard` command, which imports the package and calls `main`.

Look at the `try`. Two things can go wrong in its one line: the word might not be a direction, and the room might have no exit that way. Both of them are a `KeyError`, and both deserve the same reply. There's no checking beforehand, of the `if word in DIRECTIONS and DIRECTIONS[word] in room.exits` kind. The code goes ahead, and deals with failure if it comes. That's EAFP, from Project 1, and there's more to say about it in the next stage.

!!! success "Checkpoint"
    ```console
    $ git add .
    $ git commit -m "Build the house, and walk about in it"
    ```

### Stage 2: The engine

Now for the design decision that the rest of this chapter hangs on, and two later chapters with it.

Everything that *changes* during a game is going to live in one small object, the `State`: where the player is, where each thing is, whether the study is unlocked, how many moves have been made. And the whole of the game's logic will be one function:

```python
def respond(state: State, text: str) -> tuple[State, str]:
```

Give it the state of the game and what the player typed. It gives you back the **new** state, and what to say to the player. And that's *all* it does. It doesn't print. It doesn't call `input`. It doesn't read or write files. And, following Project 4's rule to the letter, it doesn't change the state it was given. It builds a new one.

What that buys you:

- **It's easy to test.** A test is a list of commands and an `assert`. No keyboard to fake, and no output to capture.
- **Any front end can drive it.** This chapter's reads the keyboard. Project 21's is a web page, and Project 26's is a full-screen terminal app. `respond` will never know the difference.
- **Saving is simple.** The state is one small object, so saving the game means saving that.
- **Old states stay valid.** Since nothing ever changes a `State`, you can keep the previous ones, and that makes `undo` nearly free. It's one of the challenges.

Create `src/cupboard/engine.py`. First, the state, and the functions that ask questions of it:

<!-- listing: projects/05-colossal-cupboard/src/cupboard/engine.py -->
```python title="src/cupboard/engine.py"
"""The rules of the game.

The one function that matters is respond(). It takes the state of the game and
what the player typed, and returns the new state and what to tell the player.
It never prints, never asks for input and never changes the state it's given,
so any front end can drive it: a terminal, a web page or a test.
"""

from dataclasses import dataclass, field, replace

from cupboard.world import (
    DIRECTIONS,
    ITEMS,
    PLAYER,
    ROOMS,
    START,
    START_PLACES,
    Direction,
)

FILLER = {"the", "a", "an", "to", "at", "in", "into", "with", "please"}

HELP = (
    "Try: look, go north (or just n, s, e, w, u, d), take, drop, examine, "
    "inventory (or i), unlock, load, save, restore and quit."
)


@dataclass
class State:
    """Everything that can change during a game."""

    location: str = START
    places: dict[str, str] = field(default_factory=START_PLACES.copy)
    unlocked: bool = False
    moves: int = 0
    won: bool = False


def is_dark(state: State) -> bool:
    """Is the player somewhere dark, without the torch?"""
    return ROOMS[state.location].dark and state.places["torch"] != PLAYER


def things_at(state: State, place: str) -> list[str]:
    """Return the names of the things in a room, or carried by the PLAYER."""
    return [name for name, where in state.places.items() if where == place]


def describe(state: State) -> str:
    """Describe the room the player is in, and what can be seen there."""
    if is_dark(state):
        return "It's pitch dark. You can hear breathing, and hope that it's yours."
    room = ROOMS[state.location]
    lines = [room.name, room.description]
    things = [name for name in things_at(state, state.location) if ITEMS[name].portable]
    if things:
        lines.append(f"You can see: {', '.join(things)}.")
    return "\n".join(lines)
```

Every field of `State` has a default, so `State()` is a new game. `places` is the heart of it: a dictionary from each thing to where it is. There's no inventory list, and no list of contents for each room, to be kept in step with one another. There is *one* fact about each thing, its place, and everything else is worked out from that, as the board was in Codebreaker. What's the player carrying? The things whose place is `PLAYER`.

`default_factory=START_PLACES.copy` is worth a second look. There are no brackets after `copy`, so it isn't a call: it hands over the dictionary's `copy` method itself, to be called each time a `State` is made. Every game starts with its own copy of the starting places, and the constant itself is never touched.

#### The actions, and two ways of not falling over

<!-- listing: projects/05-colossal-cupboard/src/cupboard/engine.py -->
```python title="src/cupboard/engine.py"
def go(state: State, direction: Direction) -> tuple[State, str]:
    try:
        destination = ROOMS[state.location].exits[direction]
    except KeyError:
        return state, "You can't go that way."
    if destination == "study" and not state.unlocked:
        return state, "The study door is locked."
    moved = replace(state, location=destination)
    return moved, describe(moved)


def take(state: State, name: str) -> tuple[State, str]:
    if is_dark(state):
        return state, "You grope about in the dark, and find nothing."
    if state.places.get(name) != state.location:
        return state, f"I can't see any {name} here."
    if not ITEMS[name].portable:
        return state, f"You can't carry the {name}."
    return replace(state, places=state.places | {name: PLAYER}), "Taken."


def drop(state: State, name: str) -> tuple[State, str]:
    if state.places.get(name) != PLAYER:
        return state, f"You aren't carrying any {name}."
    return replace(state, places=state.places | {name: state.location}), "Dropped."
```

Every action has the same shape. It takes a state, and returns a state and a reply. When it fails, it returns **the same state**, untouched, with an explanation. When it succeeds, it builds a new state with `dataclasses.replace`, which copies a dataclass instance, changing only the fields you name.

`state.places | {name: PLAYER}` is the `|` again. It makes a *new* dictionary, with one entry changed, and leaves the old one as it was. Had `take` said `state.places[name] = PLAYER`, it would have altered a dictionary that the *old* state is also tied to, which is Project 4's aliasing bug. There's a test coming up that would catch it.

Look at how `go` and `take` guard against failure, because they do it in opposite ways. `go` **tries the lookup and catches the `KeyError`**. `take` **checks first**, using `.get()`, which returns `None` for a name it has never heard of. Python people have names for the two styles. *EAFP* is "easier to ask forgiveness than permission", and *LBYL* is "look before you leap". Project 1 promised you the argument for EAFP, and here it is.

- **There's no gap between the check and the act.** Look before you leap, and the world may change between the looking and the leaping. For a dictionary inside your own function, it can't. For a file, it can: `if path.exists(): open(path)` has a window in which some other program deletes the file. `try: open(path)` has no window. The operation is its own check.
- **You can't get the check wrong.** To look before you leap, you have to know every way the leap can fail, and test for each of them. Project 1's example was `int()`, which accepts far more than you would think to check for. Let the operation be the judge of what's acceptable.
- **The usual case reads straight through.** The line that does the work isn't buried under conditions.

So why isn't `take` written that way? Because it isn't asking "is this key there?" but "is this thing *here*?", and `.get()` answers that in one comparison, a missing key and a thing in the wrong room alike. EAFP is Python's default, and not its law. Use whichever is clearer. What matters more is the rule that comes with `try`:

!!! warning "Gotcha"
    **Keep the `try` block as small as you can**: ideally, just the one line that you expect to fail. Everything inside a `try` is covered by its `except`, including the mistakes you haven't made yet. Put ten lines in, and a `KeyError` from a typing mistake on line 7 will be "handled", silently, as if it were the player's fault. This chapter's bug hunt is about exactly that.

There are four more actions. They bring nothing new, so type them in, and notice that each is a list of reasons to refuse, followed by one line that does the deed.

<!-- listing: projects/05-colossal-cupboard/src/cupboard/engine.py -->
```python title="src/cupboard/engine.py"
def examine(state: State, name: str) -> tuple[State, str]:
    if is_dark(state):
        return state, "It's too dark to see anything."
    if state.places.get(name) not in (state.location, PLAYER):
        return state, f"I can't see any {name} here."
    if name == "flowerpots" and state.places["key"] == "flowerpots":
        found = replace(state, places=state.places | {"key": state.location})
        return found, "Under the one that's been moved, you find a small rusty key."
    return state, ITEMS[name].description


def inventory(state: State) -> tuple[State, str]:
    carrying = things_at(state, PLAYER)
    if not carrying:
        return state, "You're empty-handed."
    return state, f"You're carrying: {', '.join(carrying)}."


def unlock(state: State) -> tuple[State, str]:
    if state.location != "hall":
        return state, "There's nothing here to unlock."
    if state.unlocked:
        return state, "It's already unlocked."
    if state.places["key"] != PLAYER:
        return state, "You have nothing to unlock it with."
    opened = replace(state, unlocked=True)
    return opened, "The key turns, with a squeal. The study is open."


def load_cassette(state: State) -> tuple[State, str]:
    if state.places["cassette"] != PLAYER:
        return state, "You have nothing to load."
    if state.location != "attic" or is_dark(state):
        return state, "There's nothing here to load it into."
    ending = (
        "You put the cassette in the recorder and press PLAY. The computer "
        "beeps twice. Four minutes of warbling later, the screen clears.\n"
        "\n"
        "    THE COLOSSAL CUPBOARD\n"
        "    Coats press in on every side...\n"
        "\n"
        f"You have won, in {state.moves + 1} moves."
    )
    return replace(state, won=True), ending
```

#### `match`: understanding the player

The player types `take the torch`, or `get torch`, or `pick up the torch please`. All of those mean one thing. In BASIC, this was where adventures went to die, under a heap of `IF LEFT$(A$,4)="TAKE" THEN…`. Python has a statement that might have been made for the job.

<!-- listing: projects/05-colossal-cupboard/src/cupboard/engine.py -->
```python title="src/cupboard/engine.py"
def respond(state: State, text: str) -> tuple[State, str]:
    """Work out what the player meant, and return the new state and a reply."""
    words = [word for word in text.lower().split() if word not in FILLER]

    match words:
        case []:
            return state, "Pardon?"
        case ["help"]:
            return state, HELP
        case ["look" | "l"]:
            new, reply = state, describe(state)
        case ["inventory" | "i"]:
            new, reply = inventory(state)
        case ["go", word] | [word] if word in DIRECTIONS:
            new, reply = go(state, DIRECTIONS[word])
        case ["take" | "get", name] | ["pick", "up", name]:
            new, reply = take(state, name)
        case ["drop", name]:
            new, reply = drop(state, name)
        case ["examine" | "x", name] | ["look", name]:
            new, reply = examine(state, name)
        case ["unlock", *_]:
            new, reply = unlock(state)
        case ["load" | "play" | "use", "cassette"]:
            new, reply = load_cassette(state)
        case [verb, *_]:
            return state, f"I don't know how to {verb}."

    return replace(new, moves=state.moves + 1), reply
```

The first line splits the text into words, in lower case, and throws the filler away, so that `take the torch please` becomes `["take", "torch"]`. Then `match` compares that list with each `case` in turn, from the top, and runs the first that fits. But a `case` isn't a value to be compared. It's a **pattern**: a description of a shape, with holes in it.

| Pattern | Matches | And ties |
|---|---|---|
| `[]` | an empty list | |
| `["help"]` | a list of exactly one item, the string `"help"` | |
| `["look" \| "l"]` | one item, which is `"look"` or `"l"` | |
| `["drop", name]` | two items, of which the first is `"drop"` | `name` to the second |
| `["take" \| "get", name] \| ["pick", "up", name]` | either shape | `name`, whichever it was |
| `["unlock", *_]` | `"unlock"`, and then anything, or nothing | |
| `[verb, *_]` | any list of one item or more | `verb` to the first |

A plain name in a pattern is a hole. It matches anything, and is tied to what it matched. A literal, such as `"drop"`, has to be equal. `|` means *or*. `*_` soaks up the rest, as `*rest` did when you unpacked tuples in Project 2, and `_` means "and I don't care what it was".

The direction case has an `if` on the end, which is called a *guard*. `["go", word] | [word]` would match any two words beginning with `go`, or any single word whatever, `xyzzy` included. The guard makes it match only if `word` really is a direction, and if it isn't, `match` moves on to the next case.

**The order matters**, because the first match wins. `["look" | "l"]`, which is one word, comes before `["look", name]`, which is two. The catch-all, `[verb, *_]`, must come last, since it matches everything that's left.

The commands that don't count as a move, which are nonsense and cries for help, return straight away. All the rest fall through to the last line, which adds one to `moves`.

!!! warning "Gotcha"
    `match` isn't `switch`. In particular, this doesn't do what it appears to:

    ```python
    NORTH = "n"

    match word:
        case NORTH:     # not a comparison with "n"!
            ...
    ```

    A plain name in a pattern is always a hole. `case NORTH:` matches *anything*, and ties it to a new variable called `NORTH`. To match against a constant, the pattern must have a dot in it, as `case Direction.NORTH:` has, or be a literal. It's the most common `match` mistake there is. Python refuses to run it if there's a case underneath, which can never be reached, but says nothing if it's the last.

!!! info "Coming from C, Java or JavaScript"
    There's no fall-through, and so no `break`. But it goes well beyond `switch`. `match` takes data apart. It can match tuples, dictionaries and dataclass instances by their shape, and pull out their fields, and in Project 17 it will be the engine of your BASIC interpreter.

Now the front end shrinks to nearly nothing. Replace `src/cupboard/__init__.py`:

<!-- listing: projects/05-colossal-cupboard/stages/stage2_init.py -->
```python title="src/cupboard/__init__.py"
"""The Colossal Cupboard: a small text adventure."""

import textwrap

from cupboard.engine import State, describe, respond


def show(text: str) -> None:
    """Print a reply, wrapping long lines but keeping indented ones as they are."""
    for line in text.splitlines():
        print(line if line.startswith(" ") else textwrap.fill(line, width=72))


def main() -> None:
    state = State()
    show(describe(state))

    while not state.won:
        text = input("\n> ")
        if text.strip().lower() in ("quit", "q"):
            break
        state, reply = respond(state, text)
        show(reply)

    show("Bye.")
```

`state, reply = respond(state, text)` is the whole game: the old state goes in, and the new one comes out and takes its name. `textwrap.fill`, from the standard library, wraps a paragraph to a given width.

!!! example "Run it"
    ```console
    $ uv run cupboard
    ```

    Can you finish it? You're looking for a cassette, and for something to play it on. If you get stuck: examine things.

#### Testing a game

This is where the design pays its first dividend. Create `tests/test_engine.py`. Your tests live in a folder of their own from now on, and because the package is installed, they can import it from there.

<!-- listing: projects/05-colossal-cupboard/tests/test_engine.py -->
```python title="tests/test_engine.py"
from cupboard.engine import State, describe, respond
from cupboard.world import ITEMS, PLAYER, ROOMS, START_PLACES

WALKTHROUGH = [
    "south",
    "e",
    "take the torch",
    "go south",
    "examine flowerpots",
    "take key",
    "n",
    "w",
    "unlock door with key",
    "w",
    "get cassette",
    "e",
    "up",
    "up",
    "load cassette",
]


def play(commands: list[str], state: State | None = None) -> tuple[State, str]:
    """Feed a list of commands to the game. Return the final state and last reply."""
    state = state or State()
    reply = ""
    for command in commands:
        state, reply = respond(state, command)
    return state, reply


def test_the_game_can_be_won():
    state, reply = play(WALKTHROUGH)
    assert state.won
    assert "You have won, in 15 moves." in reply
```

(That's the solution, so look away if you're still playing.) A whole game, from the cupboard to the closing credits, runs as one test in well under a millisecond. Whatever you do to this program from now on, you'll know at once whether it can still be won. Then test the rules, one at a time:

<!-- listing: projects/05-colossal-cupboard/tests/test_engine.py -->
```python title="tests/test_engine.py"
def test_the_study_is_locked_until_the_key_is_used():
    state, reply = play(["s", "w"])
    assert reply == "The study door is locked."
    assert state.location == "hall"

    state, reply = play(["unlock door"], state)
    assert reply == "You have nothing to unlock it with."
# ...
def test_the_attic_is_dark_without_the_torch():
    state, reply = play(["s", "u", "u"])
    assert state.location == "attic"
    assert "pitch dark" in reply
# ...
def test_respond_never_changes_the_state_it_is_given():
    before = State()
    after, _ = play(["s", "e", "take torch"], before)
    assert before == State()
    assert after != before
    assert before.places is not after.places


def test_every_thing_has_a_description_and_every_exit_leads_somewhere():
    assert set(START_PLACES) == set(ITEMS)
    for room in ROOMS.values():
        for destination in room.exits.values():
            assert destination in ROOMS
```

Look at the last two. The first of them keeps Project 4's promise, by checking that playing a game does nothing to the state it started from. Try breaking it: change `take` to say `state.places[name] = PLAYER` before its `return`, and watch that test fail. The second doesn't test the code at all. It tests the **data**: every thing that has a place also has a description, and no exit leads into the void. Write a test like that for any program with a table of data in it. It finds the typing mistakes before a player does.

Write some more of your own, for taking and dropping, and for the flowerpots. The project in the tutorial's repository has thirteen.

!!! success "Checkpoint"
    Run, test, lint, diff, commit.

    ```console
    $ git add .
    $ git commit -m "Add the game engine, with a parser built on match"
    ```

### Stage 3: Saved games, on a branch

A game that can't be saved isn't much of an adventure. This is a new feature, which will take several commits to get right, and while you're halfway through it the program may not work. So far every commit you've made has gone onto one line of history, called `main`. It's time to learn the Git feature that everything else is built on.

#### Branches

A *branch* is a separate line of development. You start one, work on it, commit to it as often as you please, and `main` stays exactly as it was: working, and ready to return to at any moment. When the feature is finished, you *merge* the branch back into `main`.

```console
$ git switch -c saves
Switched to a new branch 'saves'
```

`-c` is for *create*. `git status` now begins `On branch saves`, and VS Code shows the branch's name at the left of the status bar. Nothing else has changed, yet. A branch is nothing more than a label on a commit, which moves forward as you add commits to it, and that's why branches in Git cost nothing, and why people make them for even the smallest pieces of work.

#### Files, with `pathlib` and `with`

Create `src/cupboard/saves.py`:

<!-- listing: projects/05-colossal-cupboard/src/cupboard/saves.py -->
```python title="src/cupboard/saves.py"
"""Saving a game to a file, and getting it back."""

import json
from dataclasses import asdict
from pathlib import Path

from cupboard.engine import State


class SaveError(Exception):
    """A saved game couldn't be written, or couldn't be read."""


def save(state: State, path: Path) -> None:
    """Write the state of the game to a file, as JSON."""
    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(asdict(state), file, indent=2)
    except OSError as error:
        raise SaveError(f"I couldn't save the game: {error}") from error


def load(path: Path) -> State:
    """Read the state of a game back from a file."""
    try:
        with path.open(encoding="utf-8") as file:
            return State(**json.load(file))
    except FileNotFoundError:
        raise SaveError("There's no saved game to restore.") from None
    except (OSError, ValueError, TypeError) as error:
        raise SaveError(f"I couldn't read the saved game: {error}") from error
```

That's twenty lines, with five new ideas in them.

**`Path`.** A file's location isn't text, and shouldn't be treated as if it were. A `pathlib.Path` knows about folders and filenames, and about the differences between Windows and everything else. You join paths with `/`:

```pycon
>>> from pathlib import Path
>>> save_file = Path("games") / "cupboard-save.json"
>>> save_file.name, save_file.suffix, save_file.parent.name
('cupboard-save.json', '.json', 'games')
>>> save_file.exists()
False
```

A `Path` can also read and write the file it names, with `.read_text()` and `.write_text()`, list a folder's contents, and a good deal more. You'll see it called `os.path` in older code. `pathlib` is its replacement.

**`with`.** A file that's been opened must be closed again, whatever happens, including when the code between the opening and the closing raises an exception. `with` guarantees it:

```python
with path.open("w", encoding="utf-8") as file:
    json.dump(asdict(state), file, indent=2)
# By here the file has been closed, however we left the block.
```

`path.open(…)` gives back a file object, and `as file` ties a name to it. When the block ends, whether by reaching the bottom, by a `return` or by an exception, the file is closed. The general idea is called a *context manager*. It turns up wherever something has to be released afterwards: files, locks, network connections, database transactions. In Project 18 you'll write one. **Always open files with `with`.**

`"w"` opens the file for writing, replacing anything already in it. The default, `"r"`, is for reading. Always give the `encoding` as well. You met UTF-8 in Project 4, and it's the right answer. Before Python 3.15, what you got if you left it out depended on the computer, and that's how files come to be full of `Ã©`.

**JSON.** JSON is a text format for data, which came from JavaScript, and is what nearly everything on the web speaks. It has objects, arrays, strings, numbers, `true`, `false` and `null`, which correspond closely to Python's dictionaries, lists, strings, numbers, `True`, `False` and `None`. `json.dump(data, file)` writes, and `json.load(file)` reads. (`dumps` and `loads`, with an `s`, do the same with strings, not files.)

JSON knows nothing of dataclasses, so `dataclasses.asdict(state)` turns the state into a plain dictionary first. Coming back, `json.load` gives you a dictionary, and:

```python
State(**json.load(file))
```

The `**` spreads a dictionary out into keyword arguments, so that `State(**{"location": "hall", "moves": 3})` means `State(location="hall", moves=3)`. It's the single-star unpacking of Project 2, for dictionaries. Project 7 has the whole story.

Here's what a saved game looks like. It's text, and you can read it, which is a good part of JSON's appeal:

```json
{
  "location": "kitchen",
  "places": {
    "torch": "player",
    "key": "flowerpots",
    "flowerpots": "garden",
    "cassette": "study",
    "magazines": "study"
  },
  "unlocked": false,
  "moves": 3,
  "won": false
}
```

**Your own exceptions.** A great deal can go wrong with a file. It may not be there, or the disk may be full. You may not be allowed to read it. It may be there, and readable, and contain somebody's shopping list. The front end doesn't want to know about all that. It wants to know one thing: *did it work, and if not, what shall I tell the player?* So `saves.py` defines an exception of its own:

```python
class SaveError(Exception):
    """A saved game couldn't be written, or couldn't be read."""
```

That's a complete definition. It says that `SaveError` is a kind of `Exception`, and the docstring is the whole of its body. `save` and `load` catch the many low-level exceptions and raise this one in their place, with a message fit for a player to read. A module that turns the assorted failures of the things it uses into one exception of its own is a module that's easy to use.

Exceptions come in families. `FileNotFoundError` and `PermissionError` are both kinds of `OSError`, and `except OSError` catches either. A tuple of types, as in `except (OSError, ValueError, TypeError)`, catches any of those. When JSON can't be parsed, it raises a kind of `ValueError`. And `State(**data)` raises `TypeError` if the dictionary has keys that `State` has never heard of. The `except` clauses are tried from the top, so the particular case, `FileNotFoundError`, comes before the general one.

**`raise … from`.** When you raise one exception while handling another, say where it came from. `from error` attaches the original to the new one, as its *cause*, so that a traceback shows both, and whoever is debugging can see the real reason. `from None` says the opposite: the original is of no interest. "There's no saved game" is the entire story, and nobody needs to see a `FileNotFoundError` as well. Ruff insists that you choose one or the other (rule `B904`), and it's right to.

!!! note "Under the bonnet"
    The third Predict showed the full form of `try`, which has four parts.

    ```python
    try:
        risky()
    except SomeError:
        ...    # runs if risky() raised SomeError
    else:
        ...    # runs if nothing was raised
    finally:
        ...    # runs whatever happened, even after a return
    ```

    `else` is for code that should run only after success, and that you don't want *inside* the `try`, in keeping with the rule about small `try` blocks. `finally` is for clearing up. It's what `with` uses, underneath, to make its guarantee.

#### Wiring it in

The front end gets two commands, `save` and `restore`. They aren't part of the game's rules, and they need files, so they belong here, and not in `respond`. `main` has three kinds of command to tell apart now, and it's `match` again, on a plain string this time:

<!-- listing: projects/05-colossal-cupboard/src/cupboard/__init__.py -->
```python title="src/cupboard/__init__.py"
"""The Colossal Cupboard: a small text adventure."""

import textwrap
from pathlib import Path

from cupboard.engine import State, describe, respond
from cupboard.saves import SaveError, load, save

SAVE_FILE = Path("cupboard-save.json")
# ...
def main() -> None:
    state = State()
    show(describe(state))

    while not state.won:
        text = input("\n> ")
        match text.strip().lower():
            case "quit" | "q":
                break
            case "save":
                try:
                    save(state, SAVE_FILE)
                    show("Saved.")
                except SaveError as error:
                    show(str(error))
            case "restore":
                try:
                    state = load(SAVE_FILE)
                    show("Restored.\n" + describe(state))
                except SaveError as error:
                    show(str(error))
            case _:
                state, reply = respond(state, text)
                show(reply)

    show("Bye.")
```

Restoring a game is one assignment: `state = load(SAVE_FILE)`. That's what comes of keeping everything that changes in one object.

!!! example "Run it"
    Play for a bit, `save`, do something you regret, and `restore`. Then quit, start again, and `restore`. Have a look at `cupboard-save.json`, too. It's in your project folder, and it doesn't belong in Git, so add a line saying `cupboard-save.json` to `.gitignore`.

#### Testing with real files

Tests mustn't leave files lying about, and mustn't depend on files that happen to be there already. pytest has a *fixture* for this. A fixture is something that a test asks for, simply by naming it as a parameter. `tmp_path` is a `Path` to a new, empty folder, made for that one test and cleared away afterwards. Create `tests/test_saves.py`:

<!-- listing: projects/05-colossal-cupboard/tests/test_saves.py -->
```python title="tests/test_saves.py"
import pytest

from cupboard.engine import State, respond
from cupboard.saves import SaveError, load, save


def test_a_saved_game_comes_back_the_same(tmp_path):
    state = State()
    for command in ["s", "e", "take torch"]:
        state, _ = respond(state, command)

    save(state, tmp_path / "game.json")

    assert load(tmp_path / "game.json") == state
# ...
def test_restoring_when_nothing_was_saved(tmp_path):
    with pytest.raises(SaveError, match="no saved game"):
        load(tmp_path / "nothing.json")


def test_restoring_from_a_file_of_rubbish(tmp_path):
    rubbish = tmp_path / "game.json"
    rubbish.write_text("this is not JSON", encoding="utf-8")
    with pytest.raises(SaveError, match="couldn't read"):
        load(rubbish)
```

The first of those is a *round trip*: save, load, and compare. It's one line long because dataclasses come with `==`. The others use `pytest.raises`, which is a context manager, and so another use of `with`. The test passes if the block raises that exception, with a message that matches, and fails if it doesn't. Test your failures as carefully as your successes. They're the code you'll run least often, and so the code most likely to be wrong.

#### Merging

When the tests pass, commit on the branch, and then bring the work home:

```console
$ git add .
$ git commit -m "Add save and restore"
$ git switch main
Switched to branch 'main'
```

Look at your editor. `saves.py` has *gone*, and `__init__.py` is back as it was. Nothing is lost. You're looking at `main`, where the feature hasn't happened yet. `git switch saves` would bring it all back. Now merge:

```console
$ git merge saves
Updating 5d0c8e1..a3b9f27
Fast-forward
 .gitignore               |  3 +++
 src/cupboard/__init__.py | 22 ++++++++++++++++----
 src/cupboard/saves.py    | 32 ++++++++++++++++++++++++++++++++
 tests/test_saves.py      | 46 ++++++++++++++++++++++++++++++++++++++++++++++
 4 files changed, 99 insertions(+), 4 deletions(-)
$ git branch -d saves
Deleted branch saves (was a3b9f27).
```

*Fast-forward* means that `main` hadn't moved on while you were away, so that all Git had to do was slide the `main` label along to where `saves` was pointing. `git branch -d` then deletes the `saves` label. The commits stay, as part of `main`. To see the shape of your history:

```console
$ git log --oneline --graph
```

VS Code draws the same graph at the bottom of its Source Control panel. For now it's a straight line. In Project 12, two branches will change the same file, and things will become more interesting.

From here on, begin every new feature, and every challenge, with `git switch -c something`. If it all goes wrong, `git switch main` takes you back to a program that works, and you can delete the branch with `git branch -D`, and pretend that it never happened.

!!! success "Checkpoint"
    `git status` should say `On branch main` and `nothing to commit`, and `git branch` should list `main` alone.

## Type-in listing

*Langton's ant* lives on an endless grid of white squares. On a white square, it turns right. On a black square, it turns left. In either case it flips the colour of the square, and steps forward. That's all. Save this as `ant.py` in the project folder, and run it with `uv run ant.py`.

<!-- listing: projects/05-colossal-cupboard/ant.py -->
```python title="ant.py" linenums="1"
STEPS = 11_000

black = set()
x, y = 0, 0
dx, dy = 0, -1

for _ in range(STEPS):
    if (x, y) in black:
        black.remove((x, y))
        dx, dy = dy, -dx
    else:
        black.add((x, y))
        dx, dy = -dy, dx
    x, y = x + dx, y + dy

columns = [x for x, _ in black]
rows = [y for _, y in black]
for row in range(min(rows), max(rows) + 1):
    line = ""
    for column in range(min(columns), max(columns) + 1):
        line += "█" if (column, row) in black else " "
    print(line)
```

1. For about ten thousand steps the ant makes a mess. What does it do after that? Try `STEPS = 12_000`, and then `15_000`. Nobody has ever proved *why* it does it.
2. The grid has no edges, and yet the program never says how big it is. How is a grid being stored here, and what would go wrong with a list of lists?
3. `dx, dy = dy, -dx` turns the ant left. Work through it on paper, starting with the ant facing up, `(0, -1)`, remembering that `y` increases *down* the screen. Could you write it without tuple assignment?
4. Why is `(x, y)` allowed in a set, where `[x, y]` wouldn't be?

A set of tuples, standing for a grid with no edges: keep hold of that idea. Project 6 is built on it.

## Bug hunt

A colleague has written a new room for the adventure, the pantry, and tried it out by itself first. It's in the project's `bughunt/` folder, as `pantry.py`. Copy it into a `bughunt` folder of your own, and run it:

```console
$ uv run bughunt/pantry.py

The Pantry. You can see: marmalade, jam, teapot.
> take jam
I can't see any jam here.
```

It's there in the description, as plain as anything. The marmalade can be taken, and so can the teapot. The jam can't. Your colleague has been staring at `take` for an hour.

1. **Reproduce it**, and then try some other things. Can you take the teapot and then the marmalade? What *should* happen?
2. **Write a failing test**, in `bughunt/test_pantry.py`, that takes each of the three things in turn. Run it with `uv run pytest bughunt`.
3. **Find the cause.** The message is a lie. What's *really* going wrong? You might temporarily remove the `try`, and see what Python has to say.
4. **Fix it**, and fix the thing that hid it, too. They're two separate repairs. Then write the test that would have caught this before the pantry was ever run.

??? tip "Hint"
    How many lines of `take` can raise a `KeyError`? How many of those did the author have in mind when they wrote `except KeyError`?

??? success "Solution"
    Take out the `try`, and Python tells you at once: `KeyError: 'jam'`, from the line `item = ITEMS[name]`. There's no `"jam"` in `ITEMS`. It was typed in as `"jelly"`, while `START_PLACES` says `"jam"`. A slip in the data.

    But the slip is only half of the bug. The other half is **a `try` block that covers too much**. The author wrote `except KeyError` thinking of one line, `places[name]`, and one meaning: *the player named something that doesn't exist*. But five lines were under its protection. When a different line raised `KeyError`, for a different reason, the handler took a mistake in the *program* for a mistake by the *player*, and said something untrue with complete confidence. The third part of your test shows another symptom of the same thing: the message for a load that's too heavy comes out wrong for the jam as well.

    Two repairs. Correct the data. And shrink the `try`, to the one line that's expected to fail:

    ```python
    try:
        where = places[name]
    except KeyError:
        return places, f"I can't see any {name} here."

    if where != location:
        return places, f"I can't see any {name} here."
    item = ITEMS[name]
    ...
    ```

    Now a missing `ITEMS` entry crashes, with a traceback pointing at the very line, and you'd have found it in ten seconds. **A crash is a gift.** An error that's been handled wrongly is a mystery.

    And the test that would have prevented it all is the data test, from Stage 2:

    ```python
    def test_every_thing_that_has_a_place_has_a_description():
        assert set(START_PLACES) == set(ITEMS)
    ```

## Challenges

Make a branch for each.

**Tweak**

1. Teach the parser some more words: `grab` for take, `inv` for inventory, and `walk north` and `run north` for go.
2. Make `describe` list the ways out, as a last line: `Exits: north, east, west, up.` You can loop over a room's `exits`, and each `Direction` has a `.value`.
3. Add a room to the house, with something in it. A bathroom, off the landing, is traditional. The data test will tell you if you've forgotten anything.

**Extend**

1. **Undo.** Add an `undo` command to the front end, to take back the last move. Because `respond` never changes a state, this is far easier than it sounds. Keep a list. What should `undo` do when there's nothing to undo? And should a command that changed nothing be recorded?
2. **Score.** Five points for each room visited, and fifty for winning, with a `score` command to report it. `State` needs a new field to remember the rooms visited. A set is the natural thing, and then saving breaks, because JSON has no sets. What will you do about that?
3. **A world in a file.** Move the rooms and the things out of `world.py`, into a `world.json` beside it, and build `ROOMS` from that when the module is imported. `Room(**data)` does most of the work, but `exits` will need converting: JSON's keys are always strings, and yours are `Direction`s. `Path(__file__).parent` is the folder that the present module lives in.

??? tip "Hint for undo"
    In `main`, keep `history: list[State] = []`. Before replacing `state` with a new one, append the old one. `undo` is then `state = history.pop()`. To leave out the commands that did nothing, compare the new state with the old. Dataclasses have `==`.

**Invent**

1. **Your own adventure.** A different house, a spaceship, your old school. The engine has four puzzle mechanisms in it: a locked door, a dark room, a hidden thing, and a thing to be used in a particular place. How far can you get with those before you have to touch `engine.py`? And then, how could the *data* describe a puzzle, so that you never had to?
2. **Somebody else in the house.** A cat, which moves from room to room by itself, one room for each move you make, and which can be picked up, briefly. Where does its movement belong: in `respond`, or in the front end?
3. **A transcript.** `cupboard --transcript game.txt` records everything that's typed and everything that's shown. You'll need `sys.argv`, which is a list of the words on the command line, and a file that stays open for the whole game. Think about where the `with` goes.

Solutions to the Tweaks and the first two Extends are in the project's `solutions/` folder.

## Recap

You can now:

- [x] lay a project out as a package, split it into modules, and say which way the imports should run
- [x] explain what an editable install is, and how `[project.scripts]` makes a command
- [x] define a dataclass, with defaults and `field(default_factory=…)`, and copy one with `replace`
- [x] use an `Enum` for a closed set of values, and convert to it from text
- [x] write `match` statements with literal, capture, `|`, star and guard patterns, in the right order, and explain why a bare name isn't a constant
- [x] argue for EAFP, and keep your `try` blocks small
- [x] define an exception of your own, translate low-level errors into it, and choose between `from error` and `from None`
- [x] use `try` with `else` and `finally`
- [x] handle files with `pathlib` and `with`, and always say `encoding="utf-8"`
- [x] write data out as JSON and read it back, and rebuild a dataclass with `**`
- [x] design program logic as a function from state and input to a new state and output, and say what that buys you
- [x] test with `tmp_path` and `pytest.raises`, and write tests for your data
- [x] develop a feature on a Git branch, merge it, and delete the branch

**Read more:** [Modules](https://docs.python.org/3/tutorial/modules.html) · [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) · [The `enum` HOWTO](https://docs.python.org/3/howto/enum.html) · [PEP 636: a tutorial for `match`](https://peps.python.org/pep-0636/), whose worked example happens to be a text adventure · [Errors and exceptions](https://docs.python.org/3/tutorial/errors.html) · [`pathlib`](https://docs.python.org/3/library/pathlib.html) · [`json`](https://docs.python.org/3/library/json.html) · [Pro Git: branching and merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)

The ant lived on a set of tuples, in a world without edges. So does the most famous program in the history of recreational computing, and it's next: Project 6 is Conway's Game of Life. It brings *generators*, which are Python's way of describing a sequence that never ends, and it's where your work goes up on GitHub.
