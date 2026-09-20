"""A colleague's BASIC gets some sums wrong, and some right.

uv run bughunt/sums.py
"""

from tiny_basic import nodes
from tiny_basic.nodes import Expression
from tiny_basic.parser import PRECEDENCE, Parser
from tiny_basic.values import combine


class ColleaguesParser(Parser):
    """The same as yours, but for one line in the middle of this method."""

    def expression(self, minimum: int = 1) -> Expression:
        left = self.operand()
        while True:
            token = self.tokens.peek()
            if token is None or token.kind == "string" or token.text not in PRECEDENCE:
                return left
            precedence = PRECEDENCE[token.text]
            if precedence < minimum:
                return left
            next(self.tokens)
            left = nodes.Binary(left, token.text, self.expression(precedence))


def value(tree: Expression) -> float:
    """Work out a tree that's made of numbers and nothing else."""
    match tree:
        case nodes.Number(number):
            return number
        case nodes.Binary(left, sign, right):
            result = combine(value(left), sign, value(right))
            assert isinstance(result, float)
            return result
        case _:
            raise ValueError(f"I can only do sums, and this is {tree}")


def main() -> None:
    sums = {
        "2 + 3 * 4": 14,
        "2 * 3 + 4": 10,
        "2 ^ 3 ^ 2": 512,
        "10 - 4 - 3": 3,
        "100 / 10 / 5": 2,
        "10 - 4 + 3": 9,
    }
    for text, right in sums.items():
        got = value(ColleaguesParser(text).expression())
        verdict = "" if got == right else f"   <-- it ought to be {right}"
        print(f"{text:14} = {got:g}{verdict}")


if __name__ == "__main__":
    main()
