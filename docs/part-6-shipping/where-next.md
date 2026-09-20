# Where next

There are no more chapters. There are five **briefs**: projects described as a client, or a magazine's editor, would have described them, with a goal, some milestones, and nothing else. There are no listings, no stages and no solutions in the repository. Each of them is built on things that you've made already, and each will make you learn something that this tutorial didn't teach, which is the skill that matters most from here on.

Some advice, which applies to all five.

- **Start with the dullest version that could work**, and get it running on the first day. A roguelike with one room and one rat is a roguelike.
- **Keep the rules away from the screen.** You've seen three times over what that buys.
- **Write the test when something surprises you**, and not before you know what you're building.
- **Make a repository on the first day, and commit every time that something works.** Give it a README when it has something to show, and a version number when somebody else could use it.
- **When you're stuck, make the problem smaller**, until it fits in the REPL.
- **Read other people's code.** Every library that you've installed is sitting in a `.venv`, in plain Python, and ++f12++ will take you there.

## Brief 1 · A roguelike

*A dungeon, drawn in characters, that's different every time. You're the `@`.*

Rooms and corridors are generated at random. There are monsters, which move when you move. There are things to pick up. When you die, you're dead, and the next dungeon is a new one.

**You have:** Textual, or Rich's `Live`, for the screen. Dataclasses and enums for the world. `match` for commands. Breadth-first search, from Project 26, which is how a monster finds its way to you. Seeded `random`, from Project 3, which makes a dungeon repeatable, and therefore testable.

**You'll have to find out about:** generating levels, for which "binary space partitioning" and "cellular automata" (Project 6, in disguise) are the phrases to look up. Field of view, so that you can't see through walls: "shadowcasting". An *entity-component* arrangement, when your `Monster` class starts to sprout subclasses.

**Milestones**

1. One room, an `@` that moves, and walls that stop it.
2. A generated level, with several rooms and corridors. A test that every room can be reached from every other.
3. A rat, which moves towards you, and a fight.
4. Field of view, and a memory of what's been seen.
5. Things, an inventory, and stairs to the next level.
6. Saving and restoring. You know why the state should be one plain value.

**Stretch:** a second front end, in Pygame, with Project 15's sprites. If milestone 1 was done properly, it's an afternoon.

## Brief 2 · A multiplayer game server

*Snake, with four snakes, on four computers.*

One program is the server. It owns the rules, and the only true copy of the game. The others are clients, in Pygame. They send their keys, and draw what they're told.

**You have:** Snake's model, from Project 9, which already knows nothing about Pygame. `asyncio`, from Project 25: `TaskGroup`, queues, time-outs, cancellation. JSON, and pydantic for checking what arrives. Project 22's lesson, that a client must never break because the server is slow, or absent.

**You'll have to find out about:** `asyncio.start_server`, and streams, which are asyncio's sockets. How to frame a message, so that the receiver knows where one ends: a line of JSON for each will do. How to run an asyncio client beside a Pygame loop, for which a thread and two queues is the simple answer. Latency, and what to draw while you wait.

**Milestones**

1. An echo server, and a client that talks to it, with a test that starts both.
2. The server runs one snake, on a timer, and broadcasts the state ten times a second. A client draws it.
3. The client sends its keys. Two clients, two snakes.
4. Joining, leaving and disconnecting, none of which may disturb anybody else. Test them with a client that vanishes in mid-message.
5. A lobby, scores, and a new round.

**Stretch:** serve it over WebSockets, from FastAPI, with a client in a browser's `<canvas>`. Project 22 has most of the parts.

## Brief 3 · A teletext news service, on the real internet

*Page 100, on a real address, with today's news on it, every day, with nobody touching it.*

PyFax made the pages, Project 20 made them live, and the newsroom fetched the feeds. Put them together, put them on a server, and keep them running.

**You have:** everything but the last step. The newsroom's `fetch_all`. PyFax's page model and templates. Flask, caches, and SQLite for readers' letters. GitHub Actions.

**You'll have to find out about:** *deployment*. There are two honest routes. The cheap one is static: a scheduled GitHub Action (`on: schedule`) runs the newsroom every half an hour, builds the pages, and publishes them with GitHub Pages, and there's no server at all. The proper one is a small hosted server, for which you'll need a production WSGI server such as gunicorn, environment variables for secrets, a health check, logging that you can read afterwards, and a way to deploy a new version without downtime. Also: a feed's terms of use, and how to be a polite robot.

**Milestones**

1. The newsroom's pages, rendered as PyFax HTML, locally.
2. The static route, live, and updating on a schedule. A page that says when it was last updated, so that you can tell when it's broken.
3. What happens when a feed is down for a day? For a week?
4. The proper route, with the letters page, on a free tier somewhere.
5. Monitoring: how will you know that it's stopped, before a reader tells you?

**Stretch:** page 888, subtitles. Or a Textual client, from Project 24, that reads your service over HTTP, so that there's a teletext set on your desk showing real news.

