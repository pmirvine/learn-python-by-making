# Python for BBC BASIC programmers

If the last language that you knew well was the one that came with the computer, this page is for you. BBC BASIC was a fine language: structured, fast, and honest about the machine. A good deal of what you learnt from it still holds. This is a Rosetta stone, from its words to Python's, with a note wherever the ideas differ and not only the spelling.

It's also a map. Each section says where in the tutorial the Python side is taught.

## The shape of a program

| BBC BASIC | Python | |
|---|---|---|
| `10 PRINT "HELLO"` | `print("HELLO")` | No line numbers. A program is a file, and you edit it in an editor |
| `>` and immediate mode | `>>>`, the REPL | It can't hold a program, but it's still the best place to try a thing out. [Project 0](../part-0-switching-on/p00-hello-beeb.md) |
| `REM a remark` | `# a remark` | |
| `:` between statements | a new line | `;` exists. Nobody uses it |
| `LIST`, `RENUMBER`, `AUTO` | your editor | |
| `SAVE "PROG"`, `LOAD`, `CHAIN` | files, and `uv run prog.py` | and Git, which is `SAVE` with a memory. [Project 1](../part-1-console/p01-hi-lo.md) |
| `NEW`, `OLD` | `git restore`, `git stash` | [Project 4](../part-1-console/p04-codebreaker.md) |
| `END` | the end of the file | `sys.exit()`, or `raise SystemExit`, to stop early |
| Blocks end with a keyword: `NEXT`, `UNTIL`, `ENDPROC` | **Blocks are indented**, and end when the indentation does | The colon at the end of `if`, `for`, `def` and `class` lines opens one |

## Variables and types

| BBC BASIC | Python | |
|---|---|---|
| `A% = 42` (integer), `A = 4.2` (real), `A$ = "HI"` (string) | `a = 42`, `a = 4.2`, `a = "HI"` | **No suffixes.** The *value* has a type, and the name doesn't. A name can be tied to anything. [Project 1](../part-1-console/p01-hi-lo.md) |
| `LET A = 1` | `a = 1` | |
| Integers are 32 bits, and overflow | Integers never overflow: `2 ** 200` is fine | [Project 7](../part-1-console/p07-fractal-factory.md) |
| Reals have about 9 significant figures | Floats have about 16 | and the same trouble with a tenth |
| `A%` to `Z%` survive `RUN`; everything is global | Variables belong to the function that assigns them | This is the opposite default, and the better one. [Project 7](../part-1-console/p07-fractal-factory.md) |
| `TRUE` is -1, `FALSE` is 0 | `True` and `False`, of type `bool` | and nearly anything can be tested for truth: an empty string or list is false |
| `AND`, `OR`, `EOR`, `NOT`, which work on bits | `and`, `or`, `not` for truth. `&`, `\|`, `^`, `~` for bits | In BASIC they were the same thing, which is why `TRUE` had to be -1. [Project 19](../part-4-web/p19-pyfax.md) |
| Long names allowed, but `TOTAL` mustn't start with a keyword (`TO`!) | Any name that isn't one of about 35 keywords. `lower_case_with_underscores` by convention | |

## Arithmetic

| BBC BASIC | Python | |
|---|---|---|
| `7 / 2` is 3.5 | `7 / 2` is 3.5 | |
| `7 DIV 2`, `7 MOD 2` | `7 // 2`, `7 % 2`, or both at once: `divmod(7, 2)` | For negatives, Python rounds *down*, and BASIC rounded towards nought |
| `2 ^ 8` | `2 ** 8` | `^` is exclusive-or, in Python |
| `INT(X)` | `math.floor(x)`, or `int(x)`, which truncates | |
| `ABS`, `SGN`, `SQR`, `SIN`, `COS`, `TAN`, `LN`, `LOG`, `EXP`, `PI` | `abs` is built in. The rest are in `math`: `math.sqrt`, `math.sin`, `math.log`, `math.log10`, `math.pi`. There's no `SGN` | Angles are in radians, as they were |
| `RAD(D)`, `DEG(R)` | `math.radians(d)`, `math.degrees(r)` | |
| `RND(6)`, `RND(1)` | `random.randint(1, 6)`, `random.random()` | and `random.choice`, `shuffle`, `sample`. [Project 3](../part-1-console/p03-dice-lab.md) |
| `A = A + 1` | `a += 1` | There's no `++` |
| `EVAL("2+2")` | `eval("2+2")` exists, and you shouldn't use it on anything that a stranger typed | Write a parser. [Project 16](../part-3-interpreters/p16-logo.md) |

