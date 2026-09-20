# Learn Python by Making

In 1982 you could switch on a BBC Micro, type three lines, and have a yellow line drawn across your television before the kettle had boiled.

```bbcbasic
10 MODE 2
20 GCOL 0,3
30 MOVE 0,0 : DRAW 1279,1023
```

Nothing to install. Nothing to configure. You typed, the machine answered, and because it answered with *pictures* and *noises*, you kept typing. A lot of people learned to program that way, and it's still the best way there is: make a thing, see it work, change it, see what happens.

This tutorial teaches Python like that. It is a series of twenty-eight projects. Each one makes something you can see, hear or play with, and each one is there to teach a particular part of the language.

![Red and yellow lines fanning out from the bottom corners of a black screen, crossing to make interference patterns](assets/p08-moire.png){ .pixels }

*Project 8: fourteen lines of Python, using drawing commands you write yourself.*

## Who it's for

You can already program a bit. Perhaps it was BBC BASIC at school, or some JavaScript, or C# at work. You know what a loop is. You don't need another book that spends forty pages on `if`.

What you want is to know Python *properly*: not only the syntax, but how the language thinks, what good Python looks like, and how people who write it for a living go about their work.

So this tutorial moves quickly over what you know and slowly over what's different. And from the first project it has you working the way professionals do: with Git, a proper editor, tests, type hints and packaging. Each of those arrives when a project needs it.

## What you'll make

| Part | You make | Python you learn |
|---|---|---|
| **0 · Switching on** | A working toolkit, and a first program | uv, VS Code, Git, the REPL |
| **1 · Console** | Guessing games, turtle art, a text adventure, Life, fractals | The core: objects and names, collections, functions, modules, exceptions, generators |
| **2 · Pygame** | Your own `MOVE` and `DRAW`, Snake, Breakout, a sound synth, Asteroids, 3D wireframes, a sprite editor | Classes, the data model, protocols, composition |
| **3 · Interpreters** | A Logo interpreter, then a BASIC of your own | Decorators, pattern matching, typing in depth, CI |
| **4 · Web** | SVG art, a teletext-style site, a live Flask service, a high-score API | Templates, databases, HTTP, async beginnings |
| **5 · TUI** | Dashboards and full-screen terminal apps with Textual | Descriptors, asyncio, architecture |
| **6 · Shipping** | A published package, then the capstone | Packaging, releases |

The capstone pulls it together: a little computer of your own, in a window, that boots to a `>` prompt and runs programs written in *your* BASIC, with *your* graphics, sound and sprites.

The [roadmap](roadmap.md) lists every project.

!!! note "This is a work in progress"
    The tutorial is being written now. Part 0, Project 1 and Project 8 are here as a pilot. The roadmap shows what's coming.

## Start here

1. Read [How to use this tutorial](part-0-switching-on/how-to-use.md). It's short, and it explains the furniture.
2. Set up [The toolkit](part-0-switching-on/toolkit.md).
3. Write your first program in [Project 0 · Hello, Beeb](part-0-switching-on/p00-hello-beeb.md).

## Licence

The text is licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). All the code is MIT-licensed: use it for anything.
