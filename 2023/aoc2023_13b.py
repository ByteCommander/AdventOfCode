# Advent Of Code 2023, day 13, part 2
# http://adventofcode.com/2023/day/13
# solution by ByteCommander, 2023-12-16
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    patterns: list[list[list[str]]] = [[]]
    for line in file:
        if l := line.strip():
            patterns[-1].append(list(l))
        else:
            patterns.append([])

    answer = 0
    for pattern in patterns:
        for rows, factor in ((pattern, 100), ([*map(list, zip(*pattern))], 1)):  # rows, transposed columns
            for i in range(1, len(rows)):
                if calc_diff(rows[max(0, i * 2 - len(rows)):i], rows[min(i * 2, len(rows)) - 1:i - 1:-1]) == 1:
                    answer += i * factor

    print(f"The summary of all mirror axes with exactly one smudge is {answer}.")


def calc_diff(r1: list[list[str]], r2: list[list[str]]) -> int:
    diff = 0
    for a, b in zip(sum(r1, []), sum(r2, [])):  # iterate over pairs from flattened lists of field of both grid parts
        if a != b:
            diff += 1
    return diff


TEST_INPUT = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