## Printing and asking

| BBC BASIC | Python | |
|---|---|---|
| `PRINT "SCORE ";S%` | `print("SCORE", s)`, or better, `print(f"SCORE {s}")` | **f-strings** do the work of `;`, `,`, `@%` and `STR$` together. [Project 1](../part-1-console/p01-hi-lo.md) |
| `PRINT "NO NEW LINE";` | `print("NO NEW LINE", end="")` | |
| `PRINT ''` | `print("\n")` | |
| `@% = &20209` and its friends | `f"{x:8.2f}"`, `f"{n:>6,}"`, `f"{n:08b}"` | a small language inside the braces, and worth learning |
| `PRINT TAB(10,5);"HI"` | not in a plain terminal. Rich, Textual, or your own micro | Projects [23](../part-5-tui/p23-rich-dashboard.md), [24](../part-5-tui/p24-teletext-viewer.md) and [28](../part-6-shipping/p28-boot-to-basic.md) |
| `INPUT "NAME", N$` | `name = input("NAME? ")` | `input` **always** gives a string. For a number: `int(input("AGE? "))`, and be ready for `ValueError` |
| `G$ = GET$`, `INKEY(100)`, `INKEY(-99)` | in a game, Pygame's events and `pygame.key.get_pressed()` | [Project 9](../part-2-pygame/p09-snake.md) |
| `VDU 7` | `print("\a")` | it may even beep |

## Decisions and loops

```python
if lives == 0:                       # IF L%=0 THEN PRINT "GAME OVER" ELSE ...
    print("GAME OVER")
elif lives == 1:
    print("LAST LIFE")
else:
    print(f"{lives} LIVES")
```

BBC BASIC's `IF` lived on one line, which is why so many listings had `GOTO`s in them. Python's can be as long as it needs to be, and `elif` chains them.

| BBC BASIC | Python | |
|---|---|---|
| `=` for both assigning and comparing, and `<>` | `=` assigns. `==` compares. `!=` for not equal | |
| `FOR I% = 1 TO 10` | `for i in range(1, 11):` | **The end is left out.** `range(10)` is 0 to 9, which is what you want for counting things. [Project 2](../part-1-console/p02-turtle-sketchbook.md) |
| `FOR I% = 10 TO 0 STEP -2` | `for i in range(10, -1, -2):` | |
| `FOR I% = 0 TO N%-1 : PRINT A$(I%) : NEXT` | `for name in names: print(name)` | **Loop over the things, and not over their numbers.** If you need the number as well, `for i, name in enumerate(names)`. [Project 3](../part-1-console/p03-dice-lab.md) |
| `REPEAT … UNTIL X% = 0` | `while True:` … `if x == 0: break` | There's no loop with its test at the bottom. [Project 1](../part-1-console/p01-hi-lo.md) |
| (BASIC V) `WHILE … ENDWHILE` | `while x > 0:` | |
| `ON C% GOTO 100, 200, 300`; (BASIC V) `CASE … OF` | `match command:` | which also takes data apart. [Project 5](../part-1-console/p05-colossal-cupboard.md) |
| `GOTO 100` | nothing at all | You won't miss it, which you wouldn't have believed at the time |

## Procedures and functions

```python
def box(width, height, filled=False):    # DEF PROCbox(W%, H%, F%)
    ...                                   # ENDPROC

def area(width, height):                  # DEF FNarea(W%, H%) = W% * H%
    return width * height
```

