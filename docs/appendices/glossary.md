# Glossary

The terms of art that this tutorial uses, in a sentence or two each, with the project where each is explained. Words in *italics* have entries of their own.

**ABC (abstract base class)**
:   A class that exists to be inherited from, and that refuses to be instantiated until its abstract methods have been written. [Project 15](../part-2-pygame/p15-sprite-editor.md), [Project 26](../part-5-tui/p26-adventure-third-edition.md).

**Adapter**
:   A small class that stands between two pieces of code that don't know about each other, and speaks to each in its own terms. [Project 26](../part-5-tui/p26-adventure-third-edition.md).

**Aliasing**
:   Two names for one object. Change it through one, and the other sees the change. [Project 4](../part-1-console/p04-codebreaker.md).

**Annotation**
:   See *type hint*.

**API**
:   The part of a program that other programs are meant to use: a package's public functions, or a web server's addresses. [Project 22](../part-4-web/p22-high-score-server.md), [Project 27](../part-6-shipping/p27-ship-it.md).

**Argument, parameter**
:   A *parameter* is the name in the `def`. An *argument* is the value in the call. [Project 2](../part-1-console/p02-turtle-sketchbook.md).

**Attribute**
:   Anything after a dot: `snake.body`, `math.pi`. [Project 9](../part-2-pygame/p09-snake.md).

**Awaitable, coroutine, task**
:   A *coroutine* is what calling an `async def` function gives you: work that hasn't started. A *task* is a coroutine that the *event loop* has been asked to run. Anything that `await` accepts is *awaitable*. [Project 25](../part-5-tui/p25-newsroom.md).

**Blocking**
:   Said of a call that doesn't return until it's finished, and lets nothing else happen meanwhile. Fatal inside an *event loop*. [Project 25](../part-5-tui/p25-newsroom.md), [Project 28](../part-6-shipping/p28-boot-to-basic.md).

**Branch**
:   In Git, a movable name for a line of commits. [Project 5](../part-1-console/p05-colossal-cupboard.md).

**Build backend**
:   The program that turns your source folder into a *wheel*. uv's is `uv_build`. [Project 27](../part-6-shipping/p27-ship-it.md).

**Callable**
:   Anything that can be called with brackets: a function, a method, a class, an object with `__call__`. [Project 7](../part-1-console/p07-fractal-factory.md).

**CI (continuous integration)**
:   A robot that runs your checks on every push. [Project 17](../part-3-interpreters/p17-tiny-basic.md).

**Class, instance**
:   A *class* is a kind of object, and the recipe for making them. An *instance* is one that's been made. [Project 9](../part-2-pygame/p09-snake.md).

**Closure**
:   A function that remembers variables from the place where it was made. [Project 7](../part-1-console/p07-fractal-factory.md).

**Commit**
:   In Git, a snapshot of the whole project, with a message, a parent, and a name made from its contents. [Project 0](../part-0-switching-on/p00-hello-beeb.md).

**Composition**
:   Building an object out of other objects that it *has*, as opposed to a class that it *is*. [Project 9](../part-2-pygame/p09-snake.md), [Project 15](../part-2-pygame/p15-sprite-editor.md).

**Comprehension**
:   A list, dictionary or set, written as a description of its contents: `[n * n for n in numbers if n > 0]`. [Project 3](../part-1-console/p03-dice-lab.md).

**Context manager**
:   An object for use with `with`, which sets something up, and clears it away afterwards, whatever happens in between. [Project 5](../part-1-console/p05-colossal-cupboard.md), [Project 18](../part-4-web/p18-svg-plotter.md).

**CPython**
:   The Python that nearly everybody means by "Python": the original, written in C. There are others, such as PyPy and MicroPython.

**Dataclass**
:   A class written as a list of fields, for which Python writes `__init__`, `__repr__` and `__eq__`. [Project 5](../part-1-console/p05-colossal-cupboard.md).

**Decorator**
:   A function that takes a function, and returns one, applied with `@`. It either wraps the function, or registers it. [Project 16](../part-3-interpreters/p16-logo.md).

