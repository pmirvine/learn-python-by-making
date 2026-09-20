from pathlib import Path

import pytest

from newsroom.feeds import Feed, FeedError, Story, load_feeds, parse

FEEDS = Path(__file__).parent / "feeds"


def test_rss():
    stories = parse((FEEDS / "hedgehog.rss").read_text(encoding="utf-8"))
    assert stories[0] == Story(
        "Hedgehog wins village bake-off", "https://gazette.example/hedgehog"
    )
    assert stories[1].title == "School robot escapes again"
    assert stories[2].title == "Parish council & the duck pond: a statement"


def test_atom():
    stories = parse((FEEDS / "turtle.atom").read_text(encoding="utf-8"))
    assert [story.link for story in stories] == [
        "https://turtles.example/journey",
        "https://turtles.example/pen",
    ]


@pytest.mark.parametrize(
    ("xml", "complaint"),
    [("Dear Sir,", "it isn't XML"), ("<html><body/></html>", "isn't a feed: <html>")],
)
def test_things_that_are_not_feeds(xml, complaint):
    with pytest.raises(FeedError, match=complaint):
        parse(xml)


def test_the_list_of_feeds(tmp_path):
    path = tmp_path / "feeds.toml"
    path.write_text(
        '[[feeds]]\nname = "Gazette"\nurl = "https://gazette.example/rss"\n'
    )
    assert load_feeds(path) == [Feed("Gazette", "https://gazette.example/rss")]
    path.write_text('[[feeds]]\nname = "No address"\n')
    with pytest.raises(FeedError, match="needs a name and a url"):
        load_feeds(path)
