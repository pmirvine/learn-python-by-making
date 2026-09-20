# Coming from another language

Most of the trouble in learning a second language comes from assuming that it works like the first. These sheets are for readers who know JavaScript or TypeScript, C# or Java, or C, and they list the places where Python looks the same and isn't, or looks different and is the same. For BBC BASIC, there's [a whole appendix](bbc-basic.md).

Each row points to the project where the Python side is taught.

## Everybody

Whichever language you've come from, these are the five things to take in first.

1. **A name is a label, and not a box.** `b = a` never copies anything. All values are objects, and all names are references to them. If you know Java's objects, or JavaScript's, you know this already: in Python it's true of *everything*, numbers included. [Project 1](../part-1-console/p01-hi-lo.md), and then [Project 4](../part-1-console/p04-codebreaker.md).
2. **Indentation is the block.** There are no braces, and no `end`. The colon opens a block, and the indentation closes it. Four spaces, and let the editor do it.
3. **Dynamic, but strong.** A name may be tied to a value of any type, but the *values* have definite types, and don't quietly turn into one another: `"3" + 4` is an error, and not `"34"` or 7. [Project 1](../part-1-console/p01-hi-lo.md).
4. **Type hints are hints.** They're checked by your editor, and by pyright, and ignored when the program runs. It's TypeScript's arrangement, without a compiling step. Projects [3](../part-1-console/p03-dice-lab.md), [4](../part-1-console/p04-codebreaker.md) and [17](../part-3-interpreters/p17-tiny-basic.md).
5. **Ask forgiveness, and not permission.** Python programmers `try` the thing, and catch the exception, where others would check first. Exceptions are cheap, and they're used for ordinary events: that's how a `for` loop learns that it's finished. [Project 5](../part-1-console/p05-colossal-cupboard.md).

## From JavaScript or TypeScript

| You write | In Python | Watch for |
|---|---|---|
| `let x = 1; const y = 2;` | `x = 1` | No declarations, and no `const`. `UPPER_CASE` is a promise, and `Final` is a hint |
| `===` and `==` | `==` | There's only the strict kind. `1 == "1"` is `False`, and there's no coercion to trip over |
| `null`, `undefined` | `None` | There's one of them. A missing dictionary key is a `KeyError`, and a missing attribute an `AttributeError`, and neither is `undefined`. [Project 3](../part-1-console/p03-dice-lab.md) |
| `if (x)`: `0`, `""`, `null`, `NaN` are falsy | `if x:`: `0`, `""`, `None`, **and empty lists, dictionaries and sets** are false | `[]` is truthy in JavaScript, and false in Python. [Project 1](../part-1-console/p01-hi-lo.md) |
| `&&`, `\|\|`, `!` | `and`, `or`, `not` | They hand back an operand, as yours do: `name or "anonymous"` |
| `x ? a : b` | `a if x else b` | The condition is in the middle |
| `` `Hello ${name}` `` | `f"Hello {name}"` | and `f"{price:.2f}"` formats as well. [Project 1](../part-1-console/p01-hi-lo.md) |
| `[1, 2, 3].map(f).filter(g)` | `[f(x) for x in items if g(x)]` | **Comprehensions** are what Python has where you'd chain. [Project 3](../part-1-console/p03-dice-lab.md) |
| `for (const x of items)` | `for x in items:` | Python's `in` is your `of`. There's no C-style `for` at all |
| `for (const k in obj)` | `for key in d:`, `for key, value in d.items():` | |
| `items.length`, `s.length` | `len(items)`, `len(s)` | A function, and not a property. Your own classes join in with `__len__`. [Project 12](../part-2-pygame/p12-asteroids.md) |
| `arr.push(x)`, `arr.includes(x)`, `arr.slice(1, 3)` | `items.append(x)`, `x in items`, `items[1:3]` | `items[-1]` is the last |
| `{name: "Ada", age: 36}` as a record | a **dataclass** | A `dict` is for look-up tables, with keys that you don't know in advance. [Project 5](../part-1-console/p05-colossal-cupboard.md) |
| `obj.key` and `obj["key"]` are the same | `d["key"]` for dictionaries, `obj.key` for objects, and they aren't the same thing | Dictionary keys needn't be strings, and `1` and `"1"` are different keys |
| `const {x, y} = point` | `x, y = point` for a tuple. `match` for anything deeper | [Project 5](../part-1-console/p05-colossal-cupboard.md) |
| `...args`, `{...a, ...b}` | `*args`, `**kwargs`, `[*a, *b]`, `a \| b` | [Project 7](../part-1-console/p07-fractal-factory.md) |
| `function f(a, b = 2)` | `def f(a, b=2):` | and callers may name arguments: `f(1, b=5)`. **Don't use a list or a dictionary as a default.** [Project 4](../part-1-console/p04-codebreaker.md) |
| `(x) => x * 2` | `lambda x: x * 2` | One expression only. For anything more, write a `def`, even inside another function |
| Closures | closures | The same, including the loop-variable trap that `var` had. [Project 7](../part-1-console/p07-fractal-factory.md) |
| `this` | `self` | An ordinary parameter, written out, and never rebound behind your back. [Project 9](../part-2-pygame/p09-snake.md) |
| `class A extends B`, `super(...)` | `class A(B):`, `super().__init__(...)` | [Project 15](../part-2-pygame/p15-sprite-editor.md) |
| `import {x} from "./mod.js"` | `from mod import x` | No paths, and no file endings. Packages are found by name. [Project 5](../part-1-console/p05-colossal-cupboard.md) |
| `npm`, `package.json`, `node_modules`, `package-lock.json`, `npx` | `uv`, `pyproject.toml`, `.venv`, `uv.lock`, `uvx` | Almost one for one. [The toolkit](../part-0-switching-on/toolkit.md), and [Project 27](../part-6-shipping/p27-ship-it.md) |
| `async`/`await`, Promises | `async`/`await`, coroutines and tasks | The keywords match, and the machinery doesn't: **nothing starts until it's awaited, or made into a task**, and there's no event loop until you run one. [Project 25](../part-5-tui/p25-newsroom.md) |
| `function*`, `yield` | generators, which are everywhere | [Project 6](../part-1-console/p06-life.md) |
| `try`/`catch`/`finally`, `throw` | `try`/`except`/`else`/`finally`, `raise` | Catch by type: `except ValueError:` |
| Interfaces, in TypeScript | `Protocol` | Structural, as yours are. [Project 16](../part-3-interpreters/p16-logo.md), and [Project 26](../part-5-tui/p26-adventure-third-edition.md) |
| Number: one type, a 64-bit float | `int`, of any size, and `float` | `7 / 2` is 3.5, and `7 // 2` is 3 |
| Tagged templates, JSX | t-strings | [Project 18](../part-4-web/p18-svg-plotter.md) |