**Dependency**
:   A package that yours needs. A *development* dependency is needed only to work on yours. [Project 4](../part-1-console/p04-codebreaker.md), [Project 27](../part-6-shipping/p27-ship-it.md).

**Dependency injection**
:   Handing an object what it needs, such as a clock or a source of random numbers, where it might have fetched it for itself. It makes testing possible. [Project 9](../part-2-pygame/p09-snake.md).

**Descriptor**
:   An object that takes charge of what happens when an attribute is read or assigned. Properties, methods and Textual's reactive attributes are all descriptors. [Project 24](../part-5-tui/p24-teletext-viewer.md).

**Distribution**
:   What an *index* holds and an installer installs: a name and a version. It's not always the name that you import. [Project 27](../part-6-shipping/p27-ship-it.md).

**Docstring**
:   A string as the first thing in a function, class or module, which `help()` shows. [Project 1](../part-1-console/p01-hi-lo.md).

**Duck typing**
:   Caring about what an object can do, and not what it is. "If it quacks." [Project 12](../part-2-pygame/p12-asteroids.md).

**Dunder**
:   A name with a double underscore at each end, such as `__init__` and `__add__`, by which Python calls on your objects. [Project 12](../part-2-pygame/p12-asteroids.md).

**EAFP**
:   "Easier to ask forgiveness than permission": try it, and catch the exception. Its opposite is LBYL, "look before you leap". [Project 5](../part-1-console/p05-colossal-cupboard.md).

**Editable install**
:   A package installed as a pointer to its source folder, so that changes take effect at once. [Project 5](../part-1-console/p05-colossal-cupboard.md), [Project 11](../part-2-pygame/p11-sound-and-envelope.md).

**Entry point**
:   A name, in a package's metadata, for a function to call: a command, or a plug-in. [Project 5](../part-1-console/p05-colossal-cupboard.md), [Project 27](../part-6-shipping/p27-ship-it.md).

**Environment (virtual)**
:   A folder, `.venv`, with a Python and a set of installed packages that belong to one project. [Project 0](../part-0-switching-on/p00-hello-beeb.md), [Project 27](../part-6-shipping/p27-ship-it.md).

**Event loop**
:   A loop that waits for things to happen, and hands each to whoever's interested. Pygame programs have one that you write. asyncio and Textual have one that you're given. [Project 8](../part-2-pygame/p08-mode2-sketchpad.md), [Project 25](../part-5-tui/p25-newsroom.md).

**Exception**
:   An object that's raised when something goes wrong, and travels up through the calls until something catches it. [Project 1](../part-1-console/p01-hi-lo.md).

**Expression, statement**
:   An *expression* has a value: `2 + 2`, `name.upper()`. A *statement* does something: `x = 1`, `if`, `def`. 

**Fake, stand-in, spy**
:   Objects used in tests in place of real ones. A *fake* works, simply. A *spy* records what was done to it. [Project 7](../part-1-console/p07-fractal-factory.md), [Project 26](../part-5-tui/p26-adventure-third-edition.md).

**Fixture**
:   In pytest, a function that prepares something that tests ask for by name. [Project 8](../part-2-pygame/p08-mode2-sketchpad.md), [Project 20](../part-4-web/p20-pyfax-live.md).

**Framework, library**
:   You call a *library*. A *framework* calls you. [Project 8](../part-2-pygame/p08-mode2-sketchpad.md), [Project 24](../part-5-tui/p24-teletext-viewer.md).

**f-string**
:   A string with an `f` in front, in which `{expressions}` are worked out and formatted. [Project 1](../part-1-console/p01-hi-lo.md).

**Generator**
:   A function with `yield` in it. Calling it gives an *iterator*, which runs the function a piece at a time, as values are asked for. [Project 6](../part-1-console/p06-life.md).

**Generic**
:   A class or function whose type hints have a gap in them, to be filled in by whoever uses it: `Peekable[T]`. [Project 17](../part-3-interpreters/p17-tiny-basic.md).

