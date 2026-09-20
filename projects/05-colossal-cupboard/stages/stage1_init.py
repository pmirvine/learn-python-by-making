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
