"""A colleague's new room for the adventure: the pantry.

You can see the jam. You can't take the jam. Why not?
"""

from dataclasses import dataclass

PLAYER = "player"
MAX_LOAD = 5


@dataclass
class Item:
    description: str
    weight: int


ITEMS = {
    "marmalade": Item("Thick cut. Somebody has been at it with a buttery knife.", 2),
    "jelly": Item("Home-made strawberry jam, with a gingham hat on.", 2),
    "teapot": Item("Brown, and big enough for a church fete.", 4),
}

START_PLACES = {"marmalade": "pantry", "jam": "pantry", "teapot": "pantry"}


def load(places: dict[str, str]) -> int:
    """Return the total weight of everything the player is carrying."""
    return sum(ITEMS[name].weight for name, where in places.items() if where == PLAYER)


def take(
    places: dict[str, str], location: str, name: str
) -> tuple[dict[str, str], str]:
    """Pick something up, if it's here and not too heavy. Return (places, reply)."""
    try:
        if places[name] != location:
            return places, f"I can't see any {name} here."
        item = ITEMS[name]
        if load(places) + item.weight > MAX_LOAD:
            return places, f"You can't manage the {name} as well."
        return places | {name: PLAYER}, "Taken."
    except KeyError:
        return places, f"I can't see any {name} here."


def main() -> None:
    places = START_PLACES.copy()
    while True:
        here = [name for name, where in places.items() if where == "pantry"]
        print(f"\nThe Pantry. You can see: {', '.join(here) or 'nothing'}.")
        words = input("> ").lower().split()
        match words:
            case ["quit" | "q"]:
                break
            case ["take", name]:
                places, reply = take(places, "pantry", name)
                print(reply)
            case _:
                print("Try: take something, or quit.")


if __name__ == "__main__":
    main()
