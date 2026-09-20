import random

import pytest
from retry import with_retries

from newsroom.feeds import FeedError


class Flaky:
    """Fails so many times, and then works."""

    def __init__(self, failures: int) -> None:
        self.failures = failures
        self.calls = 0

    async def __call__(self) -> str:
        self.calls += 1
        if self.calls <= self.failures:
            raise FeedError(f"failure {self.calls}")
        return "the news"


async def test_it_tries_again_until_it_works():
    flaky = Flaky(failures=2)
    assert (
        await with_retries(flaky, first_wait=0.001, rng=random.Random(1)) == "the news"
    )
    assert flaky.calls == 3


async def test_and_gives_up_in_the_end_with_the_last_error():
    flaky = Flaky(failures=5)
    with pytest.raises(FeedError, match="failure 3"):
        await with_retries(flaky, attempts=3, first_wait=0.001)
    assert flaky.calls == 3