## From C# or Java

| You write | In Python | Watch for |
|---|---|---|
| Everything in a class. `public static void main` | Functions at the top of a module, and `main()` called at the bottom | **A module is the unit**, and not a class. Don't write a class to hold functions. [Project 4](../part-1-console/p04-codebreaker.md) |
| `int count = 0;` | `count = 0`, or `count: int = 0` | The hint is optional, and unenforced. [Project 3](../part-1-console/p03-dice-lab.md) |
| `private`, `protected`, `public` | `_name`, by convention, and nothing else | "We're all adults here." Nothing stops a caller, and nobody does it. [Project 6](../part-1-console/p06-life.md) |
| Getters and setters, from the first day | A plain attribute. If it needs logic later, make it a `@property`, and no caller changes | This is why nobody writes `get_x()`. [Project 10](../part-2-pygame/p10-breakout.md) |
| `this.x` (optional) | `self.x` (compulsory) | and `self` is declared as the first parameter. [Project 9](../part-2-pygame/p09-snake.md) |
| Constructors overloaded by signature | One `__init__`, with default arguments. Other ways in are **class methods**: `Level.from_file(path)` | No overloading of any kind. [Project 10](../part-2-pygame/p10-breakout.md) |
| `record`, `struct`, a POJO with Lombok | `@dataclass` | with `frozen=True` for immutability. [Project 5](../part-1-console/p05-colossal-cupboard.md) |
| `interface IShape` | `Protocol`, which nothing has to declare that it implements. Or an abstract base class | [Project 26](../part-5-tui/p26-adventure-third-edition.md) settles which |
| `enum` | `Enum`, `IntEnum`, `IntFlag` | Members are objects, and can have methods. Projects [5](../part-1-console/p05-colossal-cupboard.md) and [19](../part-4-web/p19-pyfax.md) |
| `List<T>`, `Dictionary<K,V>`, `HashSet<T>`, arrays | `list`, `dict`, `set`, and `tuple` for fixed records | Written `list[int]` in hints. Any of them will hold a mixture, and shouldn't |
| Generics: `class Box<T>` | `class Box[T]:`, `def first[T](items: list[T]) -> T:` | For the type checker only. [Project 17](../part-3-interpreters/p17-tiny-basic.md) |
| LINQ, streams | comprehensions, generator expressions, `sum`, `any`, `all`, `sorted(key=…)`, `itertools` | Projects [3](../part-1-console/p03-dice-lab.md), [6](../part-1-console/p06-life.md) and [23](../part-5-tui/p23-rich-dashboard.md) |
| `IEnumerable`, `yield return` | generators | [Project 6](../part-1-console/p06-life.md) |
| Operator overloading (C#) | dunder methods: `__add__`, `__eq__`, `__len__`, `__getitem__` | [Project 12](../part-2-pygame/p12-asteroids.md) |
| `using (var f = …)`, try-with-resources | `with open(…) as f:` | and you can write your own. Projects [5](../part-1-console/p05-colossal-cupboard.md) and [18](../part-4-web/p18-svg-plotter.md) |
| Checked exceptions (Java) | None are checked. Document them | |
| `switch`, pattern matching | `match` | No fall-through. A bare name *captures*. [Project 5](../part-1-console/p05-colossal-cupboard.md) |
| `null`, `Optional<T>`, `T?` | `None`, `T \| None` | pyright narrows after `if x is None`. [Project 4](../part-1-console/p04-codebreaker.md) |
| Attributes, annotations | decorators | which are functions, and you can write one in four lines. [Project 16](../part-3-interpreters/p16-logo.md) |
| Reflection | `getattr`, `type`, `inspect`, and descriptors underneath it all | Everything is inspectable at run time, all the time. [Project 24](../part-5-tui/p24-teletext-viewer.md) |
| Threads, for speed | processes, or asyncio. Threads wait well, and don't compute in parallel, unless Python is free-threaded | the GIL. [Project 25](../part-5-tui/p25-newsroom.md) |
| Maven, Gradle, NuGet, a JAR | uv, `pyproject.toml`, a wheel | [Project 27](../part-6-shipping/p27-ship-it.md) |
| Dependency injection frameworks | Pass the thing in, as an argument. With a default, if you like | Projects [20](../part-4-web/p20-pyfax-live.md), [22](../part-4-web/p22-high-score-server.md) and [24](../part-5-tui/p24-teletext-viewer.md) |
| Design patterns with many classes | Often a function, a dictionary of functions, or a generator | Strategy is a function argument. Command may be a class ([Project 15](../part-2-pygame/p15-sprite-editor.md)) or a closure. Iterator is `yield` |

## From C

| You write | In Python | Watch for |
|---|---|---|
| `int main(void) { … }` | The file runs from the top. `if __name__ == "__main__": main()` | [Project 4](../part-1-console/p04-codebreaker.md) |
| Declare, then use. Fixed types, fixed sizes | Names appear when they're assigned. `int` never overflows | `array`, `struct` and `bytes` are for when you need C's sizes. [Project 11](../part-2-pygame/p11-sound-and-envelope.md) |
| `malloc`, `free`, pointers | Nothing. Objects live for as long as something refers to them | References are pointers that can't be null by accident, can't dangle, and can't do arithmetic |
| Pass by value, or by pointer | Always "by object reference": the function gets the same object, under a new name | It can *change* a list that you pass in. It can't make your name refer to a different one. [Project 4](../part-1-console/p04-codebreaker.md) |
| `char s[20]`, `strcpy`, `strlen`, `\0` | `str`: immutable, Unicode, any length | `bytes` is the raw kind. [Project 4](../part-1-console/p04-codebreaker.md) |
| `printf("%5.2f\n", x)` | `print(f"{x:5.2f}")` | The format codes will feel familiar |
| `for (i = 0; i < n; i++) a[i]` | `for item in a:` | Reaching for `range(len(a))` is the C accent, and the commonest one. `enumerate`, `zip`. [Project 3](../part-1-console/p03-dice-lab.md) |
| `i++`, `i--` | `i += 1` | `++i` is legal, and does nothing |
| `7 / 2 == 3`, `-7 / 2 == -3` | `7 / 2 == 3.5`, `7 // 2 == 3`, `-7 // 2 == -4` | `//` floors. `%` takes the sign of the divisor |
| `&&`, `\|\|`, `!` | `and`, `or`, `not` | `&`, `\|`, `^`, `~`, `<<`, `>>` are as you know them, and bind more tightly than comparisons, which is an improvement. [Project 19](../part-4-web/p19-pyfax.md) |
| `if (x = 5)` | A syntax error. `if (n := len(a)) > 5:` when you mean it | [Project 12](../part-2-pygame/p12-asteroids.md) |
| `switch`, with `break` | `match`, without | [Project 5](../part-1-console/p05-colossal-cupboard.md) |
| `struct point { int x, y; };` | `@dataclass class Point:` | [Project 5](../part-1-console/p05-colossal-cupboard.md) |
| `enum`, `#define`, bit flags | `Enum`, `IntFlag`, constants in capitals | [Project 19](../part-4-web/p19-pyfax.md) |
| Function pointers | Functions are values | [Project 7](../part-1-console/p07-fractal-factory.md) |
| `#include "thing.h"`, the linker | `import thing` | No headers, and no declarations. The module is run, once, when it's first imported. [Project 4](../part-1-console/p04-codebreaker.md) |
| Return codes, `errno` | Exceptions | You can't forget to check one |
| `make`, a compiler, a debugger | `uv run`. There's no build. The debugger is in VS Code | [Project 2](../part-1-console/p02-turtle-sketchbook.md) |
| Undefined behaviour | None. A mistake is an exception, with a line number | |
| Speed | Between 10 and 100 times slower, for loops of arithmetic. Usually it doesn't matter, and when it does, the loop goes into NumPy, or C | Measure first. Projects [7](../part-1-console/p07-fractal-factory.md), [13](../part-2-pygame/p13-life-in-pixels.md) and [25](../part-5-tui/p25-newsroom.md) |
