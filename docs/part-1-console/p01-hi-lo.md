# Project 1 · Hi-Lo

The computer thinks of a number and you try to guess it. It's the first game in a hundred programming books, and for good reason: in forty lines it uses variables, input, decisions and loops. You know all of those already. So this chapter spends its time on what Python does *differently* with them, and there's more of that than you might expect.

```text
I'm thinking of a number between 1 and 100.
[7 left] Your guess? 50
Too high.
[6 left] Your guess? 25
Too low.
[5 left] Your guess? 37
Too low.
[4 left] Your guess? forty
'forty' isn't a whole number.
[4 left] Your guess? 43
Too high.
[3 left] Your guess? 40
Got it in 5 guesses!
That's a new best: 5.
Play again? (y/n) n
Thanks for playing. Your best was 5.
```

| | |
|---|---|
| **You'll learn** | How names and objects work; `int`, `float`, `str`, `bool` and `None`; `input` and f-strings; `if`, `while`, `break` and `else`; truthiness; a first `try`/`except`; simple functions |
| **New tool skill** | The commit rhythm: `git status`, `git diff`, `git log`. Reading tracebacks. |
| **Time** | 2 hours |
| **Before you start** | [Project 0](../part-0-switching-on/p00-hello-beeb.md) |

## Predict

Four snippets. Decide what each prints *before* you open the answer. If you'd like to check, the REPL is a `uv run python` away.

!!! question "Predict"
    ```python
    a = 10
    b = a
    a = a + 1
    print(a, b)
    ```

??? success "Answer"
    ```text
    11 10
    ```

    No surprise there, perhaps. But hold on to *why*, because in Project 4 a snippet that looks just like this one will do something else. Stage 1 explains.

!!! question "Predict"
    ```python
    print("5" * 3)
    print("5" + 3)
    ```

??? success "Answer"
    ```text
    555
    Traceback (most recent call last):
      ...
    TypeError: can only concatenate str (not "int") to str
    ```

    Multiplying a string by a number repeats it. *Adding* a number to a string is an error. JavaScript would have said `"53"`; Python declines to guess what you meant.

!!! question "Predict"
    ```python
    print(7 // 2, -7 // 2)
    print(7 % 2, -7 % 2)
    ```

??? success "Answer"
    ```text
    3 -4
    1 1
    ```

    `//` is whole-number division, and it rounds *down*, towards minus infinity: not towards zero, as C, Java, JavaScript and BBC BASIC's `DIV` all do. `%` agrees with it, so the remainder always takes the sign of the divisor. Stage 3 has more.

!!! question "Predict"
    ```python
    if "0":
        print("yes")
    print(bool("False"), bool(""), bool(0.0), bool(-1))
    ```

??? success "Answer"
    ```text
    yes
    True False False True
    ```

    Any value can stand as a condition. Empty things and zeros count as false; everything else counts as true, including the strings `"0"` and `"False"`, which are not empty. Stage 3 again.

## Build

### Stage 1: One guess

Make the project, just as you did in Project 0:

```console
$ cd making
$ uv init --no-package hi-lo
$ cd hi-lo
$ code .
```

Open `main.py` and delete everything in it. A Python program doesn't need a `main` function, or any functions at all. Python runs a file from the top, one statement at a time, like a BASIC listing without the line numbers. For the first three stages that's how you'll write it. Type this in:

<!-- listing: projects/01-hi-lo/stages/stage1.py -->
```python title="main.py"
import random

secret = random.randint(1, 100)
print("I'm thinking of a number between 1 and 100.")

guess = int(input("Your guess? "))

if guess < secret:
    print("Too low.")
elif guess > secret:
    print("Too high.")
else:
    print("Got it!")

print(f"The number was {secret}.")
```

!!! example "Run it"
    ```console
    $ uv run main.py
    I'm thinking of a number between 1 and 100.
    Your guess? 50
    Too low.
    The number was 62.
    ```

    It works. It's not much of a game yet, with one guess and the answer given away, but it works. Run it a few times.

There's a good deal of Python in those twelve lines. Let's go through it.

#### Names are labels, not boxes

`secret = random.randint(1, 100)` looks like assignment in any language. You didn't declare `secret`, or say what type it is, and that's normal: a name comes into being when you first assign to it.

