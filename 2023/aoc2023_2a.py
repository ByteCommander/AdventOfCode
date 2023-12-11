# Advent Of Code 2023, day 2, part 1
# http://adventofcode.com/2023/day/2
# solution by ByteCommander, 2023-12-11
from typing import TextIO

from aoc_tools.lib import run

BAG_CONTENT = {"red": 12, "green": 13, "blue": 14}


def main(file: TextIO):
    valid_sum = 0
    for line in file:
        game_id, sets = parse(line)
        for s in sets:
            for color, num in s.items():
                if num > BAG_CONTENT[color]:
                    # print(f"Game {game_id} is invalid because the bag does not contain {num} {color} balls")
                    break
            else:
                continue  # to break outer loop only if inner loop was broken
            break
        else:
            # print(f"Game {game_id} is valid")
            valid_sum += game_id
    print(f"The sum of all valid game IDs is {valid_sum}.")


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
