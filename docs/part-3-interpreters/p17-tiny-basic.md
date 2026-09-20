# Project 17 · Tiny BASIC

```text
>10 PRINT "HELLO"
>20 GOTO 10
>RUN
HELLO
HELLO
HELLO
```

Everybody who ever stood in front of a BBC Micro in a shop typed that, or something ruder, and walked away leaving it running. It was the first program of a whole generation of programmers. Now you're going to write the thing that runs it: line numbers, `GOTO`, `FOR` and `NEXT`, `GOSUB`, strings with dollar signs on, BBC BASIC's own `REPEAT … UNTIL`, and a `>` prompt to type it all at.

Your Logo read its program again, word by word, every time round a loop. This interpreter works as nearly every real one does. Each line is **parsed once**, as it's typed, into a **tree** of small objects, and running the program means walking the tree. The tree is made of dataclasses, it's walked with `match`, and that pairing is one of the best things in modern Python.

It's also the project where the tools grow up. There's a lot of code here whose whole job is to be correct, and so you'll turn Pylance up to its strictest setting, measure how much of the code your tests really exercise, and have GitHub run every check, on three operating systems, each time you push. And then you'll install your BASIC as a command, to be run from anywhere on your machine.

| | |
|---|---|
| **You'll learn** | A syntax tree of dataclasses, walked with `match`; precedence climbing; writing an iterator class; typing in depth: generics, `Literal`, unions, `assert_never`, `TYPE_CHECKING`; `@contextmanager`; the `operator` module |
| **New tool skills** | Pylance and pyright in `strict` mode; test coverage; continuous integration with GitHub Actions; `uv build` and `uv tool install` |
| **Time** | 7 to 8 hours. It's the biggest project so far, and the final project is built on it |
| **Before you start** | [Project 16](p16-logo.md) |

## Predict

!!! question "Predict"
    ```python
    class Countdown:
        def __init__(self, start):
            self.now = start

        def __iter__(self):
            return self

        def __next__(self):
            if self.now == 0:
                raise StopIteration
            self.now -= 1
            return self.now + 1


    count = Countdown(3)
    print(list(count))
    print(list(count))
    ```

??? success "Answer"
    ```text
    [3, 2, 1]
    []
    ```

    Here's what a `for` loop has been doing since Project 1. It calls `__iter__` to get an iterator, and then calls `__next__` over and over, until that raises `StopIteration`. Any class with those two methods is an iterator. And an iterator gets used up: the second `list` finds nothing left. Generators have been writing these two methods for you since Project 6. Stage 1.

!!! question "Predict"
    ```python
    from dataclasses import dataclass


    @dataclass
    class Number:
        value: float


    @dataclass
    class Add:
        left: object
        right: object


    def work_out(tree):
        match tree:
            case Number(value):
                return value
            case Add(left, right):
                return work_out(left) + work_out(right)


    print(work_out(Add(Number(2), Add(Number(3), Number(4)))))
    ```

??? success "Answer"
    ```text
    9
    ```

    `case Add(left, right)` asks two questions at once: is this an `Add`? And if it is, what are its fields? A dataclass can be matched by position, with its fields in the order in which they were declared. A tree of dataclasses, and a recursive function with a `match` in it, are the whole of an interpreter in eighteen lines. The rest of this chapter is the same thing, made bigger. Stage 5.

!!! question "Predict"
    ```python
    print(2**3**2, 10 - 4 - 3, -(2**2), -2**2)
    ```

??? success "Answer"
    ```text
    512 3 -4 -4
    ```

    `10 - 4 - 3` is `(10 - 4) - 3`: subtraction goes from left to right. `2**3**2` is `2**(3**2)`: powers go from right to left, as they do in mathematics. And a minus sign in front holds less tightly than a power. Every language has to decide these things. Yours will decide them as Python does, and in Stage 3 you'll see that it comes down to a `+ 1`. The bug hunt is about leaving it out.

!!! question "Predict"
    ```python
    from contextlib import contextmanager


    @contextmanager
    def announced(name):
        print("Starting", name)
        try:
            yield
        finally:
            print("Finished", name)


    with announced("the sums"):
        print(1 / 0)
    ```

??? success "Answer"
    ```text
    Starting the sums
    Finished the sums
    Traceback (most recent call last):
      ...
    ZeroDivisionError: division by zero
    ```

    You've used `with` since Project 5, for files. `@contextmanager` turns a generator into something that `with` can use: whatever's before the `yield` happens on the way in, and whatever's after it on the way out, *even if the block fails*, thanks to the `finally`. It's a decorator and a generator, working together, and you've met both. Stage 6.

## BASIC in two minutes

```text
10 REM Anything after REM is a remark
20 INPUT "What's your name? ", NAME$
30 FOR I = 1 TO 3 : PRINT "Hello, "; NAME$ : NEXT
40 IF LEN(NAME$) > 8 THEN PRINT "That's a long name" ELSE GOTO 60
50 GOSUB 100
60 END
100 PRINT "(a subroutine)" : RETURN
```

A line with a number is *kept*, in order of its number, and a line without one is *done*, at once. `RUN` runs the program, `LIST` shows it, and `NEW` throws it away. A colon joins statements on a line. A variable whose name ends in `$` holds a string, and any other holds a number, and BASIC won't let you mix them up. In a `PRINT`, a semicolon means "and then, with no gap", and a comma means "move along to the next column".

## Build

```console
$ cd making
$ uv init tiny-basic
$ cd tiny-basic
$ uv add --dev pytest ruff
$ code .
```

There are no dependencies at all. Everything in this project comes from the standard library.

The pipeline has the same stages as Logo's, with one great difference: the middle of it happens once for each line, when it's typed, and not every time that it's run.

```text
'PRINT 2 + 3 * 4'                                   text
       │  tokenise                                  (Stage 1)
       ▼
PRINT  2  +  3  *  4                                tokens
       │  parse                                     (Stage 3)
       ▼
Print(Binary(Number(2), "+",                        a tree
      Binary(Number(3), "*", Number(4))))           (Stage 2)
       │  execute, as often as you like             (Stage 5)
       ▼
14
```

First, the exception. BBC BASIC's error messages were short, and said which line: `No such line at line 20`. Create `src/tiny_basic/errors.py`:

<!-- listing: projects/17-tiny-basic/src/tiny_basic/errors.py -->
```python title="src/tiny_basic/errors.py"
"""What goes wrong in a BASIC program, said as the BBC Micro would have said it."""


class BasicError(Exception):
    """A mistake in somebody's BASIC. The message is what they'll be shown."""

    def __init__(self, message: str, line: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.line = line

    def __str__(self) -> str:
        if self.line is None:
            return self.message
        return f"{self.message} at line {self.line}"
```

### Stage 1: Tokens, and an iterator of your own

The tokeniser is Logo's, with different tokens. Create `src/tiny_basic/tokens.py`:

<!-- listing: projects/17-tiny-basic/src/tiny_basic/tokens.py -->
```python title="src/tiny_basic/tokens.py"
"""Chopping one line of BASIC into tokens."""

import re
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Literal

from tiny_basic.errors import BasicError

type Kind = Literal["number", "string", "keyword", "name", "symbol"]

KEYWORDS = {
    "PRINT", "LET", "INPUT", "IF", "THEN", "ELSE", "GOTO", "GOSUB", "RETURN",
    "FOR", "TO", "STEP", "NEXT", "REPEAT", "UNTIL", "REM", "END",
    "AND", "OR", "NOT", "DIV", "MOD",
}  # fmt: skip

TOKEN = re.compile(
    r"""
      (?P<number>  \d+ (\.\d*)? | \.\d+  )
    | (?P<string>  "[^"]*"               )
    | (?P<word>    [A-Za-z][A-Za-z0-9_]* \$?  )   # COUNT, or NAME$
    | (?P<symbol>  <= | >= | <> | [-+*/^=<>(),;:]  )
    | (?P<space>   \s+                   )
    | (?P<mistake> .                     )
    """,
    re.VERBOSE,
)


@dataclass(frozen=True, slots=True)
class Token:
    kind: Kind
    text: str

    def __str__(self) -> str:
        return self.text


def tokenise(line: str) -> Iterator[Token]:
    """Yield the tokens of one line of BASIC."""
    for found in TOKEN.finditer(line):
        text = found.group()
        match found.lastgroup:
            case "space":
                pass
            case "number":
                yield Token("number", text)
            case "string":
                yield Token("string", text[1:-1])
            case "symbol":
                yield Token("symbol", text)
            case "word" if text.upper() == "REM":
                yield Token("keyword", "REM")
                yield Token("string", line[found.end() :].strip())
                return
            case "word" if text.upper() in KEYWORDS:
                yield Token("keyword", text.upper())
            case "word":
                yield Token("name", text.upper())
            case _ if text == '"':
                raise BasicError('Missing "')
            case _:
                raise BasicError(f"Mistake: I don't understand {text!r}")
```

In the pattern for symbols, `<=`, `>=` and `<>` come before the single characters. A regex tries its alternatives from left to right, and if `<` were first, `<=` would never be seen whole. `REM` is a special case: everything after it is a remark, which mustn't be tokenised at all, since it may well contain an odd number of quotation marks.

**`Literal`** is the first new piece of typing. `kind: str` would let a token be of kind `"nubmer"`, and nobody would notice until a `case "number"` quietly failed to match. `Literal["number", "string", …]` is the type of *those five strings and no others*. Pylance will now underline `Token("nubmer", "1")`, and will offer you the five choices as you type. When a string is really a choice from a short list, say so.

#### An iterator with `peek`