But what assignment *does* is different, and it's worth getting straight now, because a great deal follows from it. In BBC BASIC, C or Java, a variable is a box: a labelled piece of memory, with a type, into which values are copied. `A% = 42` puts 42 in the box called `A%`.

In Python the *value* is the thing that exists in its own right. It's an *object*, and it knows its own type. A variable is only a name attached to it: a luggage label tied to a suitcase. Assignment ties the label on. It never copies the suitcase.

Open a REPL alongside your editor (`uv run python`) and see:

```pycon
>>> secret = 42
>>> type(secret)
<class 'int'>
>>> secret = "forty-two"
>>> type(secret)
<class 'str'>
```

The name `secret` has no type. It was tied to an `int` object, and then re-tied to a `str` object. The *objects* have types, and they take them seriously, as you saw in the second Predict: `"5" + 3` is an error. Python is *dynamically* typed, in that names can refer to anything, but *strongly* typed, in that objects won't pretend to be what they aren't.

Now the first Predict again, in slow motion:

```pycon
>>> a = 10
>>> b = a
>>> a = a + 1
>>> a, b
(11, 10)
```

`b = a` ties a second label, `b`, to the *same* object that `a` is tied to. Nothing is copied. Then `a = a + 1` works out a *new* object, 11, and moves the `a` label over to it. `b` is still tied to the 10.

With numbers, you get the same answer as you would from the boxes picture, so you could be forgiven for wondering what the fuss is about. It's this: two names for one object is harmless only while the object can't change, and numbers and strings can't. Lists can. In Project 4 you'll tie two names to one list, change it through one name, and watch the change appear through the other. Labels, not boxes. Bank it for now.

!!! note "Under the bonnet"
    *Everything* in Python is an object: numbers, strings, functions, modules, even types. Objects have *methods*, functions that belong to them, which you reach with a dot.

    ```pycon
    >>> "too low".upper()
    'TOO LOW'
    >>> (100).bit_length()
    7
    ```

    The integer 100 knows how many binary digits it takes to write itself down. (The brackets are there only because `100.` would look like the start of a decimal number.) That `7` turns out to be just what this game needs. It comes back in Stage 3.

#### The standard library, and a warning about `randint`

`import random` brings in the standard library's `random` module, as `import platform` did in Project 0. `random.randint(1, 100)` gives a whole number from 1 to 100, and that does include the 100.

Remember that, because it's the odd one out. Nearly everywhere else in Python, a range *includes its start and excludes its end*. You'll meet that rule properly in Project 2, and come to like it. `randint` is the exception.

#### `input` gives you a string, always

`input("Your guess? ")` prints its prompt, waits for a line, and returns what was typed as a `str`. Always a `str`, even if what was typed was `50`. There's no `INPUT A%` that reads a number: you convert it yourself, by calling the type you want.

```pycon
>>> int("50")
50
>>> int("  50 ")
50
>>> float("2.5")
2.5
>>> str(50) + "%"
'50%'
>>> int(2.9)
2
```

`int` doesn't mind spaces around the digits. Given a `float`, it throws away the fractional part. And given something that isn't a number at all, it doesn't return zero, or `NaN`, or some other quiet nonsense:

```pycon
>>> int("seven")
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 10: 'seven'
```

It *raises an exception*: it stops, and says why. Try it on your game. Run it, and guess `seven`.

```text
Traceback (most recent call last):
  File "/Users/you/making/hi-lo/main.py", line 6, in <module>
    guess = int(input("Your guess? "))
ValueError: invalid literal for int() with base 10: 'seven'
```

Read it from the bottom, as in Project 0. *What* went wrong: a `ValueError`, and the message even quotes the offending text. *Where*: line 6. Crashing is hardly polite, but it beats carrying on with a wrong number. You'll handle this properly in Stage 3.

#### `if`, `elif`, `else`

Nothing to frighten anyone here. The points to notice:

- The condition needs no brackets, and each branch line ends in a colon.
- The block is whatever's indented underneath. When the indentation stops, so does the block.
- It's `elif`, not `else if` or `ELSE IF`.
- Comparisons are `<`, `>`, `<=`, `>=`, `==` and `!=`. A single `=` is assignment, and Python won't let you use it as a condition by mistake.
- The logical operators are words: `and`, `or`, `not`.

