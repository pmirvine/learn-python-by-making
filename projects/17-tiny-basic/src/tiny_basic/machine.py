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