**GIL (global interpreter lock)**
:   The lock in *CPython* that lets only one thread run Python at a time. [Project 25](../part-5-tui/p25-newsroom.md).

**Hashable**
:   Able to be a dictionary key, or a member of a set. In practice: immutable. [Project 4](../part-1-console/p04-codebreaker.md), [Project 12](../part-2-pygame/p12-asteroids.md).

**Immutable, mutable**
:   An *immutable* object can't be changed after it's made: numbers, strings, tuples, frozen dataclasses. A *mutable* one can: lists, dictionaries, sets, most objects. [Project 4](../part-1-console/p04-codebreaker.md).

**Index (package index)**
:   A server that holds *distributions*. PyPI is the one that everybody uses. [Project 27](../part-6-shipping/p27-ship-it.md).

**Inheritance**
:   Making a class as a special kind of another, which gets its parent's methods, and may replace them. [Project 15](../part-2-pygame/p15-sprite-editor.md).

**Interpreter**
:   A program that runs programs. CPython is one. You've written two. [Project 16](../part-3-interpreters/p16-logo.md), [Project 17](../part-3-interpreters/p17-tiny-basic.md).

**Iterable, iterator**
:   An *iterable* is anything that a `for` loop can go through. An *iterator* is the thing that remembers how far it's got. [Project 6](../part-1-console/p06-life.md).

**Keyword argument**
:   An argument given by name: `box(width=10)`. [Project 2](../part-1-console/p02-turtle-sketchbook.md).

**Lint, linter**
:   A program that reads your code and points out likely mistakes. Ruff. [Project 3](../part-1-console/p03-dice-lab.md).

**Lock file**
:   `uv.lock`: the exact version of everything, so that every computer builds the same *environment*. [Project 0](../part-0-switching-on/p00-hello-beeb.md), [Project 27](../part-6-shipping/p27-ship-it.md).

**Method**
:   A function that belongs to a class, and is given the object as its first argument, `self`. [Project 9](../part-2-pygame/p09-snake.md), [Project 24](../part-5-tui/p24-teletext-viewer.md).

**Module, package**
:   A *module* is a file of Python. A *package* is a folder of modules, with an `__init__.py`. [Project 5](../part-1-console/p05-colossal-cupboard.md).

**Name, binding**
:   A *name* is a label. *Binding* is tying it to an object, which is all that `=` does. [Project 1](../part-1-console/p01-hi-lo.md).

**Namespace**
:   A place where names live: a module, a function's locals, an object's attributes.

**Parser, tokeniser**
:   A *tokeniser* chops text into words and symbols. A *parser* works out what they mean together. [Project 16](../part-3-interpreters/p16-logo.md), [Project 17](../part-3-interpreters/p17-tiny-basic.md).

**PEP**
:   A Python Enhancement Proposal: the document in which a change to Python is argued for, and decided. PEP 8 is the style guide.

**Property**
:   A method that's read as if it were an *attribute*. [Project 10](../part-2-pygame/p10-breakout.md).

**Protocol**
:   A description of what an object must be able to do, for the *type checker*, which nothing has to inherit from. [Project 12](../part-2-pygame/p12-asteroids.md), [Project 26](../part-5-tui/p26-adventure-third-edition.md).

**Pull request**
:   A proposal, on GitHub, to merge one *branch* into another, with a place to discuss it. [Project 16](../part-3-interpreters/p16-logo.md).

**Pure function**
:   One whose result depends only on its arguments, and which changes nothing. The easiest kind of code to test, and to reuse. [Project 5](../part-1-console/p05-colossal-cupboard.md), [Project 26](../part-5-tui/p26-adventure-third-edition.md).

**PyPI**
:   The Python Package Index, at pypi.org. [Project 27](../part-6-shipping/p27-ship-it.md).

**Pythonic**
:   Written as an experienced Python programmer would write it: using the language's own idioms, and not another's.