| BBC BASIC | Python | |
|---|---|---|
| `DEF PROCname` … `ENDPROC`, and `DEF FNname` … `=value` | `def name():`, for both | A function that doesn't `return` anything gives back `None`. [Project 1](../part-1-console/p01-hi-lo.md) |
| `PROCbox(10, 20)` | `box(10, 20)`, or `box(width=10, height=20)`, or `box(10, 20, filled=True)` | keyword arguments, and defaults. [Project 2](../part-1-console/p02-turtle-sketchbook.md) |
| `LOCAL X%` | nothing: a variable assigned inside a function is local already | `global x` is the exception, and rare. [Project 8](../part-2-pygame/p08-mode2-sketchpad.md) |
| Procedures at the end, after `END`, at line 1000 | Functions first, and `main()` called at the bottom | or in other files: `import`. [Project 4](../part-1-console/p04-codebreaker.md) |
| `GOSUB 2000` … `RETURN` | a function | |
| Recursion, with `LOCAL` | recursion | [Project 2](../part-1-console/p02-turtle-sketchbook.md) |
| A function can return one value | A function can return several: `return x, y` | It's one tuple, really. [Project 2](../part-1-console/p02-turtle-sketchbook.md) |
| You can't pass a procedure to a procedure | Functions are values: pass them, store them in lists and dictionaries, return them | It changes how you design programs. Projects [7](../part-1-console/p07-fractal-factory.md) and [16](../part-3-interpreters/p16-logo.md) |

## Arrays, strings and data

| BBC BASIC | Python | |
|---|---|---|
| `DIM A%(9)`: ten integers, fixed for ever | `a = [0] * 10`, or `a = []` and `a.append(…)` | A **list** grows, shrinks, holds anything, and knows its `len`. [Project 3](../part-1-console/p03-dice-lab.md) |
| `A%(0)` to `A%(9)` | `a[0]` to `a[9]`, and `a[-1]` for the last, and `a[2:5]` for a slice | |
| `DIM G%(7,7)` | a list of lists: `g[y][x]`. Or a dictionary with `(x, y)` keys, or a set of them | [Project 6](../part-1-console/p06-life.md) |
| Parallel arrays: `NAME$(I%)`, `SCORE%(I%)` | one list of **dataclasses**, or a **dictionary**: `scores["ADA"]` | BASIC had nothing like a dictionary, and you'll wonder how you managed. Projects [3](../part-1-console/p03-dice-lab.md) and [5](../part-1-console/p05-colossal-cupboard.md) |
| `DATA`, `READ`, `RESTORE` | a list, written in the program: `LEVELS = [...]`. Or a file: text, JSON, TOML | Projects [5](../part-1-console/p05-colossal-cupboard.md), [10](../part-2-pygame/p10-breakout.md) and [14](../part-2-pygame/p14-wireframe.md) |
| `LEN(A$)` | `len(a)` | the same `len` as for a list |
| `LEFT$(A$, 2)`, `RIGHT$(A$, 2)`, `MID$(A$, 2, 3)` | `a[:2]`, `a[-2:]`, `a[1:4]` | **slices**, and they count from nought. [Project 4](../part-1-console/p04-codebreaker.md) |
| `INSTR(A$, "X")` | `"X" in a`, or `a.find("X")` | |
| `A$ + B$`, `STRING$(3, "AB")` | `a + b`, `"AB" * 3` | |
| `ASC("A")`, `CHR$(65)` | `ord("A")`, `chr(65)` | and the whole of Unicode, where there were 256 |
| `STR$(X)`, `VAL(A$)` | `str(x)`, `int(a)` or `float(a)` | `VAL("FROG")` was 0. `int("FROG")` is a `ValueError`, which is kinder in the long run |
| Strings of up to 255 characters, which you could poke | Strings of any length, which **can't be changed**: methods return new ones | `a.upper()`, `a.split()`, `", ".join(words)`. [Project 4](../part-1-console/p04-codebreaker.md) |

## Errors

| BBC BASIC | Python | |
|---|---|---|
| `ON ERROR GOTO 9000`, then `ERR`, `ERL`, `REPORT` | `try:` … `except ValueError as error:` | Around the few lines that might fail, and for the kinds of failure that you expect. [Project 1](../part-1-console/p01-hi-lo.md) |
| `Mistake`, `No such variable`, `Type mismatch at line 120` | a *traceback*: the error, the line, and how the program got there. Read it from the bottom | [Project 1](../part-1-console/p01-hi-lo.md) |
| `ON ERROR OFF` | not catching it | |
| ++escape++ | ++ctrl+c++, which raises `KeyboardInterrupt` | |
| Raising your own: `ERROR 100, "Bad move"` (BASIC V) | `raise ValueError("Bad move")`, and classes of your own | [Project 5](../part-1-console/p05-colossal-cupboard.md) |

