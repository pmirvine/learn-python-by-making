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
