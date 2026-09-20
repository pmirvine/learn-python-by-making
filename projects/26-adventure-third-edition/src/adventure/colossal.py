"""The Colossal Cupboard, made to fit. This is the only module that knows both sides."""

from collections import deque
from pathlib import Path

from cupboard.engine import State, describe, is_dark, respond, things_at
from cupboard.saves import SaveError, load, save
from cupboard.world import PLAYER, ROOMS, START, Direction, Room

from adventure.game import Chart, Place

STEPS = {
    Direction.NORTH: (0, -1, 0),
    Direction.SOUTH: (0, 1, 0),
    Direction.EAST: (1, 0, 0),
    Direction.WEST: (-1, 0, 0),
    Direction.UP: (0, 0, 1),
    Direction.DOWN: (0, 0, -1),
}
FLOORS = ["Ground floor", "First floor", "Second floor"]


def layout(rooms: dict[str, Room], start: str) -> dict[str, tuple[int, int, int]]:
    """Work out where every room is, by walking outwards from the first."""
    spots = {start: (0, 0, 0)}
    waiting = deque([start])
    while waiting:
        name = waiting.popleft()
        x, y, floor = spots[name]
        for direction, neighbour in rooms[name].exits.items():
            if neighbour not in spots:
                across, down, up = STEPS[direction]
                spots[neighbour] = (x + across, y + down, floor + up)
                waiting.append(neighbour)
    return spots


SPOTS = layout(ROOMS, START)


class Colossal:
    """The game as an object that remembers: its past is a list of states."""

    title = "The Colossal Cupboard"

    def __init__(self) -> None:
        self.history = [State()]

    @property
    def state(self) -> State:
        return self.history[-1]

    @property
    def over(self) -> bool:
        return self.state.won

    def opening(self) -> str:
        return describe(self.state)

    def play(self, text: str) -> str:
        after, reply = respond(self.state, text)
        if after != self.state:
            self.history.append(after)
        return reply

    def status(self) -> dict[str, str]:
        carrying = things_at(self.state, PLAYER)
        return {
            "Moves": str(self.state.moves),
            "Carrying": ", ".join(carrying) or "nothing",
        }

    def undo(self) -> str:
        if len(self.history) == 1:
            return "There's nothing to take back."
        self.history.pop()
        return "Taken back.\n" + describe(self.state)

    def chart(self) -> Chart:
        seen = {state.location for state in self.history if not is_dark(state)}
        places = {name: place(name) for name in seen}
        dark = Place("?", *SPOTS[self.state.location])
        return Chart(
            tuple(places.values()),
            places.get(self.state.location, dark),
            FLOORS[SPOTS[self.state.location][2]],
        )

    def save(self, path: Path) -> str:
        try:
            save(self.state, path)
        except SaveError as error:
            return str(error)
        return "Saved."

    def restore(self, path: Path) -> str:
        try:
            self.history = [load(path)]
        except SaveError as error:
            return str(error)
        return "Restored.\n" + describe(self.state)


def place(name: str) -> Place:
    """Return a room as the map wants it: a short label, a spot, and its exits."""
    exits = "".join(direction.value[0] for direction in ROOMS[name].exits)
    return Place(name.capitalize(), *SPOTS[name], exits)