**Recursion**
:   A function that calls itself, on a smaller piece of the problem. [Project 2](../part-1-console/p02-turtle-sketchbook.md).

**Refactoring**
:   Changing how code is arranged, without changing what it does. Tests are what make it safe. [Project 10](../part-2-pygame/p10-breakout.md).

**Registry**
:   A dictionary of functions, filled in by a *decorator*, so that new abilities can be added without editing a central list. [Project 16](../part-3-interpreters/p16-logo.md), [Project 28](../part-6-shipping/p28-boot-to-basic.md).

**REPL**
:   Read, evaluate, print, loop: the `>>>` prompt. [Project 0](../part-0-switching-on/p00-hello-beeb.md).

**Repository**
:   A project's folder, with its whole history, as Git keeps it. [Project 0](../part-0-switching-on/p00-hello-beeb.md).

**Scope**
:   The part of a program in which a name means something. [Project 7](../part-1-console/p07-fractal-factory.md).

**sdist**
:   A source distribution: your project's source, packed up, from which a *wheel* can be built. [Project 27](../part-6-shipping/p27-ship-it.md).

**Semantic versioning**
:   Version numbers that say what kind of change was made: major, minor, patch. [Project 22](../part-4-web/p22-high-score-server.md), [Project 27](../part-6-shipping/p27-ship-it.md).

**Sequence**
:   An ordered collection that can be indexed and sliced: a list, a tuple, a string, a `range`. [Project 3](../part-1-console/p03-dice-lab.md).

**Shadowing**
:   Hiding a name with another of the same name, nearer in. [Project 7](../part-1-console/p07-fractal-factory.md).

**Side effect**
:   Anything that a function does apart from returning a value: printing, writing a file, changing its arguments.

**Slice**
:   A piece of a *sequence*: `items[1:4]`. [Project 3](../part-1-console/p03-dice-lab.md).

**Standard library**
:   The modules that come with Python: `math`, `random`, `pathlib`, `json`, `asyncio`, and two hundred more.

**State machine**
:   A thing that's always in exactly one of a few named states, with rules for moving between them. [Project 9](../part-2-pygame/p09-snake.md).

**Structured concurrency**
:   The rule that tasks can't outlive the block that started them. `TaskGroup`. [Project 25](../part-5-tui/p25-newsroom.md).

**Tag**
:   In Git, a permanent name for one *commit*, usually a version. [Project 7](../part-1-console/p07-fractal-factory.md), [Project 22](../part-4-web/p22-high-score-server.md).

**Traceback**
:   The report of an uncaught *exception*: what went wrong, where, and how the program got there. Read it from the bottom. [Project 1](../part-1-console/p01-hi-lo.md).

**Truthy, falsy**
:   Counting as true, or as false, in an `if`. Empty things, nought and `None` are falsy. [Project 1](../part-1-console/p01-hi-lo.md).

**Tuple**
:   An *immutable* *sequence*, usually of a fixed number of things that belong together: a point, a colour. [Project 2](../part-1-console/p02-turtle-sketchbook.md).

**Type checker**
:   A program that reads your *type hints*, and tells you where they don't add up, without running anything. Pyright, which is inside Pylance. [Project 4](../part-1-console/p04-codebreaker.md), [Project 17](../part-3-interpreters/p17-tiny-basic.md).

**Type hint**
:   A note about what type a name is meant to have: `def area(width: int) -> int`. Python ignores it at run time. [Project 3](../part-1-console/p03-dice-lab.md).

**Unpacking**
:   Assigning the items of a *sequence* to several names at once: `x, y = point`. [Project 2](../part-1-console/p02-turtle-sketchbook.md).

**Wheel**
:   A built package: a zip file, ready to be installed by unzipping. [Project 17](../part-3-interpreters/p17-tiny-basic.md), [Project 27](../part-6-shipping/p27-ship-it.md).

**Widget**
:   In Textual, and in user interfaces generally, one piece of the screen that looks after itself. [Project 24](../part-5-tui/p24-teletext-viewer.md).
