"""Running a Logo program."""

from collections import ChainMap
from collections.abc import Callable
from dataclasses import dataclass

from logo.errors import LogoError
from logo.reader import Item, Stream, read
from logo.registry import COMMANDS, show
from logo.tokens import Token, tokenise
from logo.turtle import Canvas, Turtle

type Value = float | bool | str | list[Item]


class Stop(Exception):
    """Raised by STOP and OUTPUT, to leave a procedure from however deep inside it."""

    def __init__(self, value: Value | None = None) -> None:
        super().__init__()
        self.value = value


@dataclass(frozen=True)
class Procedure:
    name: str
    parameters: tuple[str, ...]
    body: list[Item]


class Interpreter:
    def __init__(self, canvas: Canvas, say: Callable[[str], None] = print) -> None:
        self.turtle = Turtle(canvas)
        self.say = say
        self.variables: ChainMap[str, Value] = ChainMap()
        self.procedures: dict[str, Procedure] = {}
        self.counts: list[int] = []  # how far round each REPEAT we are, innermost last

    def run(self, text: str) -> None:
        """Run some Logo. Anything wrong with it comes out as a LogoError."""
        try:
            self.execute(read(tokenise(text)))
        except Stop:
            raise LogoError("STOP and OUTPUT only make sense inside a TO") from None
        except RecursionError as error:
            raise LogoError("That went too deep. Is there a STOP missing?") from error
        except ZeroDivisionError as error:
            raise LogoError("I can't divide by nought") from error

    def execute(self, items: list[Item]) -> None:
        stream = Stream(items)
        while stream.more:
            if stream.next_is("TO"):
                self.define(stream)
                continue
            value = self.expression(stream)
            if value is not None:
                raise LogoError(f"You don't say what to do with {show(value)}")

    def define(self, stream: Stream) -> None:
        """Deal with TO name :input :input ... END."""
        stream.take()
        match stream.take() if stream.more else None:
            case Token(kind="word", text=name) if name not in COMMANDS:
                pass
            case other:
                raise LogoError(f"TO can't use {show(other)} as a name")

        parameters = []
        while isinstance(item := stream.peek(), Token) and item.kind == "variable":
            parameters.append(item.text)
            stream.take()
        body = []
        while not stream.next_is("END"):
            if not stream.more:
                raise LogoError(f"TO {name} has no END")
            body.append(stream.take())
        stream.take()
        self.procedures[name] = Procedure(name, tuple(parameters), body)

    def call(self, word: Token, stream: Stream) -> Value | None:
        """Run the command or procedure that a word names, with inputs from the stream."""
        if word.text in COMMANDS:
            wanted = COMMANDS[word.text].inputs
        elif word.text in self.procedures:
            wanted = len(self.procedures[word.text].parameters)
        else:
            raise LogoError(f"I don't know how to {word.text}")

        inputs = []
        for _ in range(wanted):
            if not stream.more:
                raise LogoError(f"Not enough inputs to {word.text}")
            value = self.expression(stream)
            if value is None:
                raise LogoError(f"{word.text} needs a value, and didn't get one")
            inputs.append(value)

        if word.text in COMMANDS:
            return COMMANDS[word.text].function(self, *inputs)
        return self.invoke(self.procedures[word.text], inputs)

    def invoke(self, procedure: Procedure, inputs: list[Value]) -> Value | None:
        named = dict(zip(procedure.parameters, inputs, strict=True))
        self.variables = self.variables.new_child(named)
        try:
            self.execute(procedure.body)
        except Stop as stop:
            return stop.value
        finally:
            self.variables = self.variables.parents
        return None

    def assign(self, name: str, value: Value) -> None:
        """Change a variable where it already is, or else make a new one at the top."""
        for scope in self.variables.maps:
            if name in scope:
                scope[name] = value
                return
        self.variables.maps[-1][name] = value

    # Expressions, by recursive descent. Each of these methods deals with one level
    # of the grammar, and calls the next one down for the pieces.

    def expression(self, stream: Stream) -> Value | None:
        """sum, or sum < sum, or sum > sum, or sum = sum"""
        left = self.sum(stream)
        if stream.next_is("<", ">", "="):
            sign = str(stream.take())
            right = self.sum(stream)
            if sign == "=":
                return left == right
            a, b = self.number(left, sign), self.number(right, sign)
            return a < b if sign == "<" else a > b
        return left

    def sum(self, stream: Stream) -> Value | None:
        """product, and then any number of + product or - product"""
        total = self.product(stream)
        while stream.next_is("+", "-"):
            sign = str(stream.take())
            right = self.number(self.product(stream), sign)
            left = self.number(total, sign)
            total = left + right if sign == "+" else left - right
        return total

    def product(self, stream: Stream) -> Value | None:
        """atom, and then any number of * atom or / atom"""
        total = self.atom(stream)
        while stream.next_is("*", "/"):
            sign = str(stream.take())
            right = self.number(self.atom(stream), sign)
            left = self.number(total, sign)
            total = left * right if sign == "*" else left / right
        return total

    def atom(self, stream: Stream) -> Value | None:
        """a number, a :variable, a "word, a [list], (an expression), -atom, or a call"""
        if not stream.more:
            raise LogoError("There's something missing at the end")
        match stream.take():
            case list() as items:
                return items
            case Token(kind="number", text=text):
                return float(text)
            case Token(kind="quoted", text=text):
                return text
            case Token(kind="variable", text=name):
                if name not in self.variables:
                    raise LogoError(f"{name} has no value")
                return self.variables[name]
            case Token(kind="word") as word:
                return self.call(word, stream)
            case Token(text="("):
                value = self.expression(stream)
                if not stream.next_is(")"):
                    raise LogoError("There's a ( with no ) to close it")
                stream.take()
                return value
            case Token(text="-"):
                return -self.number(self.atom(stream), "-")
            case other:
                raise LogoError(f"I didn't expect {show(other)} there")

    def number(self, value: Value | None, sign: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise LogoError(f"{sign} doesn't like {show(value)} as input")
        return value
