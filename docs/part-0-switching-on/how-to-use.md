# How to use this tutorial

Five minutes on how the chapters work, and then you can get on.

## Make things, in order

Every chapter is a project. You build it in stages, and at the end of each stage you have something that runs. Do the projects in order: each assumes the ones before it, and several return later in a new form.

**Type the code; don't paste it.** It's slower, and that is the point. Typing makes you read every character. You'll make mistakes, the mistakes will produce error messages, and learning to read Python's error messages is a good part of learning Python. Every listing in this tutorial is checked against working, tested code, so when yours misbehaves, comparing the two is a fair fight.

**Then break it.** A program you've only ever seen working is a program you half understand. Change a number. Delete a line. Guess what will happen, then find out.

## How a chapter is laid out

Every project chapter has the same parts.

**Predict** comes first: a few short snippets of Python. Before you run them, commit to a guess about what they print. You will often be wrong, and that's what they're for. Being surprised is how a fact sticks; reading the same fact in a paragraph is how it slides off.

!!! question "Predict"
    ```python
    print(10 / 2)
    ```

??? success "Answer"
    `5.0`, not `5`. In Python, `/` always gives a floating-point result, even when the division is exact. Project 1 has the details.

**Build** is the main event, in stages. Each stage ends with two boxes:

!!! example "Run it"
    What to type to run your program, and what you should see when you do.

!!! success "Checkpoint"
    A Git commit. You'll make dozens of these; by Part 2 you won't think about it.

**Type-in listing** is a short program, thirty lines at most, in the spirit of the listings in 1980s computer magazines. There's no walkthrough. Type it in, run it, and work out how it does what it does.

**Bug hunt** (from Project 4) hands you a broken program. You reproduce the bug, write a test that fails because of it, and then fix it. That is how bugs get fixed in real life, and it's a skill quite separate from writing new code.

**Challenges** come in three sizes:

- **Tweak** — ten minutes. Change something that's already there.
- **Extend** — about an hour. Add a feature. Hints are there if you want them, folded away.
- **Invent** — a description of something to build, and nothing else.

Do at least the Tweaks. They're where reading turns into knowing. Solutions to the Tweak and Extend challenges are in each project's `solutions/` folder in the tutorial's repository, but a solution you've read is worth about a tenth of one you've found.

**Recap** lists what you've learned, for ticking off, with links to the official documentation.

## The boxes

Along the way you'll meet four kinds of aside.

!!! info "Coming from BBC BASIC"
    These compare Python with a language you may already know: BBC BASIC, JavaScript, C#, Java or C. Most confusion when learning a second language comes from assuming it works like your first. These boxes say which assumptions are safe and which aren't. Skip the ones that aren't about you.

!!! note "Under the bonnet"
    How something really works, one level down. You can skip these on a first reading and nothing later will depend on them. They're for the second reading, or for when you catch yourself wondering.

!!! warning "Gotcha"
    Something that will bite you, along with what it looks like when it does.

!!! tip "Pythonic"
    Two versions of the same code: the one you'd naturally write coming from another language, and the one a Python programmer would write, with the reason. *Pythonic* is the community's word for code that goes with the grain of the language.

## If you get stuck

In rough order:

1. **Read the error message.** All of it, bottom line first. Python's error messages have become very good, and the answer is often right there.
2. **Compare with the stage snapshot.** Each project's `stages/` folder has the code as it should be at the end of each stage.
3. **Use the debugger.** Project 2 shows you how. Watching your program run one line at a time clears up most mysteries.
4. **Walk away for ten minutes.** Annoyingly effective.

## A word about AI assistants

Your editor can probably finish your code for you these days. For work, that's marvellous. For learning, it's like taking a taxi to the gym.

The struggle is where the learning happens: remembering how a slice works, puzzling over the error, trying three things before the fourth works. An assistant that removes the struggle removes the learning along with it, and leaves you feeling that you understand code you couldn't have written.

So, while you work through this tutorial:

- **Switch off AI completions in your editor.** In VS Code that's one setting, `chat.disableAIFeatures`. [The toolkit](toolkit.md) shows where to find it, and how to switch it off for your tutorial folder only.
- **Do the challenges yourself.** All of them that you do at all.
- **Do use an assistant as a tutor.** "Explain this error message." "Why does Python do this?" "Here's my code: what's un-Pythonic about it?" Those questions make you better. "Write me a function that…" doesn't, yet.

When you've finished the tutorial, switch everything back on. You'll be able to tell whether what it writes is any good, which is the skill that matters.

## Conventions

Things you type in a terminal look like this. The `$` stands for your prompt; don't type it.

```console
$ uv run main.py
```

Sessions at Python's interactive prompt look like this. You type what follows `>>>`; the other lines are Python's replies.

```pycon
>>> 2 + 2
4
```

Where macOS, Windows and Linux differ, you'll see tabs:

=== "macOS"

    Instructions for macOS.

=== "Windows"

    Instructions for Windows.

=== "Linux"

    Instructions for Linux.

Choose yours once and every set of tabs on the site follows.

Keys look like ++ctrl+s++. Where a shortcut differs on a Mac, both are given: ++ctrl+s++ (++cmd+s++).

The tutorial is written for **Python 3.14**. Anything from 3.13 onwards will work. Now and then a box points out something new in a later version.

Right. [Let's get you a toolkit](toolkit.md).
