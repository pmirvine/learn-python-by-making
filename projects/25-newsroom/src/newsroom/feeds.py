"""Reading a news feed. There are two formats in the wild, RSS and Atom, and both are XML."""

import tomllib
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

ATOM = "{http://www.w3.org/2005/Atom}"


class FeedError(Exception):
    """A feed that couldn't be fetched, or made no sense when it arrived."""


@dataclass(frozen=True, slots=True)
class Feed:
    name: str
    url: str


@dataclass(frozen=True, slots=True)
class Story:
    title: str
    link: str


def parse(xml: str) -> list[Story]:
    """Return the stories in a feed, newest first, as the feed had them."""
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as error:
        raise FeedError(f"it isn't XML: {error}") from error

    if root.tag == "rss":
        items = root.iter("item")
        return [
            Story(tidy(item.findtext("title")), tidy(item.findtext("link")))
            for item in items
        ]
    if root.tag == f"{ATOM}feed":
        stories: list[Story] = []
        for entry in root.iter(f"{ATOM}entry"):
            link = entry.find(f"{ATOM}link")
            address = link.get("href", "") if link is not None else ""
            stories.append(Story(tidy(entry.findtext(f"{ATOM}title")), address))
        return stories
    raise FeedError(f"it's XML, but it isn't a feed: <{root.tag}>")


def tidy(text: str | None) -> str:
    """Turn any run of white space into one space. A missing title is an empty one."""
    return " ".join((text or "").split())


def load_feeds(path: Path) -> list[Feed]:
    """Read the list of feeds to follow, from a TOML file."""
    with path.open("rb") as file:
        data = tomllib.load(file)
    match data:
        case {"feeds": [*entries]}:
            pass
        case _:
            raise FeedError(f"{path.name} should have some [[feeds]] in it")
    feeds: list[Feed] = []
    for entry in entries:
        match entry:
            case {"name": str(name), "url": str(url)}:
                feeds.append(Feed(name, url))
            case _:
                raise FeedError(
                    f"every feed needs a name and a url, and this has {entry}"
                )
    return feeds