!!! tip "Pythonic"
    To check that a number lies within a range, you'd naturally write:

    ```python
    if guess >= 1 and guess <= 100:
    ```

    That works. But Python lets you chain comparisons, as mathematicians do:

    ```python
    if 1 <= guess <= 100:
    ```

    It means just what it looks as if it means, and `guess` is worked out only once.

#### f-strings

The last line builds its message with an f-string, which you met in Project 0. Whatever's inside the braces is an expression, and it can be any expression:

```pycon
>>> secret = 62
>>> f"The number was {secret}."
'The number was 62.'
>>> f"Twice that is {secret * 2}, and half is {secret / 2}."
'Twice that is 124, and half is 31.0.'
```

After a colon you can say how you'd like the value laid out. There's a whole miniature language for this, and you'll pick it up a piece at a time. Here are decimal places, and thousands separators:

```pycon
>>> f"{secret / 7:.2f}"
'8.86'
>>> f"{2 ** 32:,}"
'4,294,967,296'
```

!!! info "Coming from BBC BASIC"
    An f-string does the job of `PRINT "The number was ";secret%;"."`, with its semicolons, and of `@%` and `STR$` for the formatting. Python's `print` puts a space between the items you give it and a new line at the end. Both can be changed, as you saw in the Project 0 type-in: `print("no new line", end="")`.

!!! success "Checkpoint"
    It runs, so commit it.

    ```console
    $ git add .
    $ git commit -m "Pick a number and check one guess"
    ```

### Stage 2: Keep guessing

One guess isn't a game. Wrap the guessing in a loop, and count the guesses. The changed lines are highlighted.

<!-- listing: projects/01-hi-lo/stages/stage2.py -->
```python title="main.py" hl_lines="4 7 9 16 18"
import random

secret = random.randint(1, 100)
guesses = 0
print("I'm thinking of a number between 1 and 100.")

while True:
    guess = int(input("Your guess? "))
    guesses += 1

    if guess < secret:
        print("Too low.")
    elif guess > secret:
        print("Too high.")
    else:
        break

print(f"Got it in {guesses} guesses!")
```

Mind the indentation: everything from `guess = …` down to `break` has moved four spaces to the right, because it's now inside the loop. In VS Code, select the lines and press ++tab++. (++shift+tab++ moves them back.)

`while True:` is a loop with no exit condition. It goes round until a `break` jumps out of it, and here that happens when the guess is neither too low nor too high.

!!! info "Coming from BBC BASIC"
    This is `REPEAT … UNTIL guess% = secret%`. Python has no loop with its test at the bottom, no `REPEAT`/`UNTIL` and no `do`/`while`. `while True:` with a `break` is how it's done, and nobody thinks it inelegant.

!!! info "Coming from C, Java or JavaScript"
    There's no `++` in Python. `guesses += 1` is as short as it gets. All the rest of the family is there: `-=`, `*=`, `/=`, `//=`, `%=`, `**=`.

!!! example "Run it"
    ```console
    $ uv run main.py
    I'm thinking of a number between 1 and 100.
    Your guess? 50
    Too low.
    Your guess? 75
    Too high.
    Your guess? 62
    Got it in 3 guesses!
    ```

    Play it a few times. Can you always get there in seven guesses or fewer? What's your method?

Before you commit, look at what you're about to commit. This is the habit the chapter is here to give you.

```console
$ git status
$ git diff
```

`git status` says which files have changed: just `main.py`. `git diff` shows *how*: removed lines in red, with a `-` in front, and added lines in green, with a `+`. (If it fills the screen, ++space++ pages down and ++q++ gets you out.) Reading your own diff is a thirty-second code review. It's astonishing how often it catches a stray `print` you'd put in for debugging, or an edit you didn't mean to make.

!!! success "Checkpoint"
    ```console
    $ git add main.py
    $ git commit -m "Loop until the guess is right, counting guesses"
    ```

    That's the rhythm: **make it work, look at the diff, commit**. Small commits, often, each one a working program. When an experiment goes wrong, and one will, you're never more than a few minutes from safety.

### Stage 3: Bad input, and a limit

There are two things wrong with the game. Type a word and it crashes. And with unlimited guesses there's no way to lose, so there's no tension. Here's the new version. It's nearly all new, so take it slowly.