In Logo, you gave up on the iterator when the parser needed to look ahead, and wrote `Stream`, which was a list and a position. There's a tidier answer: an iterator that *can* look ahead. Create `src/tiny_basic/peekable.py`:

<!-- listing: projects/17-tiny-basic/src/tiny_basic/peekable.py -->
```python title="src/tiny_basic/peekable.py"
"""An iterator that lets you look at what's coming, without taking it."""

from collections.abc import Iterable, Iterator


class Peekable[T]:
    """Wrap any iterable, and add `peek`.

    It's an iterator in its own right, since it has `__iter__` and `__next__`,
    and so it works in a `for` loop, or with `next`, or with `list`.
    """

    def __init__(self, items: Iterable[T]) -> None:
        self._items: Iterator[T] = iter(items)
        self._ahead: list[T] = []  # the item that's been peeked at, if any

    def __iter__(self) -> "Peekable[T]":
        return self

    def __next__(self) -> T:
        if self._ahead:
            return self._ahead.pop()
        return next(self._items)

    def peek(self) -> T | None:
        """Return the next item without using it up, or None if there are no more."""
        if not self._ahead:
            try:
                self._ahead.append(next(self._items))
            except StopIteration:
                return None
        return self._ahead[0]
```

This is the first Predict. **`__iter__` and `__next__` are the iterator protocol**, and any object that has them works with `for`, `next`, `list`, `zip`, and everything else that takes an iterator. When a generator function won't do, because the iterator needs *extra methods* as this one does, you write the class.

