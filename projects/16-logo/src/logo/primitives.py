"""Logo's built-in commands. Importing this module is what puts them on the list."""

import random

from logo.errors import LogoError
from logo.interpreter import Interpreter, Stop, Value
from logo.registry import COMMANDS, command, numeric, show
from logo.turtle import COLOURS


@command("FORWARD", "FD")
@numeric
def forward(logo: Interpreter, distance: float) -> None:
    """FORWARD 50   Move forward, drawing a line if the pen is down."""
    logo.turtle.forward(distance)


@command("BACK", "BK")
@numeric
def back(logo: Interpreter, distance: float) -> None:
    """BACK 50   Move backward."""
    logo.turtle.forward(-distance)


@command("RIGHT", "RT")
@numeric
def right(logo: Interpreter, degrees: float) -> None:
    """RIGHT 90   Turn clockwise."""
    logo.turtle.turn(degrees)


@command("LEFT", "LT")
@numeric
def left(logo: Interpreter, degrees: float) -> None:
    """LEFT 90   Turn anticlockwise."""
    logo.turtle.turn(-degrees)


@command("PENUP", "PU")
def penup(logo: Interpreter) -> None:
    """PENUP   Stop drawing."""
    logo.turtle.pen_down = False


@command("PENDOWN", "PD")
def pendown(logo: Interpreter) -> None:
    """PENDOWN   Start drawing again."""
    logo.turtle.pen_down = True


@command("SETPENCOLOR", "SETPC")
@numeric
def setpencolor(logo: Interpreter, colour: float) -> None:
    """SETPENCOLOR 1   Choose a colour, from 0 to 7, as on the BBC Micro."""
    if colour not in range(len(COLOURS)):
        raise LogoError(f"SETPENCOLOR doesn't like {show(colour)} as input")
    logo.turtle.colour = int(colour)


@command("SETXY")
@numeric
def setxy(logo: Interpreter, x: float, y: float) -> None:
    """SETXY 100 50   Go straight to a place, drawing a line if the pen is down."""
    logo.turtle.goto(x, y)


@command("HOME")
def home(logo: Interpreter) -> None:
    """HOME   Go back to the middle, facing up, without drawing."""
    logo.turtle.home()


@command("CLEARSCREEN", "CS")
def clearscreen(logo: Interpreter) -> None:
    """CLEARSCREEN   Wipe the picture, and go home."""
    logo.turtle.canvas.clear()
    logo.turtle.home()


@command("REPEAT")
def repeat(logo: Interpreter, times: Value, block: Value) -> None:
    """REPEAT 4 [FD 50 RT 90]   Do what's in the brackets, that many times."""
    if not isinstance(times, float) or not isinstance(block, list):
        raise LogoError("REPEAT needs a number, and then something in [ ]")
    for count in range(1, int(times) + 1):
        logo.counts.append(count)
        try:
            logo.execute(block)
        finally:
            logo.counts.pop()


@command("REPCOUNT")
def repcount(logo: Interpreter) -> float:
    """REPCOUNT   How many times round the REPEAT we are, counting from 1."""
    if not logo.counts:
        raise LogoError("REPCOUNT only makes sense inside a REPEAT")
    return float(logo.counts[-1])


@command("IF")
def if_(logo: Interpreter, condition: Value, block: Value) -> None:
    """IF :size < 5 [STOP]   Do what's in the brackets, if it's true."""
    if not isinstance(condition, bool) or not isinstance(block, list):
        raise LogoError("IF needs something true or false, and then something in [ ]")
    if condition:
        logo.execute(block)


@command("IFELSE")
def ifelse(logo: Interpreter, condition: Value, block: Value, otherwise: Value) -> None:
    """IFELSE :n = 0 [PRINT "none] [PRINT :n]   One or the other."""
    if not (isinstance(condition, bool) and isinstance(block, list)):
        raise LogoError("IFELSE needs something true or false, and two lots of [ ]")
    if not isinstance(otherwise, list):
        raise LogoError("IFELSE needs something true or false, and two lots of [ ]")
    logo.execute(block if condition else otherwise)


@command("STOP")
def stop(logo: Interpreter) -> None:
    """STOP   Leave the procedure that we're in."""
    raise Stop


@command("OUTPUT", "OP")
def output(logo: Interpreter, value: Value) -> None:
    """OUTPUT :n * 2   Leave the procedure, and hand this back to whoever called it."""
    raise Stop(value)


@command("MAKE")
def make(logo: Interpreter, name: Value, value: Value) -> None:
    """MAKE "size 50   Give a variable a value. Read it back with :size."""
    if not isinstance(name, str):
        raise LogoError(f"MAKE doesn't like {show(name)} as a name. Try MAKE \"SIZE")
    logo.assign(name, value)


@command("RANDOM")
@numeric
def random_(logo: Interpreter, limit: float) -> float:
    """RANDOM 6   A whole number from 0 up to, and not including, the limit."""
    return float(random.randrange(int(limit)))


@command("REMAINDER")
@numeric
def remainder(logo: Interpreter, number: float, divisor: float) -> float:
    """REMAINDER 17 5   What's left over when one number is divided by another."""
    return float(number % divisor)


@command("PRINT", "PR")
def print_(logo: Interpreter, value: Value) -> None:
    """PRINT :size   Show a value."""
    text = show(value)
    logo.say(text[1:-1] if isinstance(value, list) else text)


@command("HELP")
def help_(logo: Interpreter) -> None:
    """HELP   This list."""
    seen: list[str] = []
    for primitive in COMMANDS.values():
        line = (primitive.function.__doc__ or primitive.name).strip()
        if line not in seen:
            seen.append(line)
            logo.say(line)
