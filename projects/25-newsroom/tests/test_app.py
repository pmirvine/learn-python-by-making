from datetime import UTC, datetime

from conftest import BROKEN, GAZETTE, TURTLES

from newsroom.app import Newsroom

NOON = datetime(2026, 9, 20, 12, 0, 0, tzinfo=UTC)


async def test_the_news_arrives_while_the_app_is_running(client):
    app = Newsroom([GAZETTE, BROKEN, TURTLES], client, clock=lambda: NOON)
    async with app.run_test(size=(60, 30)) as pilot:
        assert "Fetching the news" in app.site[100].text()
        await app.workers.wait_for_complete()
        await pilot.pause()

        index = app.site[100].text()
        assert "3 feeds in" in index
        assert "Gazette" in index
        assert "failed" in index
        assert sorted(app.site) == [100, 101, 102, 103]

        await pilot.press("1", "0", "1")
        assert app.number == 101
        assert "Hedgehog wins village bake-off" in app.site[101].text()
        assert "This feed couldn't be fetched" in app.site[102].text()


async def test_f_fetches_again(client, web):
    app = Newsroom([GAZETTE], client, clock=lambda: NOON)
    async with app.run_test(size=(60, 30)) as pilot:
        await app.workers.wait_for_complete()
        assert len(web.asked) == 1
        await pilot.press("f")
        await app.workers.wait_for_complete()
        assert len(web.asked) == 2