`peek` takes the next item from the iterator underneath, and puts it by in `_ahead`. `__next__` hands over what's been put by, if there's anything, before it goes back for more. (It's a list, and not "the item, or `None`", so that it would still work if `None` were one of the items.) The underscores at the front are Python's way of saying "this is private: keep out", as in Project 9.

**`class Peekable[T]`** is a *generic* class. `T` stands for "whatever type the items are". Give it tokens, and it's a `Peekable[Token]`: `next` returns a `Token`, and `peek` returns `Token | None`, and Pylance knows it. Give it a string, and it's a `Peekable[str]`. You've used generic types since Project 3, every time that you wrote `list[int]`. This is how they're made. The square brackets after the name are all it takes.

```pycon
>>> from tiny_basic.peekable import Peekable
>>> letters = Peekable("abc")
>>> letters.peek(), letters.peek(), next(letters)
('a', 'a', 'a')
>>> list(letters)
['b', 'c']
```

!!! success "Checkpoint"
    Test both, in `tests/test_tokens.py`. There's a test that a `Peekable` works in a `for` loop over a generator, which no `Stream` could.

    ```console
    $ git add .
    $ git commit -m "Add a tokeniser for BASIC, and a peekable iterator"
    ```

### Stage 2: The tree

Before writing the parser, decide what it produces. `2 + 3 * 4` has a structure, which the text only hints at:

```text
        +
       / \
      2   *
         / \
        3   4
```

That's a **syntax tree**. The multiplication is lower down than the addition, and so it gets done first, and that's all that "precedence" means, once there's a tree. Brackets don't appear in a tree at all. They were only ever instructions for building it.

Each kind of node is a small, frozen dataclass. Create `src/tiny_basic/nodes.py`:

<!-- listing: projects/17-tiny-basic/src/tiny_basic/nodes.py -->
```python title="src/tiny_basic/nodes.py"
"""The tree that a line of BASIC is turned into. Every kind of node is a dataclass."""

from dataclasses import dataclass

# Expressions: the things that have a value.


@dataclass(frozen=True, slots=True)
class Number:
    value: float


@dataclass(frozen=True, slots=True)
class String:
    value: str


@dataclass(frozen=True, slots=True)
class Variable:
    name: str


@dataclass(frozen=True, slots=True)
class Unary:
    operator: str
    operand: "Expression"


@dataclass(frozen=True, slots=True)
class Binary:
    left: "Expression"
    operator: str
    right: "Expression"


@dataclass(frozen=True, slots=True)
class Call:
    name: str
    arguments: tuple["Expression", ...]


type Expression = Number | String | Variable | Unary | Binary | Call

# Statements: the things that do something.


@dataclass(frozen=True, slots=True)
class Print:
    """PRINT "X is "; X   The separators are kept, since ; and , mean different things."""

    items: tuple["Expression | str", ...]


@dataclass(frozen=True, slots=True)
class Let:
    name: str
    value: Expression


@dataclass(frozen=True, slots=True)
class Input:
    prompt: str
    name: str


@dataclass(frozen=True, slots=True)
class If:
    condition: Expression
    then: tuple["Statement", ...]
    otherwise: tuple["Statement", ...] = ()


@dataclass(frozen=True, slots=True)
class Goto:
    line: int


@dataclass(frozen=True, slots=True)
class Gosub:
    line: int


@dataclass(frozen=True, slots=True)
class Return:
    pass


@dataclass(frozen=True, slots=True)
class For:
    name: str
    start: Expression
    limit: Expression
    step: Expression = Number(1)


@dataclass(frozen=True, slots=True)
class Next:
    name: str | None = None


@dataclass(frozen=True, slots=True)
class Repeat:
    pass


@dataclass(frozen=True, slots=True)
class Until:
    condition: Expression


@dataclass(frozen=True, slots=True)
class Rem:
    text: str


@dataclass(frozen=True, slots=True)
class End:
    pass


@dataclass(frozen=True, slots=True)
class Command:
    """A statement that's a word and some values: CLS, and whatever you add later."""

    name: str
    arguments: tuple[Expression, ...]


type Statement = (
    Print | Let | Input | If | Goto | Gosub | Return | For | Next
    | Repeat | Until | Rem | End | Command
)  # fmt: skip
```

It's a long file with no logic in it whatever. It's a *description* of BASIC: these are the kinds of expression that there are, these are the kinds of statement, and this is what each is made of.

**`type Expression = Number | String | Variable | Unary | Binary | Call`** is a **union**: an expression is any one of those six. `Binary` has two `Expression`s inside it, and so the types refer to each other, round in a circle, which is why some of the hints are in quotation marks. The tree in the picture above is `Binary(Number(2), "+", Binary(Number(3), "*", Number(4)))`.

Why not a base class, `class Expression`, with `Number` and the rest as its children, in the manner of Project 15? You could. But there's no code that they'd share, which was the test. And there's a better reason to come: a union is a *closed* list, and in Stage 5 Pylance will use that to tell you when you've forgotten a case.

Frozen dataclasses compare by value, and so the parser's tests can build the tree that they expect, and use `==`.

!!! success "Checkpoint"
    ```console
    $ git add .
    $ git commit -m "Describe BASIC's syntax tree as dataclasses"
    ```

### Stage 3: The parser

In Logo there was a method for each level of precedence: `expression`, `sum`, `product`, `atom`. BASIC has six levels. Six methods, all alike but for the list of signs, would be tedious, and adding an operator would mean surgery. There's a technique that does any number of levels with **one method and a table**, called *precedence climbing*.

Create `src/tiny_basic/parser.py`. Here's the top of it, as far as expressions:

<!-- listing: projects/17-tiny-basic/src/tiny_basic/parser.py -->
```python title="src/tiny_basic/parser.py"
"""Turning the tokens of a line into a tree."""

from tiny_basic import nodes
from tiny_basic.errors import BasicError
from tiny_basic.nodes import Expression, Statement
from tiny_basic.peekable import Peekable
from tiny_basic.registry import COMMANDS, FUNCTIONS
from tiny_basic.tokens import Token, tokenise

# The bigger the number, the tighter the operator holds on to what's beside it.
PRECEDENCE = {
    "OR": 1,
    "AND": 2,
    "=": 4, "<>": 4, "<": 4, ">": 4, "<=": 4, ">=": 4,
    "+": 5, "-": 5,
    "*": 6, "/": 6, "DIV": 6, "MOD": 6,
    "^": 8,
}  # fmt: skip
NOT = 3
NEGATIVE = 7
RIGHT_TO_LEFT = {"^"}


class Parser:
    def __init__(self, text: str) -> None:
        self.tokens = Peekable(tokenise(text))

    # Helpers, for looking at the next token and for insisting on one.

    def next_is(self, *texts: str) -> bool:
        token = self.tokens.peek()
        return token is not None and token.kind != "string" and token.text in texts

    def take(self, text: str) -> bool:
        """Use up the next token if it's this one, and say whether it was."""
        if self.next_is(text):
            next(self.tokens)
            return True
        return False

    def expect(self, text: str) -> None:
        if not self.take(text):
            raise BasicError(f"Missing {text}")

    def name(self) -> str:
        match next(self.tokens, None):
            case Token("name", name):
                return name
            case _:
                raise BasicError("Syntax error: there should be a variable here")

    def line_number(self) -> int:
        match next(self.tokens, None):
            case Token("number", text) if text.isdecimal():
                return int(text)
            case _:
                raise BasicError("Syntax error: there should be a line number here")

    # Expressions, by precedence climbing.

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
            tighter = precedence if token.text in RIGHT_TO_LEFT else precedence + 1
            left = nodes.Binary(left, token.text, self.expression(tighter))

    def operand(self) -> Expression:
        match next(self.tokens, None):
            case Token("number", text):
                return nodes.Number(float(text))
            case Token("string", text):
                return nodes.String(text)
            case Token("symbol", "-"):
                return nodes.Unary("-", self.expression(NEGATIVE))
            case Token("keyword", "NOT"):
                return nodes.Unary("NOT", self.expression(NOT))
            case Token("symbol", "("):
                inside = self.expression()
                self.expect(")")
                return inside
            case Token("name", name) if name in FUNCTIONS:
                return nodes.Call(name, self.arguments(brackets=True))
            case Token("name", name):
                return nodes.Variable(name)
            case None:
                raise BasicError("Syntax error: the line stops too soon")
            case token:
                raise BasicError(f"Syntax error: I didn't expect {token}")

    def arguments(self, brackets: bool) -> tuple[Expression, ...]:
        """Parse some expressions with commas between, in brackets or not."""
        if brackets and not self.take("("):
            return ()
        found: list[Expression] = []
        if brackets or not (self.tokens.peek() is None or self.next_is(":", "ELSE")):
            found.append(self.expression())
            while self.take(","):
                found.append(self.expression())
        if brackets:
            self.expect(")")
        return tuple(found)
```

(The import of `COMMANDS` and `FUNCTIONS` is for Stage 4's `registry.py`. Create that file first, if you'd like Pylance to stop complaining.)

`PRECEDENCE` gives every operator a number, and the bigger the number, the tighter it holds. `expression(minimum)` means: *parse an expression in which every operator has a precedence of `minimum` or more*. Follow `2 + 3 * 4` through it:

1. `expression(1)` reads the operand `2`. Next comes `+`, of precedence 5, which is 1 or more, and so it's taken.
2. Now for the right-hand side of the `+`. It calls `expression(6)`: "give me an expression, and stop at anything that holds *no tighter than I do*".
3. That inner call reads `3`, and sees `*`, of precedence 6. That's enough, and so it takes it, and reads `4`. It returns `3 * 4`, as one node.
4. Back in the outer call, `left` becomes `2 + (3 * 4)`.

Had it been `2 * 3 + 4`, the inner call, `expression(7)`, would have read `3`, seen `+` at only 5, and stopped. The outer loop would have gone round again, and made `(2 * 3) + 4`.

**The `+ 1` is what makes operators go from left to right.** In `10 - 4 - 3`, the right-hand side of the first `-` is parsed with a minimum of 6, and so the second `-`, at 5, isn't swallowed by it. It's left for the outer loop, which makes `(10 - 4) - 3`. For `^`, which goes from right to left, there's no `+ 1`. The right-hand side may take another `^`, and so `2 ^ 3 ^ 2` is `2 ^ (3 ^ 2)`. That was the third Predict, and it's the bug hunt.

To add an operator to this language, you add a line to the table.

`operand` is Logo's `atom`. The token patterns are `Token("number", text)`, by position, since `Token` is a dataclass. A minus sign parses its operand with a minimum of 7, which is tighter than `*`, and looser than `^`, and so `-A ^ 2` is `-(A ^ 2)`, as in Python. (BBC BASIC made it `(-A) ^ 2`. Nobody ever thanked it.)

The rest of the file is statements:

<!-- listing: projects/17-tiny-basic/src/tiny_basic/parser.py -->
```python title="src/tiny_basic/parser.py"
    # Statements.

    def statement(self) -> Statement:
        match next(self.tokens, None):
            case Token("keyword", "PRINT"):
                return self.print_()
            case Token("keyword", "LET"):
                return self.let(self.name())
            case Token("name", name) if self.next_is("="):
                return self.let(name)
            case Token("name", name) if name in COMMANDS:
                return nodes.Command(name, self.arguments(brackets=False))
            case Token("keyword", "INPUT"):
                return self.input_()
            case Token("keyword", "IF"):
                return self.if_()
            case Token("keyword", "GOTO"):
                return nodes.Goto(self.line_number())
            case Token("keyword", "GOSUB"):
                return nodes.Gosub(self.line_number())
            case Token("keyword", "RETURN"):
                return nodes.Return()
            case Token("keyword", "FOR"):
                return self.for_()
            case Token("keyword", "NEXT"):
                return self.next_()
            case Token("keyword", "REPEAT"):
                return nodes.Repeat()
            case Token("keyword", "UNTIL"):
                return nodes.Until(self.expression())
            case Token("keyword", "REM"):
                return nodes.Rem(str(next(self.tokens)))
            case Token("keyword", "END"):
                return nodes.End()
            case None:
                raise BasicError("Syntax error: there's a statement missing")
            case token:
                raise BasicError(f"Mistake: I don't know what to do with {token}")

    def next_(self) -> nodes.Next:
        token = self.tokens.peek()
        if token is not None and token.kind == "name":
            return nodes.Next(self.name())
        return nodes.Next()

    def let(self, name: str) -> nodes.Let:
        self.expect("=")
        return nodes.Let(name, self.expression())

    def print_(self) -> nodes.Print:
        items: list[Expression | str] = []
        while not (self.tokens.peek() is None or self.next_is(":", "ELSE")):
            if self.next_is(";", ","):
                items.append(str(next(self.tokens)))
            else:
                items.append(self.expression())
        return nodes.Print(tuple(items))

    def input_(self) -> nodes.Input:
        prompt = "? "
        match self.tokens.peek():
            case Token("string", text):
                next(self.tokens)
                prompt = text
                if not (self.take(",") or self.take(";")):
                    raise BasicError("Missing ,")
            case _:
                pass
        return nodes.Input(prompt, self.name())

    def if_(self) -> nodes.If:
        condition = self.expression()
        self.expect("THEN")
        then = self.branch()
        otherwise = self.branch() if self.take("ELSE") else ()
        return nodes.If(condition, then, otherwise)

    def branch(self) -> tuple[Statement, ...]:
        """Parse what follows THEN or ELSE: a line number, or some statements."""
        token = self.tokens.peek()
        if token is not None and token.kind == "number":
            return (nodes.Goto(self.line_number()),)
        found = [self.statement()]
        while self.take(":"):
            found.append(self.statement())
        return tuple(found)

    def for_(self) -> nodes.For:
        name = self.name()
        self.expect("=")
        start = self.expression()
        self.expect("TO")
        limit = self.expression()
        step = self.expression() if self.take("STEP") else nodes.Number(1)
        return nodes.For(name, start, limit, step)

    def statements(self) -> tuple[Statement, ...]:
        """Parse a whole line: some statements, with colons between them."""
        found = [self.statement()]
        while self.take(":"):
            found.append(self.statement())
        leftover = self.tokens.peek()
        if leftover is not None:
            raise BasicError(f"Syntax error: I didn't expect {leftover}")
        return tuple(found)


def parse(text: str) -> tuple[Statement, ...]:
    """Turn the text of a line, without its line number, into statements."""
    return Parser(text).statements()
```

`statement` is one `match` on the first token of the statement, and that tells you everything. BASIC was designed to be parsed in this way, by a program that had to fit into a few kilobytes: every statement begins with a keyword which says what it is. The one exception is assignment, where `LET` may be left out, and so `X = 1` has to be recognised by the `=` that follows the name. That's what `peek` was for.

`IF` takes everything else on the line, up to an `ELSE`. `branch` allows a bare line number after `THEN`, which is `IF X > 9 THEN 200`, the most BASIC of all idioms.

`statements` parses a whole line, and then checks that there's nothing left over. **Every line is parsed as it's typed**, and so a mistake in line 500 is reported when you type line 500, and not an hour later, when the program at last gets there. That was one of the things that made BBC BASIC pleasant, and it comes free with the design.

The parser's tests are the clearest in the project: some text goes in, and a tree comes out. `tests/test_parser.py`:

<!-- listing: projects/17-tiny-basic/tests/test_parser.py -->
```python title="tests/test_parser.py"
def tree(text: str) -> nodes.Expression:
    return Parser(text).expression()


def test_multiplying_comes_before_adding():
    assert tree("2 + 3 * 4") == Binary(
        Number(2), "+", Binary(Number(3), "*", Number(4))
    )


def test_brackets_come_before_everything():
    assert tree("(2 + 3) * 4") == Binary(
        Binary(Number(2), "+", Number(3)), "*", Number(4)
    )


def test_taking_away_goes_from_left_to_right():
    assert tree("10 - 4 - 3") == Binary(
        Binary(Number(10), "-", Number(4)), "-", Number(3)
    )


def test_powers_go_from_right_to_left():
    assert tree("2 ^ 3 ^ 2") == Binary(
        Number(2), "^", Binary(Number(3), "^", Number(2))
    )
# ...
def test_if_takes_the_rest_of_the_line_and_a_bare_number_is_a_goto():
    assert parse("IF X THEN PRINT 1 : PRINT 2 ELSE 300") == (
        nodes.If(
            Variable("X"),
            (nodes.Print((Number(1),)), nodes.Print((Number(2),))),
            (nodes.Goto(300),),
        ),
    )
```

!!! success "Checkpoint"
    ```console
    $ git add .
    $ git commit -m "Parse BASIC into a tree, by precedence climbing"
    ```

### Stage 4: Values, and the built-in functions

BASIC has numbers and strings, and won't mix them: `"A" + 1` is a `Type mismatch`. Create `src/tiny_basic/values.py`:

<!-- listing: projects/17-tiny-basic/src/tiny_basic/values.py -->
```python title="src/tiny_basic/values.py"
"""BASIC has two kinds of value, numbers and strings, and is strict about which is which."""

import math
import operator
from collections.abc import Callable

from tiny_basic.errors import BasicError

type Value = float | str

TRUE, FALSE = -1.0, 0.0  # as on the BBC Micro: every bit set, and none


def number(value: Value) -> float:
    """Insist on a number."""
    if isinstance(value, str):
        raise BasicError("Type mismatch")
    return value


def string(value: Value) -> str:
    """Insist on a string."""
    if not isinstance(value, str):
        raise BasicError("Type mismatch")
    return value


def show(value: Value) -> str:
    """Return a value as PRINT would show it: whole numbers have no decimal point."""
    if isinstance(value, str):
        return value
    if value == int(value) and abs(value) < 1e15:
        return str(int(value))
    return f"{value:.9g}"


COMPARISONS: dict[str, Callable[[Value, Value], bool]] = {
    "=": operator.eq,
    "<>": operator.ne,
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge,
}
ARITHMETIC: dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": lambda x, y: x / y,  # operator.truediv would do, but its hints are vague
    "^": math.pow,
    "DIV": lambda x, y: int(x / y),
    "MOD": lambda x, y: math.fmod(int(x), int(y)),
    "AND": lambda x, y: int(x) & int(y),
    "OR": lambda x, y: int(x) | int(y),
}


def combine(left: Value, sign: str, right: Value) -> Value:
    """Work out `left sign right`, for any of BASIC's operators."""
    if sign in COMPARISONS:
        if isinstance(left, str) != isinstance(right, str):
            raise BasicError("Type mismatch")
        return TRUE if COMPARISONS[sign](left, right) else FALSE
    if sign == "+" and isinstance(left, str) and isinstance(right, str):
        return left + right
    x, y = number(left), number(right)
    if y == 0 and sign in ("/", "DIV", "MOD"):
        raise BasicError("Division by zero")
    try:
        return float(ARITHMETIC[sign](x, y))
    except OverflowError:
        raise BasicError("Too big") from None
    except ValueError:
        raise BasicError("-ve root") from None
```

**The `operator` module** has a function for every one of Python's operators: `operator.add(a, b)` is `a + b`. They exist so that an operator can be put into a variable, passed about, or, as here, kept in a dictionary. `combine` looks the sign up, and calls what it finds. The alternative is a `match` with sixteen cases, all nearly alike, and this was that, in the first draft. A table that maps names to functions is one of Python's handiest idioms. The ones that the module hasn't got are little `lambda`s.

!!! note "Under the bonnet"
    In BBC BASIC, true is −1, and false is 0. It looks perverse, and it's rather clever. In binary, −1 has *every bit set*. So `AND`, `OR` and `NOT` could work on the bits of whole numbers, as `6 AND 3` is 2, and *the very same* operators did for logic, with no special cases at all. `NOT 0` is −1, and `NOT -1` is 0. Yours behaves in the same way, and Project 19 has more to say about bits.

The functions are kept by a registry, which is Logo's, with better type hints. Create `src/tiny_basic/registry.py`:

<!-- listing: projects/17-tiny-basic/src/tiny_basic/registry.py -->
```python title="src/tiny_basic/registry.py"
"""BASIC's built-in functions, and the simple commands, kept on two lists by decorators."""

import inspect
from collections.abc import Callable
from dataclasses import dataclass

from tiny_basic.values import Value


@dataclass(frozen=True, slots=True)
class Builtin:
    name: str
    function: Callable[..., Value | None]
    arguments: int


FUNCTIONS: dict[str, Builtin] = {}
COMMANDS: dict[str, Builtin] = {}


def function[F: Callable[..., Value]](name: str) -> Callable[[F], F]:
    """List a Python function as a BASIC function, such as INT or LEFT$."""

    def register(python: F) -> F:
        wanted = len(inspect.signature(python).parameters)
        FUNCTIONS[name] = Builtin(name, python, wanted)
        return python

    return register


def command[F: Callable[..., None]](name: str) -> Callable[[F], F]:
    """List a Python function as a BASIC command. Its first parameter is the machine."""

    def register(python: F) -> F:
        wanted = len(inspect.signature(python).parameters) - 1
        COMMANDS[name] = Builtin(name, python, wanted)
        return python

    return register
```

**`def function[F: Callable[..., Value]](name: str) -> Callable[[F], F]`** is a generic *function*, and it answers a question that Logo's registry dodged. What's the type of a decorator that hands a function back unchanged? "It takes some function of type `F`, and returns that same `F`." The `[F: …]` declares the type variable, and the part after the colon is a *bound*: `F` can be any type, provided that it's a callable which returns a `Value`. Without this, a decorated function would lose its type, and Pylance would know nothing about `rnd` or `left`. With it, they're exactly what they were.

And `src/tiny_basic/functions.py`. Here's a sample of it:

<!-- listing: projects/17-tiny-basic/src/tiny_basic/functions.py -->
```python title="src/tiny_basic/functions.py"
"""BASIC's built-in functions and simple commands. Importing this module lists them."""

import math
import random
import time
from typing import TYPE_CHECKING

from tiny_basic.errors import BasicError
from tiny_basic.registry import command, function
from tiny_basic.values import number, show, string

if TYPE_CHECKING:
    from tiny_basic.machine import Machine

STARTED = time.monotonic()


@function("RND")
def rnd(limit: float) -> float:
    """RND(6) is a whole number from 1 to 6. RND(1) is a fraction from 0 up to 1."""
    if number(limit) <= 1:
        return random.random()
    return float(random.randint(1, int(limit)))
# ...
@function("MID$")
def mid(text: str, start: float, count: float) -> str:
    first = max(int(number(start)) - 1, 0)
    return string(text)[first : first + int(number(count))]
# ...
@command("CLS")
def cls(machine: "Machine") -> None:
    machine.console.write("\x1b[2J\x1b[H")
```

The others are `INT`, `ABS`, `SGN`, `SQR`, `SIN`, `COS`, `PI`, `TIME`, `LEN`, `LEFT$`, `RIGHT$`, `STRING$`, `CHR$`, `ASC`, `STR$` and `VAL`. Each is two or three lines. Write them from their names, with the BBC's user guide or the repository to hand. `MID$` counts from 1, as BASIC does. `VAL("pardon?")` is 0, and not an error.

**`if TYPE_CHECKING:`** deals with a problem that's been waiting for you. `cls` needs to say that its parameter is a `Machine`. But `machine.py`, in the next stage, imports *this* module. If each imports the other, then whichever goes first finds the other half-made, and Python raises an `ImportError` about a "partially initialized module". That's a *circular import*. The import here is only wanted for a type hint, and hints aren't needed when the program runs. `TYPE_CHECKING` is a constant that's `False` when Python runs your program, and that type checkers treat as `True`. So Pylance sees the import, and Python never performs it. The hint has to go in quotation marks, since, as far as Python is concerned, the name doesn't exist.

!!! success "Checkpoint"
    ```console
    $ git add .
    $ git commit -m "Add values, operators, and the built-in functions"
    ```

### Stage 5: The machine

Create `src/tiny_basic/machine.py`. First, the housekeeping: a program is a dictionary from line numbers to text, and another from line numbers to trees.

<!-- listing: projects/17-tiny-basic/src/tiny_basic/machine.py -->
```python title="src/tiny_basic/machine.py"
"""The machine that holds a BASIC program, and runs it."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, assert_never

from tiny_basic import functions, nodes
from tiny_basic.errors import BasicError
from tiny_basic.nodes import Expression, Statement
from tiny_basic.parser import parse
from tiny_basic.registry import COMMANDS, FUNCTIONS
from tiny_basic.values import Value, combine, number, show

__all__ = ["Console", "Machine", "functions"]

NUMBERED = re.compile(r"\s*(\d+) ?(.*)")
ZONE = 10  # a comma in a PRINT moves on to the next column that's a multiple of this


class Console(Protocol):
    """Where PRINT goes to, and where INPUT comes from."""

    def write(self, text: str) -> None: ...

    def read(self, prompt: str) -> str: ...


@dataclass(slots=True)
class ForLoop:
    name: str
    limit: float
    step: float
    body: int  # the step to go back to


@dataclass(slots=True)
class RepeatLoop:
    body: int


class Machine:
    def __init__(self, console: Console) -> None:
        self.console = console
        self.source: dict[int, str] = {}
        self.program: dict[int, tuple[Statement, ...]] = {}
        self.variables: dict[str, Value] = {}
        self.column = 0
        # While a program is running:
        self.steps: list[tuple[int | None, Statement]] = []
        self.starts: dict[int, int] = {}
        self.pc = 0
        self.loops: list[ForLoop | RepeatLoop] = []
        self.returns: list[int] = []

    def enter(self, text: str) -> None:
        """Deal with a line that's been typed: keep it, if it has a number, or do it."""
        if found := NUMBERED.fullmatch(text):
            self.store(int(found[1]), found[2])
            return
        word, _, rest = text.strip().partition(" ")
        match word.upper():
            case "":
                pass
            case "RUN":
                self.run()
            case "LIST":
                for line in self.listing():
                    self.write(line + "\n")
            case "NEW":
                self.new()
            case "SAVE":
                self.save(Path(rest.strip(' "')).with_suffix(".bas"))
            case "LOAD":
                self.load_file(Path(rest.strip(' "')).with_suffix(".bas"))
            case _:
                self.run(parse(text))

    # Keeping the program.

    def store(self, number: int, text: str) -> None:
        """Keep a numbered line, or, if there's nothing on it, throw it away."""
        if not text.strip():
            self.source.pop(number, None)
            self.program.pop(number, None)
            return
        self.program[number] = parse(text)
        self.source[number] = text.strip()

    def listing(self) -> list[str]:
        return [f"{number:5} {self.source[number]}" for number in sorted(self.source)]

    def new(self) -> None:
        self.source.clear()
        self.program.clear()
        self.variables.clear()

    def save(self, path: Path) -> None:
        lines = [f"{number} {self.source[number]}" for number in sorted(self.source)]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def load_file(self, path: Path) -> None:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            raise BasicError(f"File not found: {path}") from None
        self.new()
        for line in lines:
            if not NUMBERED.fullmatch(line):
                raise BasicError(f"{path} has a line with no number: {line!r}")
            self.enter(line)
```

**`Console` is a `Protocol`**, as Logo's `Canvas` was: somewhere to write, and somewhere to read from. In this project it's the terminal. In tests it's a script. In the final project it'll be a Pygame window that looks like a BBC Micro's screen, and nothing in this file will change.

`enter` is what happens when a line is typed. The regular expression picks a line number off the front, if there is one. `store` parses the line *before* it keeps it, and so a line with a mistake in it is refused, and whatever was there before is left alone. A line number with nothing after it deletes the line, as it always did.

#### GOTO, and the program counter

Logo ran lists inside lists, and Python's own call stack kept track of where it had got to. BASIC can't work like that, since `GOTO` can jump from anywhere to anywhere. So the machine works as a real processor does. The program is laid out as **one flat list of steps**, and there's a **program counter**, `pc`, which is the number of the next step. To run a step is to fetch it, add one to `pc`, and execute it. And then `GOTO` is nothing more than an assignment to `pc`.

<!-- listing: projects/17-tiny-basic/src/tiny_basic/machine.py -->
```python title="src/tiny_basic/machine.py"
    # Running it.

    def load(self, immediate: tuple[Statement, ...] = ()) -> None:
        """Lay the program out as a flat list of steps, ready to be run.

        After the program comes an END, and after that, any statements that were
        typed without a line number. They're where the machine starts, unless
        there aren't any, and then it starts at the top.
        """
        self.steps = []
        self.starts = {}
        for line in sorted(self.program):
            self.starts[line] = len(self.steps)
            self.steps += [(line, statement) for statement in self.program[line]]
        self.steps.append((None, nodes.End()))
        self.pc = len(self.steps) if immediate else 0
        self.steps += [(None, statement) for statement in immediate]
        self.loops = []
        self.returns = []

    def step(self) -> bool:
        """Do one statement. Return False when there's nothing left to do."""
        if self.pc >= len(self.steps):
            return False
        line, statement = self.steps[self.pc]
        self.pc += 1
        try:
            self.execute(statement)
        except BasicError as error:
            self.pc = len(self.steps)
            raise BasicError(error.message, line) from None
        except (KeyboardInterrupt, EOFError):
            self.pc = len(self.steps)
            raise BasicError("Escape", line) from None
        return True

    def run(self, immediate: tuple[Statement, ...] = ()) -> None:
        if not immediate:
            self.variables.clear()
        self.load(immediate)
        while self.step():
            pass

    def jump(self, line: int) -> None:
        if line not in self.starts:
            raise BasicError("No such line")
        self.pc = self.starts[line]
```

`load` flattens the program, and notes where each line starts. After the program goes an `END`, and after that go any statements that were typed without a line number, which is where the machine starts, if there are any. So `PRINT 2 + 2` at the prompt, and `RUN`, and even `GOTO 50` at the prompt, are all the same operation.

**`step` does one statement, and says whether there's more to do.** `run` is a `while` loop round it. It would have been shorter to put the loop inside, and it's done this way with the final project in mind. A program that's running in a window has to share the processor with the window, and a machine that can be stepped can be given a thousand steps in each frame.

`step` is also where an error acquires its line number, and where ++ctrl+c++, which is Python's `KeyboardInterrupt`, becomes BASIC's `Escape at line 20`, which is how you stop `20 GOTO 10`.

#### Walking the tree

<!-- listing: projects/17-tiny-basic/src/tiny_basic/machine.py -->
```python title="src/tiny_basic/machine.py"
    def execute(self, statement: Statement) -> None:
        match statement:
            case nodes.Rem():
                pass
            case nodes.Print(items):
                self.print_(items)
            case nodes.Let(name, value):
                self.assign(name, self.evaluate(value))
            case nodes.Input(prompt, name):
                text = self.console.read(prompt)
                self.column = 0
                self.assign(name, text if name.endswith("$") else functions.val(text))
            case nodes.If(condition, then, otherwise):
                branch = then if number(self.evaluate(condition)) else otherwise
                for inner in branch:
                    self.execute(inner)
            case nodes.Goto(line):
                self.jump(line)
            case nodes.Gosub(line):
                self.returns.append(self.pc)
                self.jump(line)
            case nodes.Return():
                if not self.returns:
                    raise BasicError("No GOSUB")
                self.pc = self.returns.pop()
            case nodes.For(name, start, limit, step):
                self.assign(name, number(self.evaluate(start)))
                loop = ForLoop(
                    name,
                    number(self.evaluate(limit)),
                    number(self.evaluate(step)),
                    self.pc,
                )
                self.loops.append(loop)
            case nodes.Next(name):
                self.next_(name)
            case nodes.Repeat():
                self.loops.append(RepeatLoop(self.pc))
            case nodes.Until(condition):
                if not self.loops or not isinstance(self.loops[-1], RepeatLoop):
                    raise BasicError("No REPEAT")
                if number(self.evaluate(condition)):
                    self.loops.pop()
                else:
                    self.pc = self.loops[-1].body
            case nodes.End():
                self.pc = len(self.steps)
            case nodes.Command(name, arguments):
                builtin = COMMANDS[name]
                if len(arguments) != builtin.arguments:
                    raise BasicError(f"Wrong number of values for {name}")
                builtin.function(self, *(self.evaluate(value) for value in arguments))
            case _:  # pragma: no cover
                assert_never(statement)
```

This is the second Predict, at full size. **Each `case` names a kind of node, and takes it apart in the same breath**: `case nodes.For(name, start, limit, step)` checks the type and unpacks four fields in one line. Compare it with what it replaces: a chain of `isinstance` checks, with `statement.name` and `statement.limit` all the way down. And compare it with the object-oriented way, which is an `execute` method on every node class. That works too, and it scatters the interpreter over twenty classes. Here the nodes are plain data, and everything about *running* them is in one place. A second way of walking the tree, such as a pretty-printer, or a compiler, would be another function beside this one, and the nodes wouldn't change.

**The loops don't nest in the tree.** `FOR` and `NEXT` are separate statements, which may be lines apart. So `FOR` puts a note on a stack, to say which variable it is, the limit, the step, and *the step number to come back to*. `NEXT` looks at the top of the stack, adds the step, and either sets `pc` back, or takes the note off and carries on. `REPEAT` and `UNTIL` do the same, and `GOSUB` and `RETURN` have a stack of their own. There are three little stacks, doing between them what Python's call stack did for Logo.

(A `FOR` loop in BBC BASIC always goes round once, even `FOR I = 5 TO 1`, since the test is at the `NEXT`. Yours does the same, and there's a test to prove that it's deliberate.)

#### `assert_never`, and the point of a closed union

Look at the last case: `case _: assert_never(statement)`. At run time, `assert_never` raises an error if it's ever reached. Its real work is done before then. A type checker knows that `statement` is a `Statement`, which is one of fourteen classes. After each `case`, it crosses one off. When it reaches the `case _`, there ought to be none left, and the type of `statement` is `Never`, which is the type that has no values. `assert_never` accepts a `Never`, and nothing else.

Now suppose that next month you add `While` to the language. You write the dataclass, and add it to the union in `nodes.py`. At once, **Pylance underlines `assert_never(statement)`**, with a message that names `While`, because there's now a kind of statement which the `match` doesn't handle. It does the same in `evaluate`, for expressions. The type checker takes you to every place that needs to change. That's the payoff for describing the tree as a closed union, and it's something that the base class of Project 15 can't do for you, since anybody might add a subclass anywhere.

<!-- listing: projects/17-tiny-basic/src/tiny_basic/machine.py -->
```python title="src/tiny_basic/machine.py"
    def next_(self, name: str | None) -> None:
        if not self.loops or not isinstance(self.loops[-1], ForLoop):
            raise BasicError("No FOR")
        loop = self.loops[-1]
        if name not in (None, loop.name):
            raise BasicError(f"Can't match FOR: this is the loop for {loop.name}")
        value = number(self.variables[loop.name]) + loop.step
        self.variables[loop.name] = value
        finished = value > loop.limit if loop.step >= 0 else value < loop.limit
        if finished:
            self.loops.pop()
        else:
            self.pc = loop.body

    def assign(self, name: str, value: Value) -> None:
        if name.endswith("$") != isinstance(value, str):
            raise BasicError("Type mismatch")
        self.variables[name] = value

    def print_(self, items: tuple[Expression | str, ...]) -> None:
        for item in items:
            if item == ",":
                self.write(" " * (ZONE - self.column % ZONE))
            elif not isinstance(item, str):
                self.write(show(self.evaluate(item)))
        if not items or items[-1] not in (";", ","):
            self.write("\n")

    def write(self, text: str) -> None:
        self.console.write(text)
        self.column = 0 if text.endswith("\n") else self.column + len(text)

    # Working things out.

    def evaluate(self, expression: Expression) -> Value:
        match expression:
            case nodes.Number(value) | nodes.String(value):
                return value
            case nodes.Variable(name):
                if name not in self.variables:
                    raise BasicError(f"No such variable: {name}")
                return self.variables[name]
            case nodes.Unary("-", operand):
                return -number(self.evaluate(operand))
            case nodes.Unary(_, operand):
                return float(~int(number(self.evaluate(operand))))
            case nodes.Binary(left, operator, right):
                return combine(self.evaluate(left), operator, self.evaluate(right))
            case nodes.Call(name, arguments):
                builtin = FUNCTIONS[name]
                if len(arguments) != builtin.arguments:
                    raise BasicError(f"Wrong number of values for {name}")
                values = [self.evaluate(value) for value in arguments]
                result = builtin.function(*values)
                assert result is not None
                return result
            case _:  # pragma: no cover
                assert_never(expression)
```

`evaluate` is `execute`'s twin, for expressions, and it's the second Predict almost word for word. `case nodes.Number(value) | nodes.String(value)` handles two kinds of node in one case, which is allowed when both alternatives bind the same names. `case nodes.Unary("-", operand)` matches on a *value* in one field while capturing the other.

Finally, `src/tiny_basic/__init__.py` exports the three names that anybody using the package will want:

<!-- listing: projects/17-tiny-basic/src/tiny_basic/__init__.py -->
```python title="src/tiny_basic/__init__.py"
"""A small BASIC, in the manner of the BBC Micro's."""

from tiny_basic.errors import BasicError
from tiny_basic.machine import Console, Machine

__all__ = ["BasicError", "Console", "Machine"]
```

The tests need a console that isn't a terminal. `tests/conftest.py` has one, and a helper that types a program in and runs it:

<!-- listing: projects/17-tiny-basic/tests/conftest.py -->
```python title="tests/conftest.py"
import pytest

from tiny_basic import Machine


class Script:
    """A console for tests: it keeps what's written, and answers INPUT from a list."""

    def __init__(self, *replies: str) -> None:
        self.written: list[str] = []
        self.replies = list(replies)

    def write(self, text: str) -> None:
        self.written.append(text)

    def read(self, prompt: str) -> str:
        self.written.append(prompt)
        if not self.replies:
            raise EOFError
        return self.replies.pop(0)

    @property
    def text(self) -> str:
        return "".join(self.written)


@pytest.fixture
def console() -> Script:
    return Script()


@pytest.fixture
def machine(console: Script) -> Machine:
    return Machine(console)


def run(machine: Machine, program: str) -> str:
    """Type a program in, run it, and return everything that it printed."""
    for line in program.strip().splitlines():
        machine.enter(line.strip())
    machine.enter("RUN")
    console = machine.console
    assert isinstance(console, Script)
    return console.text
```

`Script` has a `write` and a `read`, and so it's a `Console`. With it, the tests are BASIC programs, and what they ought to print. `tests/test_machine.py`:

<!-- listing: projects/17-tiny-basic/tests/test_machine.py -->
```python title="tests/test_machine.py"
def test_the_oldest_program_there_is(machine):
    assert run(machine, '10 PRINT "HELLO"') == "HELLO\n"
# ...
def test_for_next_with_a_step_and_a_loop_inside_a_loop(machine):
    assert (
        run(
            machine,
            """
        10 FOR I = 1 TO 2
        20   FOR J = 10 TO 0 STEP -5 : PRINT I * J; " "; : NEXT J
        30 NEXT
        40 PRINT "done"; I
    """,
        )
        == "10 5 0 20 10 0 done3\n"
    )


def test_a_for_loop_always_goes_round_once_as_on_the_bbc(machine):
    assert run(machine, '10 FOR I = 5 TO 1 : PRINT "once" : NEXT') == "once\n"
# ...
def test_goto_gosub_and_end(machine):
    assert (
        run(
            machine,
            """
        10 GOSUB 100
        20 GOSUB 100
        30 GOTO 50
        40 PRINT "never"
        50 PRINT "end"
        60 END
        100 PRINT "sub ";
        110 RETURN
    """,
        )
        == "sub sub end\n"
    )
# ...
def test_the_machine_can_be_stepped_one_statement_at_a_time(machine):
    machine.enter("10 PRINT 1 : PRINT 2")
    machine.enter("20 PRINT 3")
    machine.load()
    assert machine.step()
    assert machine.console.text == "1\n"
    assert machine.step()
    assert machine.step()
    assert machine.step()  # the END that's put after every program
    assert not machine.step()
    assert machine.console.text == "1\n2\n3\n"
```

There are also a table of 27 sums with their answers, and a table of 19 programs that go wrong, each with the complaint that it ought to get.

!!! success "Checkpoint"
    ```console
    $ git add .
    $ git commit -m "Add the machine: a program counter, three stacks, and a tree walker"
    ```

### Stage 6: The prompt, and a context manager

Create `src/tiny_basic/repl.py`:

<!-- listing: projects/17-tiny-basic/src/tiny_basic/repl.py -->
```python title="src/tiny_basic/repl.py"
"""BASIC at a prompt, in the terminal, or running a program from a file."""

import argparse
import sys
import time
from collections.abc import Generator
from contextlib import contextmanager, nullcontext
from pathlib import Path

from tiny_basic.errors import BasicError
from tiny_basic.machine import Machine

BANNER = "Tiny BASIC\n"


class Terminal:
    """A console that's the terminal that Python is running in."""

    def write(self, text: str) -> None:
        print(text, end="", flush=True)

    def read(self, prompt: str) -> str:
        return input(prompt)


@contextmanager
def timed(label: str) -> Generator[None]:
    """Time whatever happens inside the `with`, and say how long it took."""
    started = time.perf_counter()
    try:
        yield
    finally:
        seconds = time.perf_counter() - started
        print(f"[{label}: {seconds:.3f} seconds]", file=sys.stderr)


def converse(machine: Machine) -> None:
    """Take lines from the keyboard until there are no more."""
    print(BANNER)
    while True:
        try:
            line = input(">")
        except EOFError:
            print()
            return
        if line.strip().upper() == "QUIT":
            return
        try:
            machine.enter(line)
        except BasicError as error:
            print(f"\n{error}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("program", nargs="?", type=Path, help="a .bas file to run")
    parser.add_argument("--time", action="store_true", help="say how long it took")
    args = parser.parse_args()

    machine = Machine(Terminal())
    if args.program is None:
        converse(machine)
        return

    try:
        with timed("loading") if args.time else nullcontext():
            machine.load_file(args.program)
        with timed("running") if args.time else nullcontext():
            machine.run()
    except BasicError as error:
        raise SystemExit(f"\n{error}") from None
```

Set the command in `pyproject.toml` to `basic = "tiny_basic.repl:main"`.

`Terminal` is the third `Console`. `converse` is a *read-eval-print loop*: read a line, give it to the machine, show any complaint, and go round again. That's where the word REPL comes from, and you've now written one for the second time.

!!! example "Run it"
    ```console
    $ uv run basic
    Tiny BASIC

    >10 PRINT "HELLO"
    >20 GOTO 10
    >RUN
    HELLO
    HELLO
    HELLO
    ```

    Press ++ctrl+c++. `Escape at line 10`. You've earned that.

    ```text
    >NEW
    >10 FOR I = 1 TO 10
    >20 PRINT I, I * I, SQR(I)
    >30 NEXT
    >RUN
    >SAVE "squares"
    >20 PRINT I * (
    Missing )
    >PRINT 22 / 7
    3.14285714
    ```

    `QUIT`, or ++ctrl+d++, to leave. On Windows it's ++ctrl+z++ and then ++enter++.

#### `@contextmanager`

`timed` was the fourth Predict. You've now written the same idea three times. In Project 7 it was a function that wrapped a function. In Project 16 it could have been a decorator. As a context manager, it times *a block of code*, which needn't be a function at all:

```python
with timed("running"):
    machine.run()
```

A context manager is anything that does one thing on the way into a `with`, and another on the way out, *whatever happens in between*. Files close themselves. Locks get released. Here, a stopwatch gets read. `@contextmanager`, from `contextlib`, makes one out of a generator with exactly one `yield` in it. The code before the `yield` runs on the way in. The block runs while the generator is paused at the `yield`. The code after it runs on the way out. If the block raises an exception, it's raised *inside the generator, at the `yield`*, and that's why the `try … finally` is there. Whatever you `yield` is what `as` would receive, as `open` hands over a file. This one yields nothing.

**`nullcontext()`** is a context manager that does nothing at all. It's for occasions such as this one, where there's sometimes something to do, and sometimes not, and you don't want to write the block out twice. `contextlib` has several more. `suppress(FileNotFoundError)` is a tidy way of writing a `try` with an `except: pass`, and `redirect_stdout` catches what's printed.

Project 18 shows the other way of writing a context manager, as a class with `__enter__` and `__exit__`, which is what this decorator is building for you.

#### Was the tree worth it?

Save `primes.bas` from the repository's `examples/` folder, which counts the primes below 20,000 the slow way, and time it:

```console
$ uv run basic primes.bas --time
[loading: 0.000 seconds]
2262 primes below 20000
[running: 1.962 seconds]
```

That's a million and a half statements, at about 750,000 a second. It's some hundreds of times faster than the BBC Micro managed, and it's dreadfully slow for a modern machine, since every one of those statements is a Python `match`, some dictionary lookups, and a good many function calls.

How much did parsing in advance save? Measure one line, both ways. Save this as `measure_parse.py`:

<!-- listing: projects/17-tiny-basic/measure_parse.py -->
```python title="measure_parse.py"
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
```

```console
$ uv run measure_parse.py
Parsing the line:  17.4 microseconds
Running the tree:   2.7 microseconds
Parsing it every time would be 7.4 times slower.
```

**Tokenising and parsing a line costs six times as much as running it.** An interpreter that went back to the text each time, as your Logo does, would take fifteen seconds over those primes, and not two. Real interpreters carry this further. Python compiles your program into *bytecode*, which is a flat list of very simple instructions, and that's what the files in `__pycache__` are. BBC BASIC did a little of it too: it stored `PRINT` as a single byte, and called that a token.

!!! success "Checkpoint"
    ```console
    $ git add .
    $ git commit -m "Add the prompt, files, and --time"
    ```

### Stage 7: Strict

In Project 12 you turned Pylance from `basic` to `standard`. There's one more setting, and this is the project for it: a parser and an interpreter are made of just the sort of code, with many types and many cases, in which a type checker finds real bugs.

You could change the setting in VS Code. It's better to put it in the project, where it applies to everybody who works on it, and to the command line as well. Pylance is built on an open-source type checker called **pyright**, and both read their settings from `pyproject.toml`. Add:

```toml
[tool.pyright]
include = ["src"]
typeCheckingMode = "strict"
```

Then install pyright itself, so that it can be run from a terminal, and, in Stage 9, by GitHub:

```console
$ uv add --dev pyright
$ uv run pyright
0 errors, 0 warnings, 0 informations
```

`standard` reports code that's *wrong*. `strict` also reports code that it *can't be sure is right*: a function with no hints, a value whose type is unknown, an import that isn't used, a `dict` with nothing said about what's in it. It's demanding, and in application code that's held together with untyped libraries, it can be more trouble than it's worth. For a self-contained library such as this one, it's a second pair of eyes that never gets tired.

When this chapter's code was first checked, that line didn't say nought. It said two, and both are worth seeing.

```text
repl.py:26:2 - error: The function "contextmanager" is deprecated
    Annotating the return type as `-> Iterator[Foo]` with `@contextmanager` is
    deprecated. Use `-> Generator[Foo]` instead. (reportDeprecated)
values.py:49:10 - error: Type of "truediv" is partially unknown
    Type of "truediv" is "(a: Unknown, b: Unknown, /) -> Unknown"
```

The first was a habit from older Python, which is just what `reportDeprecated` is for. The second explains the one `lambda` in the table of operators that looks as if it needn't be there: the standard library's own hints for `operator.truediv` say nothing about its types, and strict mode won't take "unknown" for an answer. A `lambda` that the checker can see through was simpler than arguing.

Here's the typing that this project has used, all in one place:

| | |
|---|---|
| `float \| str`, `Token \| None` | a **union**: one or the other |
| `type Value = float \| str` | an **alias**: a name for a type. It may refer to itself |
| `Literal["number", "string"]` | these exact values, and no others |
| `class Peekable[T]` | a **generic class**: `T` is filled in by whoever uses it |
| `def function[F: Callable[..., Value]]` | a **generic function**, with a **bound** on `F` |
| `Callable[[float, float], float]` | a function that takes two floats and returns one. `Callable[..., X]` takes anything |
| `class Console(Protocol)` | anything with these methods |
| `assert_never(x)` | "every case has been dealt with". The checker tells you if not |
| `if TYPE_CHECKING:` | an import that only the checker sees |
| `Generator[None]` | what a `@contextmanager` function returns |
| `Self` (Project 15) | whatever class this method was called on |

When strict mode is wrong, and you're sure of it, `# pyright: ignore[reportUnknownMemberType]` at the end of a line silences one rule, on that line. Give the rule's name, always, and never a bare `# type: ignore`, which silences everything, including next year's real bug.

!!! success "Checkpoint"
    ```console
    $ git add .
    $ git commit -m "Check types in strict mode"
    ```

### Stage 8: Coverage

You have a hundred tests. Do they test everything? There's a tool that will tell you *which lines of your code no test has ever run*:

```console
$ uv add --dev pytest-cov
$ uv run pytest --cov=tiny_basic --cov-branch --cov-report=term-missing
Name                          Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------
src/tiny_basic/__init__.py        3      0      0      0   100%
src/tiny_basic/errors.py          9      0      2      0   100%
src/tiny_basic/functions.py      65      0      4      0   100%
src/tiny_basic/machine.py       211      7    102      5    96%   64, 110, 164, 213-214, 272-273
src/tiny_basic/nodes.py          49      0      0      0   100%
src/tiny_basic/parser.py        175      0     86      0   100%
src/tiny_basic/peekable.py       18      0      4      0   100%
src/tiny_basic/registry.py       20      0      0      0   100%
src/tiny_basic/repl.py           51      3      4      1    93%   23, 62-63
src/tiny_basic/tokens.py         36      0     18      0   100%
src/tiny_basic/values.py         38      0     16      0   100%
-------------------------------------------------------------------------
TOTAL                           675     10    236      6    98%
```

That's the real report from this chapter's first draft, and the `Missing` column is the useful part. `--cov-branch` counts both ways out of every `if`, and not only the lines. Go and look at each number:

- **Line 164** was the `pass` under `case nodes.Rem()`. There were remarks in the tests, and none was ever *run*. That's harmless, as it turns out, and it's one line of test to be sure.
- **Line 110** was the complaint about a file that has a line with no number in it. **An error path that had never once been run.** It might have had a typing mistake in it that would turn a polite message into a crash. This is what coverage is best at finding: the code for when things go wrong is the code that's least often tried.
- **Line 64** was what happens when you press ++enter++ on an empty line.
- **Lines 213–214 and 272–273** were the two `assert_never` cases. No test *can* reach them. That's what they're for.

So there were three tests to write:

<!-- listing: projects/17-tiny-basic/tests/test_machine.py -->
```python title="tests/test_machine.py"
def test_remarks_and_empty_lines_do_nothing(machine):
    machine.enter("")
    machine.enter("   ")
    assert run(machine, "10 REM nothing to see\n20 PRINT 1 : REM or here") == "1\n"


def test_a_file_with_a_line_that_has_no_number_is_refused(machine, tmp_path):
    program = tmp_path / "bad.bas"
    program.write_text('10 PRINT "ok"\nPRINT "no number"\n', encoding="utf-8")
    with pytest.raises(BasicError, match="has a line with no number"):
        machine.load_file(program)
```

And for the lines that can't be reached, a comment that tells coverage so: `case _:  # pragma: no cover`. Use it rarely, and only where you could defend it.

!!! warning "Gotcha"
    **Coverage tells you what you haven't tested. It can't tell you what you have.** A line is "covered" if it was run, whether or not any test looked at what it did. You can reach 100% with tests that assert nothing. So treat a low number as information, a high number as unremarkable, and never chase the last few per cent by writing tests that you wouldn't otherwise have wanted. The three lines in `repl.py` are the ones that really open a terminal. Testing those would mean faking so much that the test would prove nothing, and 99% with a known gap is an honest result.

!!! success "Checkpoint"
    ```console
    $ git add .
    $ git commit -m "Measure coverage, and test three things that it found"
    ```

### Stage 9: Let GitHub do the checking

Before every commit, you now run Ruff twice, pyright, and pytest. You'll forget, sooner or later, and one day you'll want to know that it all works on Windows when you only have a Mac. **Continuous integration**, or CI, is a machine that runs your checks for you, every time you push. GitHub's is called Actions, and it's free for public repositories.

A *workflow* is a YAML file in `.github/workflows/`. Create `.github/workflows/check.yml`:

<!-- listing: projects/17-tiny-basic/.github/workflows/check.yml -->
```yaml title=".github/workflows/check.yml"
name: Check

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  check:
    name: Python ${{ matrix.python }} on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python: ["3.13", "3.14"]
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.1.0
        with:
          enable-cache: true
          python-version: ${{ matrix.python }}
      - run: uv sync --locked
      - run: uv run ruff check
      - run: uv run ruff format --check
      - run: uv run pyright
      - run: uv run pytest --cov=tiny_basic --cov-branch --cov-fail-under=95
```

Read it from the top. **`on`** says when to run: on every push to `main`, and on every pull request. **`jobs`** has one job, called `check`, and its **`matrix`** asks for that job to be run once for every combination of three operating systems and two versions of Python. That's six brand-new virtual machines, which exist for a minute or two each. `fail-fast: false` lets the others finish when one fails, so that you can see whether a failure is Windows alone, or everywhere.

**`steps`** is what each of them does. `uses:` runs an *action*, which is a packaged step that somebody else has written: one fetches your code, and one installs uv. `run:` is a shell command, and those are the five that you know. **`uv sync --locked`** installs exactly what's in `uv.lock`, and *fails* if the lock file is out of date, which is the reason that you've been committing it since Project 0. `--cov-fail-under=95` fails the job if the coverage drops below 95%.

If any step fails, the job fails, and you get an email.

```console
$ git add .
$ git commit -m "Add continuous integration"
$ git push
$ gh run watch
```

`gh run watch` shows the jobs as they run. `gh run list` shows the recent ones, and `gh run view --log-failed` shows what went wrong. On GitHub, there's a green tick, or a red cross, beside every commit.

This is where last project's pull requests come into their own. Make a branch, break something on purpose, such as deleting the `+ 1` in the parser, push, and open a pull request. Within a couple of minutes all six checks are red *on the pull request's page*, before anything has gone near `main`. In the repository's settings, under **Branches**, you can make a passing check compulsory before anything may be merged.

!!! tip "Pythonic"
    **CI should run exactly what you run.** There's nothing in that workflow that you can't type at your own terminal, and that's deliberate. When it fails, you can reproduce the failure. If the commands should ever grow complicated, put them into a script in the repository, and have the workflow and the people both run the script. This tutorial's own repository does just that.

#### Install it

One more thing. `uv run basic` works inside the project's folder. Your BASIC is a finished tool, and it ought to work anywhere:

```console
$ uv build
Successfully built dist/tiny_basic-0.1.0.tar.gz
Successfully built dist/tiny_basic-0.1.0-py3-none-any.whl
$ uv tool install .
Installed 1 executable: basic
$ cd ~
$ basic
Tiny BASIC

>PRINT "HELLO FROM ANYWHERE"
HELLO FROM ANYWHERE
```

**`uv build`** makes the two files that Python packages are distributed as. The `.whl` is a *wheel*: a zip file of your package, ready to be installed. The `.tar.gz` is the *source distribution*. Anybody with either can install your BASIC. (`dist/` is in your `.gitignore`. Built files don't belong in Git.)

**`uv tool install`** installs a package, in an environment of its own, and puts its commands on your `PATH`. It's how you'd install Ruff itself, or any other tool that's written in Python, without disturbing any project. If `basic` isn't found, `uv tool update-shell` will put it right. `uv tool list` shows what you have, `uv tool install --reinstall .` brings it up to date after you've changed something, and `uv tool uninstall tiny-basic` removes it. Project 27 takes the last step, and publishes a package for everybody else.

## Type-in listings

They're in BASIC, this time, to be typed into your own interpreter. The first is four lines long.

<!-- listing: projects/17-tiny-basic/examples/wave.bas -->
```text title="wave.bas"
10 REM A wave, down the screen
20 FOR A = 0 TO 12.6 STEP 0.3
30   PRINT STRING$(INT(20 + 18 * SIN(A)), " "); "*"
40 NEXT
```

And here's where the tutorial came in. This is Project 1, in the language that it would have been written in, in 1982:

<!-- listing: projects/17-tiny-basic/examples/hilo.bas -->
```text title="hilo.bas"
10 REM Hi-Lo
20 SECRET = RND(100)
30 TRIES = 0
40 PRINT "I'm thinking of a number from 1 to 100."
50 REPEAT
60   INPUT "Your guess? ", GUESS
70   TRIES = TRIES + 1
80   IF GUESS < SECRET THEN PRINT "Too low."
90   IF GUESS > SECRET THEN PRINT "Too high."
100 UNTIL GUESS = SECRET
110 PRINT "Got it, in "; TRIES; " tries."
```

1. When you typed line 30 of the wave, what did `store` do with it? Draw the tree for `20 + 18 * SIN(A)`.
2. Line 20 of the wave counts from 0 to 12.6 in steps of 0.3, and 12.6 is 42 steps of 0.3. So there ought to be 43 stars. Count them. Where did the last one go? (Project 7. The BBC Micro did just the same.)
3. In Hi-Lo, which stack does line 50 push on to? What's on it? What does line 100 do with it?
4. Type `GOTO 80` at the prompt, after a game. What happens, and why is it allowed?
5. Both programs are in the repository as `.bas` files. `LIST` one after loading it. Where did the indentation go? Whose job was it to keep it?

## Bug hunt

A colleague's BASIC gets some sums right, and some wrong. Their parser is in the tutorial's repository, as `projects/17-tiny-basic/bughunt/sums.py`. It's yours, with one method overridden.

```console
$ uv run bughunt/sums.py
2 + 3 * 4      = 14
2 * 3 + 4      = 10
2 ^ 3 ^ 2      = 512
10 - 4 - 3     = 9   <-- it ought to be 3
100 / 10 / 5   = 50   <-- it ought to be 2
10 - 4 + 3     = 3   <-- it ought to be 9
```

"Precedence works," says your colleague. "Multiplication comes before addition. I tested it."

1. **Reproduce it**, and say what the three wrong ones have in common, that the three right ones haven't.
2. **Write a failing test.** The parser's tests compare trees. What tree *should* `10 - 4 - 3` make? What tree does it make?
3. **Fix it.** It's two characters.

??? success "Solution"
    The wrong ones all have two operators **of the same precedence**, side by side. Your colleague tested that `*` beats `+`. They never tested `-` against `-`.

    Their `expression` parses the right-hand side with `self.expression(precedence)`. So the right-hand side of the first `-` is allowed to contain another `-`, and takes it: `10 - (4 - 3)`, which is 9. Every operator goes from right to left. For `^`, that's correct, which is why `2 ^ 3 ^ 2` looked fine. For addition and multiplication by themselves it makes no difference, which is why nobody noticed. The fix is `precedence + 1`, for every operator but `^`.

    ```python
    def test_taking_away_goes_from_left_to_right():
        assert Parser("10 - 4 - 3").expression() == Binary(
            Binary(Number(10), "-", Number(4)), "-", Number(3)
        )
    ```

    **What to take from it.** The direction in which operators group is called *associativity*, and it's the part of precedence that people forget to test. Coverage wouldn't have helped: every line of that method was run by the tests that your colleague did write. **Coverage counts lines, and bugs live in cases.** The habit to form is asking, of any table or any rule: what happens with two of the same?

## Challenges

Make a branch for each, merge it with a pull request, and watch the checks go green.

**Tweak**

1. **More functions.** `TAN`, `UPPER$`, and `INSTR("BBC MICRO", "MIC")`, which is 5. Put them in a file of your own. How many lines of the parser did you change? Then add a command, `WAIT`, that pauses for some hundredths of a second.
2. Add `<>`'s cousin, `EOR`, which is BBC BASIC's exclusive or. It's one line in each of two tables.
3. `LIST 100, 200` lists a range of lines. `RENUMBER` renumbers the program in tens. What else has to change when the line numbers do?

**Extend**

1. **`WHILE … ENDWHILE`.** BBC BASIC had to wait for the Archimedes to get this. Add a node for each, add them to the `Statement` union, and *then follow the squiggles*: Pylance will take you to `execute`. The subtle part is a `WHILE` whose condition is false on the first visit, when the machine has to skip forward to the matching `ENDWHILE`. How will it find it? What if there's another `WHILE` inside?
2. **Arrays.** `DIM A(10)`, and then `A(3) = 7` and `PRINT A(3)`. The parser already reads `A(3)` as a call of something. How will it know which it is?
3. **`DATA`, `READ` and `RESTORE`.** These kept tables of numbers inside a program. `DATA` does nothing when it's executed. So when is it looked at?
4. **`TRACE ON`.** Print each line number, in square brackets, as it's executed, as the BBC did. `step` is the place. It's the quickest way there is of finding out why a BASIC program is going wrong.

??? tip "Hint for `WHILE`"
    When `load` flattens the program, it can see every step. That's a good moment to pair up each `WHILE` with its `ENDWHILE`, using a stack, and to remember the pairs in a dictionary from step number to step number. A `WHILE` with no `ENDWHILE` can then be reported before the program has even started.

**Invent**

1. **Procedures.** BBC BASIC had `DEF PROCname(parameters)`, `ENDPROC`, and `LOCAL`, and they're what made it the best BASIC of its day. You know what a call needs, from Logo.
2. **A pretty-printer.** Write a second function that walks the tree, and turns it back into text, with consistent spacing and capital letters. Then `LIST` needn't keep the source at all. What's lost? (Try a `REM`.)
3. **A compiler.** Walk the tree, and write out a Python program that does the same thing. `GOTO` makes that hard. What could you do about it?
4. **An optimiser.** `PRINT 2 + 3 * 4` needn't be worked out every time. Write a function from a tree to a simpler tree, which works out whatever it can in advance. It's called *constant folding*, and Python does it to your programs.

Solutions to the first Tweak, and the bug hunt's tests, are in the project's `solutions/` folder.

## Recap

You can now:

- [x] describe a language as a tree of frozen dataclasses, with a union for each family of nodes
- [x] walk a tree with a recursive function and `match`, taking nodes apart by position, by value, and several at once with `|`
- [x] use `assert_never` so that the type checker tells you about the case you forgot
- [x] parse expressions by precedence climbing, and say what the `+ 1` does
- [x] run a language that has `GOTO`, with a flat list of steps and a program counter, and keep loops and subroutines on stacks
- [x] write an iterator class, with `__iter__` and `__next__`
- [x] write generic classes and functions, with bounds, and type a decorator so that it keeps the type of what it decorates
- [x] use `Literal`, and `TYPE_CHECKING` to break an import cycle
- [x] keep operators in a table, with the `operator` module
- [x] write a context manager with `@contextmanager`, and use `nullcontext`
- [x] run pyright in strict mode, and say when it's worth it
- [x] measure coverage, read the `Missing` column, and say what coverage can't tell you
- [x] write a GitHub Actions workflow with a matrix, and read its results with `gh run`
- [x] build a wheel, and install your own program as a command

**Read more:** [PEP 636: the `match` tutorial](https://peps.python.org/pep-0636/) · [The typing documentation](https://typing.python.org/en/latest/), which has guides as well as the reference · [`contextlib`](https://docs.python.org/3/library/contextlib.html) · [Parsing expressions by precedence climbing](https://eli.thegreenplace.net/2012/08/02/parsing-expressions-by-precedence-climbing), by Eli Bendersky · [coverage.py](https://coverage.readthedocs.io/) · [GitHub Actions: the quickstart](https://docs.github.com/en/actions/writing-workflows/quickstart) · [uv: tools](https://docs.astral.sh/uv/concepts/tools/) · [BBC BASIC](https://www.bbcbasic.co.uk/bbcbasic.html), which R. T. Russell still maintains, for the language as it was, and is

That's Part 3. You've written two programming languages, and the second will be back: in the final project it gets `MOVE` and `DRAW`, `SOUND` and `ENVELOPE`, sprites, and a Pygame window with a flashing cursor, and becomes a computer.

First, there's the web. For five projects you'll make *pages*, which are pictures that are described in text and drawn by a browser. It begins in [Project 18](../part-4-web/p18-svg-plotter.md), with the simplest of them, and a pen plotter.
