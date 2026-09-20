"""Pictures of the whole screen, compared with the last ones that were approved."""

from conftest import Parrot
from helpers import say

from adventure.app import AdventureApp
from adventure.colossal import Colossal

EXPLORING = ["south", "east", "take torch", "south"]


def test_exploring(snap_compare):
    async def explore(pilot):
        for command in EXPLORING:
            await say(pilot, command)

    assert snap_compare(
        AdventureApp(Colossal), run_before=explore, terminal_size=(90, 28)
    )


def test_a_game_with_no_map(snap_compare):
    assert snap_compare(AdventureApp(Parrot), terminal_size=(90, 28))
