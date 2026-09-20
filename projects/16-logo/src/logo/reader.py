"""Gathering tokens into lists, with the square brackets turned into lists inside lists."""

from collections.abc import Iterator

from logo.errors import LogoError
from logo.tokens import Token

type Item = Token | list[Item]


def read(tokens: Iterator[Token], inside: bool = False) -> list[Item]:
    """Use up tokens until they run out, or, inside brackets, until the closing one."""
    items: list[Item] = []
    for token in tokens:
        if token.text == "[":
            items.append(read(tokens, inside=True))
        elif token.text == "]":
            if not inside:
                raise LogoError(f"There's a ] on line {token.line} with no [ before it")
            return items
        else:
            items.append(token)
    if inside:
        raise LogoError("There's a [ with no ] to close it")
    return items


class Stream:
    """A list of items, and a finger to keep the place."""

    def __init__(self, items: list[Item]) -> None:
        self.items = items
        self.position = 0

    @property
    def more(self) -> bool:
        return self.position < len(self.items)

    def peek(self) -> Item | None:
        """Return the next item, without moving on."""
        return self.items[self.position] if self.more else None

    def take(self) -> Item:
        """Return the next item, and move on."""
        item = self.items[self.position]
        self.position += 1
        return item

    def next_is(self, *texts: str) -> bool:
        """Is the next item one of these symbols or words?"""
        item = self.peek()
        return isinstance(item, Token) and item.kind != "quoted" and item.text in texts
