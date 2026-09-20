# Style guide

How *Learn Python by Making* is written. Read this before writing or editing a chapter. `PLAN.md` says *what* the tutorial covers; this says *how* it sounds and how a chapter is put together.

## The reader

Someone who can already program a little — in BASIC, JavaScript, C#, Java, C, anything — and is new to Python. They know what a variable, a loop and a function are. They do not need telling that programs run from top to bottom. They *do* need telling what is different, surprising or better in Python, and why.

Two consequences:

- **Be brisk about the familiar, generous about the unfamiliar.** `if` gets a sentence. Names-bind-to-objects gets a page.
- **Teach the professional habit with the language.** Git, the editor, tests, types and packaging arrive as the projects need them, one new skill at a time, never as a lecture up front.

## Voice

- Second person, present tense, active voice. "You run the program", not "the program can now be run".
- Plain words. Short sentences where they'll do. One idea per paragraph.
- Warm and a little dry. A joke is welcome if it doesn't slow anyone down. No exclamation marks doing the work of enthusiasm.
- Honest about rough edges. If a tool is awkward, say so. If something wasn't verified on a platform, say so (see "Unverified" below).
- Never "simply", "just", "obviously", "easy". They help nobody, and sting when something goes wrong.
- Don't narrate the tutorial ("in this section we will…"). Get on with it.

## Spelling and terms

- **British English in prose**: colour, initialise, behaviour, centre, licence (noun), practise (verb). Computing senses keep their usual spelling: *program*, *disk*.
- **Code follows the code's conventions.** Pygame's `Color`, CSS `color`, and so on, stay American. *Our own* identifiers are British where they're ours to name (`colour`, `gcol`).
- "the terminal" (not console, shell, or command line, unless the distinction matters). "folder" for readers, "directory" only when quoting a tool.
- First use of a term of art is in *italics*, and is defined in the same sentence.
- Keys look like ++ctrl+c++ (the `pymdownx.keys` syntax). Menu paths look like **File → Save**.
- The original machine is "the BBC Micro" or "the Beeb". Our own projects get their own names (PyFax, Wireframe); see `PLAN.md` on trademarks.

## Chapter structure

Every project chapter has these parts, in this order, with these headings.

1. **Header block** — one paragraph saying what gets built, then a screenshot (or a sample session for console projects), then the summary table: *You'll learn*, *New tool skill*, *Time*, *Before you start*.
2. **`## Predict`** — two to four short snippets. The reader guesses the output before running anything. Answers are collapsed. Choose snippets that expose what this chapter is about to explain, ideally a classic gotcha.
3. **`## Build`** — stages, each a `### Stage N: title`. Every stage ends with something that runs, then a **Run it** block saying exactly what to type and what to expect, then a **Checkpoint** with the commit to make.
4. **`## Type-in listing`** — a program of 30 lines or fewer to type in, run and puzzle out, followed by two or three questions about how it works.
5. **`## Bug hunt`** (from Project 4 onwards) — a broken file in the project's `bughunt/` folder. The reader reproduces the bug, writes a failing test, then fixes it.
6. **`## Challenges`** — three tiers, always with these names:
    - **Tweak** — ten minutes; change what's there.
    - **Extend** — about an hour; add a feature. Hints are collapsed.
    - **Invent** — a spec and nothing else.
7. **`## Recap`** — a checklist of concepts, what joined the toolbox, and links to the official documentation.

Guidance fades across each part: the first project of a part is walked through closely; the last is closer to a specification.

## Callouts

Callouts are admonitions. Use these types and titles, and no others, so readers learn what each one means.

| Purpose | Markup | Use it for |
|---|---|---|
| Coming from… | `!!! info "Coming from BBC BASIC"` | What transfers from another language and what doesn't. Name the language in the title. |
| Under the bonnet | `!!! note "Under the bonnet"` | How it really works. Skippable on a first read; never required by later text. |
| Gotcha | `!!! warning "Gotcha"` | Something that will bite, with the symptom the reader will see. |
| Pythonic | `!!! tip "Pythonic"` | Before and after: what you'd naturally write, then the idiomatic version, and why. |
| Predict | `!!! question "Predict"` | The snippet. Follow with `??? success "Answer"`. |
| Run it | `!!! example "Run it"` | The command, and what should happen. |
| Checkpoint | `!!! success "Checkpoint"` | The Git commit that closes a stage. |
| Hint | `??? tip "Hint"` | Collapsed help in challenges. |
| Unverified | `!!! bug "Not yet verified first-hand"` | Instructions taken from documentation rather than tested. Remove once confirmed. |

Two callouts in a row is one too many. If everything is highlighted, nothing is.

Per-platform instructions use tabs, always in this order: `=== "macOS"`, `=== "Windows"`, `=== "Linux"`.

## Code

- **Code first.** The project is built and tested before the chapter is written. Code lives in `projects/NN-name/`, laid out exactly as the reader's own project would be.
- **Every listing is checked.** Put `<!-- listing: projects/NN-name/path/to/file.py -->` on the line before a fenced code block, and `scripts/check_docs.py` verifies that the block appears, verbatim, in that file. A line containing only `# ...` marks an elision; the pieces either side must appear in that order. A listing without a marker is a bug unless it is deliberately wrong code (mark those `<!-- listing: none -->`).
- **REPL sessions are checked too.** Blocks fenced as `pycon` are run as doctests, top to bottom through the chapter, sharing state. Mark a session that can't be run (random output, deliberate syntax errors) with `<!-- no-doctest -->` on the line before.
- **Give blocks a title** when they belong to a file: ```` ```python title="main.py" ````. Use `hl_lines` to pick out what changed since the last stage.
- Show whole files when they're short. When they aren't, show the changed function in full, never a fragment of one, and say where it goes.
- Code is formatted by ruff with default settings and passes `ruff check` with default rules. Line length stays within 88.
- Type hints from Project 3 onwards. Docstrings on anything a reader might call.
- Comments explain *why*. The prose explains *what*.
- Output the reader will see goes in a `text` block, not a screenshot.

Stage snapshots live in `stages/`, the broken file in `bughunt/`, and Tweak and Extend solutions in `solutions/`. `scripts/check_all.py` runs the lot.

## Pictures

Screenshots are generated, not captured by hand: see `scripts/screenshots_p08.py` for the pattern. They live in `docs/assets/`, named `pNN-what.png`. Every image has alt text that says what it shows.

## Length

A chapter is as long as its project needs, typically 4,000 to 6,000 words. Cut anything the reader can do without. If a digression is interesting but not needed, it is an *Under the bonnet* box or it is gone.