<!-- listing: projects/01-hi-lo/stages/stage3.py -->
```python title="main.py"
import random

LOWEST = 1
HIGHEST = 100
MAX_GUESSES = 7

secret = random.randint(LOWEST, HIGHEST)
guesses_left = MAX_GUESSES
print(f"I'm thinking of a number between {LOWEST} and {HIGHEST}.")
print(f"You have {MAX_GUESSES} guesses.")

while guesses_left:
    reply = input(f"[{guesses_left} left] Your guess? ")
    try:
        guess = int(reply)
    except ValueError:
        print(f"{reply!r} isn't a whole number.")
        continue

    guesses_left -= 1
    if guess < secret:
        print("Too low.")
    elif guess > secret:
        print("Too high.")
    else:
        used = MAX_GUESSES - guesses_left
        print(f"Got it in {used} {'guess' if used == 1 else 'guesses'}!")
        break
else:
    print(f"Out of guesses. I was thinking of {secret}.")
```

!!! example "Run it"
    ```console
    $ uv run main.py
    I'm thinking of a number between 1 and 100.
    You have 7 guesses.
    [7 left] Your guess? 50
    Too low.
    [6 left] Your guess? seven
    'seven' isn't a whole number.
    [6 left] Your guess? 75
    Too high.
    [5 left] Your guess? 62
    Got it in 3 guesses!
    ```

    Try to lose, as well. It takes some determination.

Six new ideas there. In order of appearance:

#### Constants are a convention

`LOWEST`, `HIGHEST` and `MAX_GUESSES` are ordinary names. Python has no `const`. Capital letters are a message from you to whoever reads the code: *this isn't supposed to change*. Python won't stop anybody changing it. A lot of Python works like this, by agreement among consenting adults rather than by enforcement, and it's less alarming in practice than it sounds.

#### Truthiness

`while guesses_left:` isn't comparing anything with anything. Python lets any value stand as a condition, and has a simple rule about which ones count as false:

- `None` and `False`
- zero, of any numeric type: `0`, `0.0`
- anything empty: `""`, and the empty list and its relatives, which you'll meet in Project 3

Everything else counts as true. So the loop goes on while `guesses_left` isn't zero. You could write `while guesses_left > 0:`, and nobody would mind. But the short form is what Python programmers write, so you need to be able to read it.

!!! warning "Gotcha"
    `"0"` is true. So is `"False"`. They're strings, and they aren't empty, and that's all Python looks at. A yes-or-no answer straight from `input()` is always true unless the user just pressed ++enter++. That was the fourth Predict.

#### `try` and `except`

This is the repair for the crash. The code that might fail goes under `try:`. If it raises a `ValueError`, Python jumps to the `except ValueError:` block instead of stopping the program. There, you apologise, and `continue` goes back round to the top of the loop, skipping the rest of the body, so that a typing slip doesn't cost the player a guess.

Do notice what you *didn't* do, which was to inspect the string beforehand to see whether it was all digits. You might think that the careful approach. In Python, the idiomatic thing is to go ahead and try, and deal with the failure if it comes. There's a reason. `int()` already knows exactly what it will accept: a minus sign, spaces around the number, underscores in the middle, digits from other alphabets. A check you wrote yourself would have to agree with it on every one of those cases, for ever. Asking `int()` directly can't get out of step. The Python community's shorthand for this is *EAFP*: "easier to ask forgiveness than permission". It returns, with its full rationale, in Project 5.

!!! warning "Gotcha"
    Always name the exception you expect: `except ValueError:`. A bare `except:` catches *everything*, including the typo on the next line that you'd very much like to be told about, and even ++ctrl+c++. Catch what you can handle, and let the rest crash. A crash with a traceback is a gift; a program that swallows its own errors is a mystery.

#### `!r`, for seeing what's really there

`{reply!r}` in an f-string means "show this the way the REPL would": with its quotes, and with anything odd made visible. If someone types a stray space, `'7 '` tells you so, where `7 ` wouldn't. It's the debugging view of a value, and you'll use it a lot.

```pycon
>>> reply = "7 "
>>> print(f"{reply} isn't a whole number.")
7  isn't a whole number.
>>> print(f"{reply!r} isn't a whole number.")
'7 ' isn't a whole number.
```

#### The one-line `if`

