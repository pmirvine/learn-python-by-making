"""How much does parsing once, and keeping the tree, save? Time both halves."""

import timeit

from tiny_basic import Machine
from tiny_basic.parser import parse

LINE = "IF N MOD D = 0 AND D < N THEN PRIME = 0"
TIMES = 20_000


class Silent:
    def write(self, text: str) -> None:
        pass

    def read(self, prompt: str) -> str:
        return ""


machine = Machine(Silent())
machine.variables.update(N=97.0, D=5.0, PRIME=-1.0)
(statement,) = parse(LINE)

parsing = min(timeit.repeat(lambda: parse(LINE), number=TIMES, repeat=5))
running = min(timeit.repeat(lambda: machine.execute(statement), number=TIMES, repeat=5))

print(f"Parsing the line: {parsing / TIMES * 1e6:5.1f} microseconds")
print(f"Running the tree: {running / TIMES * 1e6:5.1f} microseconds")
slower = (parsing + running) / running
print(f"Parsing it every time would be {slower:.1f} times slower.")