## Files

| BBC BASIC | Python | |
|---|---|---|
| `F% = OPENOUT "SCORES"`, `PRINT#F%, S%`, `CLOSE#F%` | `with open("scores.txt", "w", encoding="utf-8") as file:` and `file.write(…)` | `with` does the `CLOSE#`, even if something goes wrong. [Project 5](../part-1-console/p05-colossal-cupboard.md) |
| `OPENIN`, `INPUT#`, `EOF#` | `for line in file:` | or `Path("scores.txt").read_text()` for the lot |
| `BGET#`, `BPUT#` | `open(…, "rb")`, and `bytes` | [Project 11](../part-2-pygame/p11-sound-and-envelope.md) |
| `*CAT`, `*DELETE` | `pathlib.Path`: `.iterdir()`, `.unlink()`, `.exists()` | |

## The machine

| BBC BASIC | Python | |
|---|---|---|
| `MODE 2`, `MOVE`, `DRAW`, `PLOT 85`, `GCOL`, `CLG`, `POINT` | **Pygame**, and the `beeb` package that you build on it, with the same words and the same 1280 by 1024 | Projects [8](../part-2-pygame/p08-mode2-sketchpad.md) to [15](../part-2-pygame/p15-sprite-editor.md) |
| `SOUND 1, -15, 53, 20`, `ENVELOPE` | `beeb.sound(1, -15, 53, 20)`, made from arithmetic | [Project 11](../part-2-pygame/p11-sound-and-envelope.md) |
| `MODE 7`, and its control codes | PyFax, in HTML, and then in a terminal | Projects [19](../part-4-web/p19-pyfax.md) and [24](../part-5-tui/p24-teletext-viewer.md) |
| `TIME` | `time.monotonic()`, `time.perf_counter()` | |
| `?&7C00 = 65`, `!`, `$`, and `HIMEM` | Nothing. Python doesn't let you at memory | `bytes`, `bytearray`, `array` and `struct` are as near as it gets. [Project 11](../part-2-pygame/p11-sound-and-envelope.md) |
| `[ LDA #65 : JSR &FFEE : RTS ]` | Nothing. But see [the last brief](../part-6-shipping/where-next.md) | |
| `*FX`, `OSBYTE`, `OSWORD`, `VDU 23` | the standard library, and more than half a million packages on PyPI | `uv add` is the new sideways ROM |
| All of it, at once | [Project 28](../part-6-shipping/p28-boot-to-basic.md) | |

## What BASIC never had

These are the things that will change how you think, more than any of the spellings above. None has a counterpart on the left-hand side.

- **Dictionaries, sets and tuples**, and a `for` that loops over any of them. [Project 3](../part-1-console/p03-dice-lab.md).
- **Modules and packages**: a program in many files, and other people's code, installed by name. Projects [4](../part-1-console/p04-codebreaker.md) and [5](../part-1-console/p05-colossal-cupboard.md).
- **Classes**: data with its behaviour attached. Projects [9](../part-2-pygame/p09-snake.md) to [15](../part-2-pygame/p15-sprite-editor.md).
- **Functions as values**, closures, and decorators. Projects [7](../part-1-console/p07-fractal-factory.md) and [16](../part-3-interpreters/p16-logo.md).
- **Generators**: functions that hand over a value, and wait to be asked for the next. [Project 6](../part-1-console/p06-life.md).
- **Tests.** You tested by running the program and looking. So will you still, and then you'll write it down, so that the computer can look again tomorrow. From [Project 3](../part-1-console/p03-dice-lab.md).
- **Version control.** `SAVE "PROG2"`, `SAVE "PROG3"`, `SAVE "PROG3B"` was version control, done by hand, with the same purpose. Git does it properly. From [Project 1](../part-1-console/p01-hi-lo.md).

And one thing that BASIC had, and Python keeps: you can type a line, press ++enter++, and see what happens. Use it as much as you did then.
