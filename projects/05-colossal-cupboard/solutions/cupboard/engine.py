"""The rules of the game, with the challenges added.

Tweaks: more synonyms, and the exits listed in every description. There's a new
room in world.py. Extend 2: a score, from rooms visited and the game won.
(Extend 1, undo, is in __init__.py, because it's the front end's business.)

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
    # JSON has no sets, so the rooms visited are kept as a sorted list.
    visited: list[str] = field(default_factory=lambda: [START])


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
    exits = [direction.value for direction in room.exits]
    lines.append(f"Exits: {', '.join(exits)}.")
    return "\n".join(lines)


def score(state: State) -> int:
    """Five points for every room visited, and fifty for winning."""
    return 5 * len(state.visited) + (50 if state.won else 0)


def go(state: State, direction: Direction) -> tuple[State, str]:
    try:
        destination = ROOMS[state.location].exits[direction]
    except KeyError:
        return state, "You can't go that way."
    if destination == "study" and not state.unlocked:
        return state, "The study door is locked."
    visited = sorted({*state.visited, destination})
    moved = replace(state, location=destination, visited=visited)
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
        case ["score"]:
            best = 5 * len(ROOMS) + 50
            return state, f"You have {score(state)} points, out of a possible {best}."
        case ["inventory" | "inv" | "i"]:
            new, reply = inventory(state)
        case ["go" | "walk" | "run", word] | [word] if word in DIRECTIONS:
            new, reply = go(state, DIRECTIONS[word])
        case ["take" | "get" | "grab", name] | ["pick", "up", name]:
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
