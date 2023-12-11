# Advent Of Code 2023, day 2, part 2
# http://adventofcode.com/2023/day/2
# solution by ByteCommander, 2023-12-11
from math import prod
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    power_sum = 0
    for line in file:
        game_id, sets = parse(line)
        minimal: dict[str, int] = {}
        for color in "red", "green", "blue":
            minimal[color] = max(s[color] for s in sets if color in s)
        power = prod(minimal.values())
        # print(f"Game {game_id} needs a minimal bag {minimal} with power {power}.")
        power_sum += power
    print(f"The sum of all minimal game sets' powers is {power_sum}.")


def parse(line: str) -> (int, list[dict[str, int]]):
    _game_id, _sets = line.split(": ")
    game_id = int(_game_id.split()[-1])
    sets = [
        dict([
            (lambda _n, _c: (_c, int(_n)))(*_n_col.split())
            for _n_col in _set.split(", ")
        ])
        for _set in _sets.split("; ")
    ]
    return game_id, sets


TEST_INPUT = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

if __name__ == "__main__":
    run(main, TEST_INPUT)
