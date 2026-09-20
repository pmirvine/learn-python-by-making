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
