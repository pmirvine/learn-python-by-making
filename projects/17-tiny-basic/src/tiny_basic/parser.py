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
