"""Drive a real browser, with no window, to check the web chapters and take their pictures.

This is an authoring tool, and not part of the checks: it needs Google Chrome on
the machine, and the `websockets` package.

    uv run --with websockets python scripts/browser.py http://127.0.0.1:5000/ shot.png

It speaks the Chrome DevTools Protocol, which is JSON over a web socket.
"""

import asyncio
import base64
import json
import shutil
import socket
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Any, Self

import websockets

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def tabs_of(port: int) -> list[dict[str, Any]]:
    """Ask a Chrome that's listening on a port which tabs it has open."""
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json") as reply:
        return json.load(reply)


class Browser:
    """One tab of a headless Chrome. Use it with `async with`."""

    def __init__(self, width: int = 960, height: int = 720) -> None:
        self.size = (width, height)
        self.messages: list[str] = []  # the page's console, and its errors
        self.sent = 0

    async def __aenter__(self) -> Self:
        port = free_port()
        self.profile = tempfile.mkdtemp(prefix="tutorial-chrome-")
        self.process = await asyncio.create_subprocess_exec(
            shutil.which("google-chrome") or CHROME,
            "--headless=new",
            f"--remote-debugging-port={port}",
            f"--user-data-dir={self.profile}",
            f"--window-size={self.size[0]},{self.size[1]}",
            "--hide-scrollbars",
            "--no-first-run",
            "about:blank",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        for _ in range(100):
            try:
                tabs = await asyncio.to_thread(tabs_of, port)
                break
            except OSError:
                await asyncio.sleep(0.1)
        else:
            raise RuntimeError("Chrome didn't start")
        page = next(tab for tab in tabs if tab["type"] == "page")
        self.socket = await websockets.connect(
            page["webSocketDebuggerUrl"], max_size=50_000_000
        )
        for domain in ("Page", "Runtime", "Log"):
            await self.call(f"{domain}.enable")
        return self

    async def __aexit__(self, *details: object) -> None:
        await self.socket.close()
        self.process.terminate()
        await self.process.wait()
        shutil.rmtree(self.profile, ignore_errors=True)

    async def call(self, method: str, **params: Any) -> dict[str, Any]:
        """Send one command, and wait for its reply, noting any messages on the way."""
        self.sent += 1
        number = self.sent
        await self.socket.send(
            json.dumps({"id": number, "method": method, "params": params})
        )
        while True:
            message = json.loads(await self.socket.recv())
            if message.get("id") == number:
                if "error" in message:
                    raise RuntimeError(f"{method}: {message['error']}")
                return message.get("result", {})
            self.note(message)

    def note(self, message: dict[str, Any]) -> None:
        match message:
            case {"method": "Log.entryAdded", "params": {"entry": {"text": text}}}:
                self.messages.append(text)
            case {
                "method": "Runtime.exceptionThrown",
                "params": {"exceptionDetails": details},
            }:
                self.messages.append(str(details.get("exception", details)))
            case {"method": "Runtime.consoleAPICalled", "params": {"args": arguments}}:
                self.messages.append(" ".join(str(a.get("value")) for a in arguments))
            case _:
                pass

    async def go(self, address: str, settle: float = 0.5) -> None:
        await self.call("Page.navigate", url=address)
        await asyncio.sleep(settle)

    async def evaluate(self, script: str, settle: float = 0.0) -> Any:
        result = await self.call(
            "Runtime.evaluate", expression=script, awaitPromise=True, returnByValue=True
        )
        if settle:
            await asyncio.sleep(settle)
        return result.get("result", {}).get("value")

    async def shot(self, path: Path) -> None:
        picture = await self.call("Page.captureScreenshot", format="png")
        path.write_bytes(base64.b64decode(picture["data"]))


async def main() -> None:
    address, out = sys.argv[1], Path(sys.argv[2])
    async with Browser() as browser:
        await browser.go(address, settle=1.0)
        await browser.shot(out)
        for message in browser.messages:
            print("console:", message)
    print(f"Saved {out}")


if __name__ == "__main__":
    asyncio.run(main())
