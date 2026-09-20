"""Repo-level checks for Project 25: the stage, the bug hunt, the type-in and the race.

The reader's own tests are in the project's tests/ folder.
"""

import asyncio
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("newsroom", reason="needs the Project 25 environment")

import httpx
from newsroom.feeds import Feed, FeedError

P25 = Path(__file__).parent.parent / "projects" / "25-newsroom"
RSS = (P25 / "tests" / "feeds" / "hedgehog.rss").read_text(encoding="utf-8")


def run(*arguments: str | Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
        check=False,
    )


def test_in_stage_2_one_failure_brings_down_the_whole_group():
    spec = importlib.util.spec_from_file_location(
        "stage2_fetch", P25 / "stages" / "stage2_fetch.py"
    )
    stage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stage)
    finished: list[str] = []

    async def reply(request: httpx.Request) -> httpx.Response:
        if request.url.host == "broken.example":
            return httpx.Response(503)
        await asyncio.sleep(0.2)
        finished.append(request.url.host)
        return httpx.Response(200, text=RSS)

    async def scenario() -> None:
        feeds = [
            Feed("Good", "https://good.example/"),
            Feed("Bad", "https://broken.example/"),
        ]
        async with httpx.AsyncClient(transport=httpx.MockTransport(reply)) as client:
            await stage.fetch_all(client, feeds)

    with pytest.raises(ExceptionGroup) as caught:
        asyncio.run(scenario())
    (problem,) = caught.value.exceptions
    assert isinstance(problem, FeedError)
    assert finished == []  # the good feed was cancelled before it could finish


def test_the_bug_hunt_stops_the_clock_for_three_seconds():
    result = run(P25 / "bughunt" / "frozen.py")
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    arrivals = [line for line in lines if "has arrived" in line]
    assert [line.split()[0] for line in arrivals] == ["1.3s", "2.3s", "3.3s"]
    first_arrival, last_arrival = lines.index(arrivals[0]), lines.index(arrivals[-1])
    assert not any("tick" in line for line in lines[first_arrival:last_arrival])


def test_the_type_in_shares_nine_jobs_between_three_workers():
    result = run(P25 / "workers.py")
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    jobs = sorted(int(re.search(r"job (\d+)", line)[1]) for line in lines[:-1])
    assert jobs == list(range(1, 10))
    assert {line[0] for line in lines[:-1]} == {"A", "B", "C"}
    assert lines[-1] == "9 jobs, by three workers who never met"


def test_the_race_shows_what_the_chapter_says_it_shows():
    result = run(P25 / "race.py")
    assert result.returncode == 0, result.stderr
    times = [float(found) for found in re.findall(r"(\d+\.\d\d) s", result.stdout)]
    alone, threads, together, *_cpu = times
    assert alone > 1.9
    assert threads < 1.0
    assert together < 1.0
