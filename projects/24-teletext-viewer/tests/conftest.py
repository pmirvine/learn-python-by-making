from collections.abc import Callable
from datetime import UTC, date, datetime
from pathlib import Path

import pytest
from pyfax import Page
from pyfax.content import pages

from teleview.app import Viewer

CONTENT = Path(__file__).parent.parent / "content"
NOON = datetime(2026, 9, 20, 12, 0, 0, tzinfo=UTC)


@pytest.fixture(scope="session")
def site() -> list[Page]:
    return pages(CONTENT, date(2026, 9, 20))


@pytest.fixture
def make_viewer(site: list[Page]) -> Callable[[], Viewer]:
    """Return a function that makes a viewer whose clock has stopped.

    An app can only be run once, and so a test that runs two needs to make two.
    """
    return lambda: Viewer(site, clock=lambda: NOON)
