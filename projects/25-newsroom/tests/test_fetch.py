import asyncio
import time

import pytest
from conftest import ASLEEP, BROKEN, GAZETTE, TURTLES, FakeWeb

from newsroom.feeds import Feed, FeedError
from newsroom.fetch import fetch_all, fetch_one


async def test_fetching_one_feed(client):
    stories = await fetch_one(client, GAZETTE)
    assert len(stories) == 3


async def test_a_feed_that_fails_is_a_feed_error(client):
    with pytest.raises(FeedError, match="HTTPStatusError"):
        await fetch_one(client, BROKEN)


async def test_twelve_feeds_take_about_as_long_as_one(client, web: FakeWeb):
    web.delay = 0.1
    feeds = [Feed(f"Gazette {n}", GAZETTE.url) for n in range(12)]
    started = time.perf_counter()
    results = await fetch_all(client, feeds, at_once=12)
    took = time.perf_counter() - started
    assert len(results) == 12
    assert took < 0.5  # and not 12 x 0.1 = 1.2 seconds
    assert sum(result.seconds for result in results) > 1.0


async def test_no_more_than_a_few_at_a_time(client, web: FakeWeb):
    feeds = [Feed(f"Gazette {n}", GAZETTE.url) for n in range(12)]
    await fetch_all(client, feeds, at_once=3)
    assert web.busiest == 3
    assert len(web.asked) == 12


async def test_one_bad_feed_does_not_spoil_the_others(client):
    good, bad, also_good = await fetch_all(client, [GAZETTE, BROKEN, TURTLES])
    assert (len(good.stories), len(also_good.stories)) == (3, 2)
    assert bad.stories == []
    assert "503" in bad.problem


async def test_a_feed_that_never_answers_is_given_up_on(client):
    started = time.perf_counter()
    slow, quick = await fetch_all(client, [ASLEEP, GAZETTE], patience=0.2)
    assert time.perf_counter() - started < 1
    assert slow.problem == "no answer in 0.2 seconds"
    assert len(quick.stories) == 3


async def test_the_results_come_back_in_the_order_of_the_feeds(client, web: FakeWeb):
    results = await fetch_all(client, [TURTLES, GAZETTE, BROKEN])
    assert [result.feed.name for result in results] == ["Turtles", "Gazette", "Broken"]


async def test_cancelling_the_whole_fetch_cancels_every_part_of_it(
    client, web: FakeWeb
):
    task = asyncio.create_task(fetch_all(client, [ASLEEP, ASLEEP, ASLEEP], patience=60))
    await asyncio.sleep(0.05)
    assert web.busy == 3
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert web.busy == 0
