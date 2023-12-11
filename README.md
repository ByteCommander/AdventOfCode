# AdventOfCode

My Python 3 solutions to http://adventofcode.com 

Don't cheat by looking at them before you solved a puzzle yourself.

## Setup

Install the `aoc_tools` package with some helpers and dependencies to a new local venv:

```bash
poetry install
```

## Run a Puzzle

Use the poetry venv to execute the puzzle scripts:

```bash
poetry run python 2023/aoc2023_1a.py
```

## Solve a new Puzzle

To create a solution script stub and download your input data for a new puzzle, run the `aoc-start` command
that gets installed with the `aoc_tools` package (or run `aoc_tools/starter.py` directly instead),
providing the year and day of the puzzle to solve:

```bash
aoc-start 2023 1
```

For this to work, ensure first that:
- You have a valid `AOC_SESSION_COOKIE` environment variable (or `.env` file containing it).
  You can copy it from your browser's developer tools when logged in to https://adventofcode.com.
- The target folders for the selected year exist already (use e.g. `mkdir -p 2023/inputs` to fix).

The script will create a new solution script stub file for the first part of the given day's puzzle
(e.g. `2023/aoc2023_1a.py`) which you can edit. It's based on `aoc_tools/_template.py`.
Additionally, it downloads your personal input from the AoC website (storing it e.g. as `2023/inputs/aoc2023_1.txt`).

The solution stub uses the `aoc_tools.lib.run(...)` helper to run your main function with the automatically
discovered input text file and optionally any inline test data.