## Brief 4 · A demake

*Take a game that you love, and rebuild it for a machine that couldn't have run it.*

Choose something far too big: a modern platformer, a city builder, a racing game. Then choose the constraints: Pyxel's, from the side quest, with 16 colours, 256 by 256 pixels and four channels of sound, or your own micro's, from Project 28. The craft is in deciding what the game *is*, when nearly everything has been taken away.

**You have:** Pyxel, or Pygame with the `beeb` palette. The sprite editor. The synthesiser. State machines, from Asteroids. Levels in text files, from Breakout.

**You'll have to find out about:** tile maps, and scrolling. Animation, as a list of frames and a timer. "Game feel": why a jump needs a few frames of grace after you've left the ledge, and why that matters more than graphics. Scope, which is the hardest of them.

**Milestones**

1. One screen, one character, one verb. Jump, or dig, or shoot.
2. One complete level, with a beginning, an end, and a way to fail.
3. Sound, a title screen, and a score.
4. Give it to somebody who hasn't seen it, say nothing, and watch. Write down where they were confused. Fix those things, and nothing else.
5. Release it: a version, a README with a picture that moves, and a wheel.

**Stretch:** `uvx pygbag`, from the bonus chapter, and a link that anybody can click.

## Brief 5 · A 6502, for the brave

*The processor inside the BBC Micro, the Apple II and the Commodore 64: three registers, 56 instructions, and no mercy.*

You've written two interpreters for languages. A processor is an interpreter for a *very* simple language, in which every program ever written for those machines is expressed. Emulate the 6502, give it some memory, and run real machine code from 1981.

**You have:** `bytes`, `bytearray` and bit operations, from Projects 11 and 19. `IntFlag`, which is a status register. A registry of decorated functions, from Projects 16 and 17, which is an instruction table. `match`. A taste for writing tests first, which you'll need.

**You'll have to find out about:** the 6502 itself, which is wonderfully documented: search for "6502 instruction reference", and for "Easy 6502", which is an interactive tutorial. Addressing modes, which are most of the work. The flags, and in particular what overflow means for signed addition. Binary-coded decimal, which you can postpone. And *Klaus Dormann's functional test*, a program that exercises every instruction, and loops for ever at the address of the first thing that your emulator gets wrong. It's the best test suite that you'll ever be given.

**Milestones**

1. Memory, registers, and three instructions: `LDA #`, `STA` and `BRK`. A test that loads a number and stores it.
2. All the addressing modes, for `LDA`. Then the other load, store and transfer instructions come nearly free.
3. Arithmetic and the flags. Branches. The stack, `JSR` and `RTS`.
4. Everything else. Dormann's test passes.
5. Give it a screen: map a range of memory to a `TextScreen`, and watch a machine-code program write "HELLO".

**Stretch:** real BBC BASIC is 16 kilobytes of 6502 code, and asks surprisingly little of the machine around it: a way to write a character, a way to read a line, and a few facts about memory. If your emulator is right, it will run it, and you'll have booted a BBC Micro's BASIC in Python. Then measure how fast it is, and read about PyPy, and Cython, and why people write emulators in Rust.

## And the rest of Python

This tutorial chose depth over breadth, and visual feedback over everything. There are large parts of the Python world that it never entered, and you're now equipped for all of them.

| If you want to | Look at |
|---|---|
| Work with data: tables, statistics, charts | **pandas** or **Polars**, **Matplotlib**, and **Jupyter** notebooks, which are a REPL that keeps its pictures |
| Do arithmetic on millions of numbers at once | **NumPy**, which the rest of scientific Python stands on |
| Build a big web application, with users, forms and an admin site | **Django** |
| Talk to a database without writing SQL by hand | **SQLAlchemy**, or **SQLModel**, which marries it to pydantic |
| Automate your computer, or somebody's web site | `pathlib`, `shutil` and `subprocess`, which you know, and **Playwright** for browsers |
| Build command-line tools that are pleasant to use | **Typer** or **Click**, and Rich, which you know |
| Learn machine learning | **scikit-learn** first, and then **PyTorch** |
| Program a microcontroller | **MicroPython**, or **CircuitPython**: Python, on a board that costs less than a magazine did, and that can blink a real light |
| Make Python faster | a profiler first (`cProfile`, **py-spy**). Then NumPy, then PyPy, and then a compiled extension, in **Rust** with PyO3 and maturin, or in **Cython** |
| Understand Python itself more deeply | *Fluent Python*, by Luciano Ramalho, which is the book to read next. Then the [language reference](https://docs.python.org/3/reference/), which you can now follow |

And one more, which isn't a library. **Contribute to something that you use.** Every project in this tutorial stood on open-source packages, written by people who started where you did. Their repositories have issues marked "good first issue", their documentation has mistakes in it, and you know how to fork, branch, test, commit, push and open a pull request. It's the fastest way there is to learn how experienced people work, and it's how all of this gets made.

```text
>RUN
```