`'guess' if used == 1 else 'guesses'` is a *conditional expression*: an `if` that produces a value, so it can sit inside a larger expression. It reads nearly as English, *this if the test is true, else that*, with the test in the middle. In the C family it's `used == 1 ? "guess" : "guesses"`.

It's sitting in an f-string here, which is why it uses single quotes. Either sort of quote makes a string in Python, and they mean exactly the same. Most people use double quotes as a rule, and single quotes when the string itself has to contain doubles.

#### `while` … `else`

The `else` at the very bottom lines up with the `while`, not with an `if`. It's an odd one, and you'll rarely see it outside Python.

A loop's `else` block runs when the loop finishes *by its condition becoming false*. It's skipped if you left by `break`. Here, then: run out of guesses, and the `else` runs and tells you the answer. Guess right and `break`, and it doesn't. Think of it as "if no `break`".

Without it you'd need a flag, a `won = False` before the loop and `won = True` before the `break`, and a test of the flag afterwards. This is tidier. It's also fair to say that plenty of Python programmers find `while`/`else` obscure, and you shouldn't reach for it often. But you'll meet it in other people's code, and here it's a perfect fit.

#### Why seven?

Finally, the arithmetic, and the third Predict. Python has two division operators.

```pycon
>>> 100 / 8
12.5
>>> 100 // 8
12
>>> 100 % 8
4
>>> 8 / 2
4.0
```

`/` is true division, and always gives a `float`, even when the answer is whole. `//` is *floor division*: it rounds down to a whole number. `%` gives the remainder. If you've come from C or Java, where `/` between two integers quietly gives an integer, this will catch you out, once.

Rounding *down* means towards minus infinity, not towards zero, which matters as soon as a negative number is involved:

```pycon
>>> -7 // 2
-4
>>> -7 % 2
1
```

It looks peculiar at first, but it's the behaviour you nearly always want. `x % 12` is a position on a clock face whichever side of zero `x` is on, and you'll be glad of that in Part 2, when things start wrapping around the edges of the screen.

Now, why seven guesses? If you always guess the middle of what's left, each answer halves the possibilities: 100, then 50, 25, 12, 6, 3, 1. That's seven guesses at most. In general, you need as many guesses as the range has binary digits, and Python's integers will tell you that about themselves:

```pycon
>>> (100).bit_length()
7
>>> (1000).bit_length()
10
```

Seven guesses is exactly enough, then, if you play perfectly. One slip and you're in trouble, which is as it should be.

!!! success "Checkpoint"
    Status, diff, add, commit. You know the steps.

    ```console
    $ git commit -am "Handle bad input and limit the guesses"
    ```

    The `-a` is a short cut: it stages every file Git already knows about and commits them, in one go. It doesn't pick up brand-new files. Those still need a `git add`.

### Stage 4: Functions, and another round

For the final stage the player gets to play again, and the game remembers their best score. "Play again" means running all of that code more than once, and code you want to run more than once belongs in a function. This is also the moment to go back to the shape uv gave you in the first place, with a `main()` at the bottom.

The logic is what you've already written, rearranged into three functions:

<!-- listing: projects/01-hi-lo/main.py -->
```python title="main.py"
"""Hi-Lo: I think of a number, you guess it."""

import random

LOWEST = 1
HIGHEST = 100
MAX_GUESSES = 7


def ask_for_number(prompt):
    """Keep asking until the player types a whole number, then return it."""
    while True:
        reply = input(prompt)
        try:
            return int(reply)
        except ValueError:
            print(f"{reply!r} isn't a whole number.")


def play_round():
    """Play one round. Return the number of guesses used, or None for a loss."""
    secret = random.randint(LOWEST, HIGHEST)
    guesses_left = MAX_GUESSES
    print(f"\nI'm thinking of a number between {LOWEST} and {HIGHEST}.")

    while guesses_left:
        guess = ask_for_number(f"[{guesses_left} left] Your guess? ")
        guesses_left -= 1
        if guess < secret:
            print("Too low.")
        elif guess > secret:
            print("Too high.")
        else:
            used = MAX_GUESSES - guesses_left
            print(f"Got it in {used} {'guess' if used == 1 else 'guesses'}!")
            return used

    print(f"Out of guesses. I was thinking of {secret}.")
    return None


def main():
    best = None
    while True:
        score = play_round()
        if score is not None and (best is None or score < best):
            best = score
            print(f"That's a new best: {best}.")
        if not input("Play again? (y/n) ").lower().startswith("y"):
            break

    if best is None:
        print("Thanks for playing.")
    else:
        print(f"Thanks for playing. Your best was {best}.")


if __name__ == "__main__":
    main()
```

