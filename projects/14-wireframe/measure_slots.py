"""How much does __slots__ save? Make a lot of points each way, and ask."""

import tracemalloc
from dataclasses import dataclass

COUNT = 200_000


@dataclass(frozen=True)
class Roomy:
    x: float
    y: float
    z: float


@dataclass(frozen=True, slots=True)
class Slotted:
    x: float
    y: float
    z: float


for kind in (Roomy, Slotted):
    tracemalloc.start()
    points = [kind(1.5, 2.5, 3.5) for _ in range(COUNT)]
    size, _peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{kind.__name__:8} {size / COUNT:4.0f} bytes each, {size / 1e6:5.1f} MB")
