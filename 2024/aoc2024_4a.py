# Advent Of Code 2024, day 4, part 1
# http://adventofcode.com/2024/day/4
# solution by ByteCommander, 2024-12-04
import itertools
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    count = 0
    grid = [list(l) for line in file if (l := line.strip())]
    height, width = len(grid), len(grid[0])

    directions = list(filter(any, itertools.product([0, 1, -1], [0, 1, -1])))
    word = "XMAS"

    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val == word[0]:
                for dy, dx in directions:
                    for i in range(1, len(word)):
                        yy, xx = y + i * dy, x + i * dx
                        if not (0 <= yy < height and 0 <= xx < width and grid[yy][xx] == word[i]):
                            break
                    else:
                        count += 1

    print(f"The word grid contains {count} times the word XMAS in any direction.")


TEST_INPUT = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
