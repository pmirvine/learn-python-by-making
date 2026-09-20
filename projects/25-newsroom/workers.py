import asyncio
import random


async def worker(name: str, jobs: asyncio.Queue[int], done: list[str]) -> None:
    while True:
        job = await jobs.get()
        await asyncio.sleep(random.uniform(0.1, 0.4))  # pretend to fetch something
        done.append(f"{name} did job {job}")
        print(done[-1])
        jobs.task_done()


async def main() -> None:
    jobs: asyncio.Queue[int] = asyncio.Queue()
    done: list[str] = []
    for job in range(1, 10):
        jobs.put_nowait(job)

    async with asyncio.TaskGroup() as group:
        staff = [group.create_task(worker(name, jobs, done)) for name in "ABC"]
        await jobs.join()  # wait until every job has been marked as done
        for member in staff:
            member.cancel()
    print(f"{len(done)} jobs, by three workers who never met")


asyncio.run(main())
