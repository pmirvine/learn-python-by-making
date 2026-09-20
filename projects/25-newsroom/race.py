"""Threads, processes and asyncio, timed against each other, on two kinds of work.

uv run race.py                    # with the ordinary Python
uv run --python 3.14t race.py     # with the free-threaded one, which has no GIL
"""

import asyncio
import sys
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

JOBS = 4


def wait(seconds: float) -> float:
    """Work that's all waiting, as a request to a server is."""
    time.sleep(seconds)
    return seconds


def count_primes(limit: int) -> int:
    """Work that's all arithmetic. It never waits for anything."""
    return sum(all(n % d for d in range(2, int(n**0.5) + 1)) for n in range(2, limit))


async def wait_async(seconds: float) -> float:
    await asyncio.sleep(seconds)
    return seconds


async def all_at_once(seconds: float) -> None:
    await asyncio.gather(*(wait_async(seconds) for _ in range(JOBS)))


def timed(label: str, action) -> None:
    started = time.perf_counter()
    action()
    print(f"  {label:<22}{time.perf_counter() - started:5.2f} s")


def main() -> None:
    gil = getattr(sys, "_is_gil_enabled", lambda: True)()
    print(f"Python {sys.version.split()[0]}, {'with' if gil else 'WITHOUT'} the GIL")

    print(f"\n{JOBS} jobs that wait for half a second each:")
    timed("one after another", lambda: [wait(0.5) for _ in range(JOBS)])
    with ThreadPoolExecutor(JOBS) as pool:
        timed("threads", lambda: list(pool.map(wait, [0.5] * JOBS)))
    timed("asyncio", lambda: asyncio.run(all_at_once(0.5)))

    limit = 400_000
    print(f"\n{JOBS} jobs that count the primes below {limit:,}:")
    timed("one after another", lambda: [count_primes(limit) for _ in range(JOBS)])
    with ThreadPoolExecutor(JOBS) as pool:
        timed("threads", lambda: list(pool.map(count_primes, [limit] * JOBS)))
    with ProcessPoolExecutor(JOBS) as pool:
        timed("processes", lambda: list(pool.map(count_primes, [limit] * JOBS)))


if __name__ == "__main__":
    main()
