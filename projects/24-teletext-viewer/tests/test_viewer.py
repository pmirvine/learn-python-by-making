import asyncio

from teleview.app import Viewer
from teleview.widgets import Keypad, PageView


def drive(viewer: Viewer, *keys: str) -> tuple[int, str, str]:
    """Run the app with no screen, press some keys, and report what it's showing."""

    async def scenario() -> tuple[int, str, str]:
        async with viewer.run_test(size=(60, 30)) as pilot:
            await pilot.press(*keys)
            await pilot.pause()
            top = str(viewer.query_one(Keypad).render())
            page = viewer.query_one(PageView).page
            assert page is not None
            return viewer.number, top, page.title

    return asyncio.run(scenario())


def test_it_starts_at_the_index(make_viewer):
    number, top, title = drive(make_viewer())
    assert (number, title) == (100, "Index")
    assert top == "P100   PyFax   Sun 20 Sep  12:00:00"


def test_typing_three_digits_goes_to_a_page(make_viewer):
    number, top, title = drive(make_viewer(), "3", "0", "1")
    assert (number, title) == (301, "Weather: the outlook")
    assert top.startswith("P301 ")


def test_the_number_shows_as_it_is_typed(make_viewer):
    number, top, _title = drive(make_viewer(), "1", "0")
    assert number == 100
    assert top.startswith("P10_ ")


def test_a_page_that_is_not_there_leaves_you_where_you_were(make_viewer):
    number, top, _title = drive(make_viewer(), "7", "7", "7")
    assert number == 100
    assert top.startswith("P100 ")


def test_the_arrows_turn_the_pages_and_stop_at_the_ends(make_viewer):
    assert drive(make_viewer(), "left")[0] == 100
    assert drive(make_viewer(), "right", "right")[0] == 102


def test_i_is_for_index(make_viewer):
    assert drive(make_viewer(), "5", "0", "1", "i")[0] == 100