!!! example "Run it"
    Play two or three rounds in one go, win some, and contrive to lose one. Check that the best score is reported properly at the end, and that a loss doesn't count as a best.

#### Functions

`def` defines a function; you saw that in Project 0. Parameters go in the brackets, with no types. `return` hands back a value, and you can return from anywhere, including from inside a loop. Look at `ask_for_number`. Its `while True:` never breaks. The way out is the `return`, at the moment `int(reply)` succeeds. A good half of Stage 3's loop has become five lines with a name.

Notice what moving the code did to `play_round`, too. The `while`/`else` has gone. Once the loop is in a function, a win can simply `return used`, and the losing code just comes after the loop. Pulling code out into well-named functions often straightens out its control flow like that. It's one of the best reasons to do it.

The names `secret`, `guesses_left` and `guess` are now *local* to `play_round`: they come into being when it's called, and vanish when it returns. The constants at the top are *global*, and any function can read them. That's as much as you need to know about scope for now. The rest of the story is in Project 7.

!!! info "Coming from BBC BASIC"
    `def` does the work of both `DEF PROC` and `DEF FN`. Every Python function returns a value; one that never says `return` gives back `None`. And variables are local unless you say otherwise, which is the opposite of BASIC, where you had to remember `LOCAL`, and forgot.

#### Docstrings

The string on the first line of each function is its *docstring*. It isn't a comment. Python keeps it, and tools show it to you. Hover over `play_round` anywhere in VS Code and there it is. The string at the very top of the file is the docstring for the whole module.

You can see them at the REPL as well, and here's a neat thing. A Python file is a module, so you can import your own program:

<!-- no-doctest -->
```pycon
>>> import main
>>> help(main.play_round)
Help on function play_round in module main:

play_round()
    Play one round. Return the number of guesses used, or None for a loss.
```

Importing `main` didn't start the game. That's what `if __name__ == "__main__":` is for. The game starts when the file is *run*, and not when it's *imported*. It means you can take a program's functions one at a time and try them at the REPL. Go on, call `main.ask_for_number("Number? ")`. It also means that in Project 3 you can write tests for them. The full explanation of how it works is in Project 4.

#### `None`, and `is`

`play_round` returns the number of guesses for a win, and `None` for a loss. `None` is Python's "nothing here" value, its `null`. There is exactly one `None` object, and the way to ask whether you've got it is `is None`, or `is not None`. `is` asks whether two names are tied to *the very same object*, where `==` asks whether two objects have *equal values*. For `None`, identity is what you mean. Project 4 looks hard at the difference.

!!! warning "Gotcha"
    With truthiness fresh in your mind, you might want to shorten `main`'s test to:

    ```python
    if score and (not best or score < best):
    ```

    It would even work, here. But only because a score can never be 0. Truthiness can't tell `None` from `0`, or from `""`. In a game where nought was a possible score, that line would quietly treat a perfect round as no score at all, and it would be a miserable bug to find. When the question is "is there a value?", ask exactly that: `is not None`.

#### Method chaining

`input("Play again? (y/n) ").lower().startswith("y")` reads from left to right. `input` returns a `str`. `.lower()` returns a new, lower-case `str`. `.startswith("y")` returns `True` or `False`. So `y`, `Y`, `yes` and `Yeah, go on then` are all a yes. Strings come with dozens of methods like these. Type `"".` at the REPL and press ++tab++ to have a look.

!!! success "Checkpoint"
    ```console
    $ git commit -am "Play several rounds and track the best score"
    ```

    Now look back over the project:

    ```console
    $ git log --oneline
    e41c7d9 Play several rounds and track the best score
    90b2f05 Handle bad input and limit the guesses
    5a3d1be Loop until the guess is right, counting guesses
    c7f6a12 Pick a number and check one guess
    1d0e8aa Start the hi-lo project
    ```

    There's the story of the program, one line per working stage, which is why the messages are worth a moment's thought. `git show 90b2f05`, with one of *your* hashes, shows exactly what that commit changed. `git diff c7f6a12 e41c7d9` shows everything that changed between two of them. Nothing is ever lost.

## Type-in listing

Now for the game the other way round. *You* think of a number, and the computer guesses. Make a new file, `reverse.py`, type this in, and run it with `uv run reverse.py`.

<!-- listing: projects/01-hi-lo/reverse.py -->
```python title="reverse.py" linenums="1"
print("Think of a number between 1 and 100. I'll guess it.")
low, high = 1, 100
tries = 0

while low <= high:
    guess = (low + high) // 2
    tries += 1
    reply = input(f"Is it {guess}? (y = yes, h = too high, l = too low) ").lower()
    if reply == "y":
        print(f"Got it in {tries}. I never need more than 7.")
        break
    elif reply == "h":
        high = guess - 1
    elif reply == "l":
        low = guess + 1
    else:
        tries -= 1
        print("Just y, h or l, please.")
else:
    print("Hmm. One of those answers was a fib.")
```

Work out:

1. Line 2 assigns two names in one statement. Try `low, high = high, low` at the REPL. What does it do, and how would you have to write that in a language that didn't have it?
2. Why `// 2` on line 6? What would go wrong with `/ 2`?
3. When does the `else` on line 19 run? Play a round and lie to it. How does it *know*?

## Challenges

**Tweak**

1. Change `HIGHEST` to 1000. How many guesses is fair now? Better: have Python work `MAX_GUESSES` out from the range, so that you never need to think about it again.
2. Give the player some encouragement. When a guess is within 5 of the secret, say so: "Too low, but so close." (`abs()` gives the size of a number without its sign.)
3. A guess of 5000 is a wasted turn. Refuse any guess outside the range, without counting it.

**Extend**

1. **Difficulty levels.** Before each round, offer a menu: Easy (1 to 10), Normal (1 to 100) and Fiendish (1 to 10,000). Set the number of guesses to suit.
2. **Statistics.** When the player stops, report how many rounds they played, how many they won, and their average number of guesses per win, to one decimal place.

??? tip "Hint for the difficulty levels"
    `play_round` needs to be told the top of the range, so give it a parameter: `def play_round(highest):`. `ask_for_number` already keeps asking until it gets a whole number. Give it a lowest and a highest as well, and the same function will do for the menu *and* for the third Tweak.

??? tip "Hint for the statistics"
    You need three counters in `main`. And mind the player who never wins a round: what's their average? Try `0 / 0` at the REPL to see what Python thinks of the question.

**Invent**

1. **Hotter, colder.** Do away with "too high" and "too low". After each guess, say only whether it's *warmer* or *colder* than the guess before. It's a harder game than you'd think. What should happen on the first guess?
2. **Nim.** Start with 21 matches. The player and the computer take turns to remove 1, 2 or 3. Whoever takes the last match loses. Get it working with a computer that plays at random. Then find the strategy that lets the computer win nearly every time. (It involves `%`.)

Solutions to the Tweaks and Extends are in the project's `solutions/` folder.

## Recap

You can now:

- [x] explain why a Python variable is a label and not a box, and what `b = a` really does
- [x] convert between `str`, `int` and `float`, and say what happens when a conversion fails
- [x] choose between `/`, `//` and `%`, and predict what they do to negative numbers
- [x] build strings with f-strings, including `:.2f`, `:,` and `!r`
- [x] write `if`/`elif`/`else`, chained comparisons and conditional expressions
- [x] loop with `while`, `break` and `continue`, and read a `while`/`else`
- [x] say which values count as false, and why `is None` is safer than truthiness
- [x] catch a specific exception with `try`/`except`, and say why not a bare `except:`
- [x] write functions with docstrings, and import your own file at the REPL
- [x] work in the rhythm of *run, diff, commit*, and read a project's history

**Read more:** [An informal introduction to Python](https://docs.python.org/3/tutorial/introduction.html) · [More control flow tools](https://docs.python.org/3/tutorial/controlflow.html) · [Truth value testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing) · [The format specification mini-language](https://docs.python.org/3/library/string.html#formatspec) · [Pro Git: recording changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)

Next comes something to look at. In [Project 2](p02-turtle-sketchbook.md) you'll get a turtle to draw for you, and find out what Python functions can really do.
