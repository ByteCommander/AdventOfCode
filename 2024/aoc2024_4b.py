# Advent Of Code 2024, day 4, part 2
# http://adventofcode.com/2024/day/4
# solution by ByteCommander, 2024-12-04
import itertools
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    count = 0
    grid = [list(l) for line in file if (l := line.strip())]

    directions = list(itertools.product([1, -1], [1, -1]))
    word = "MAS"

    for y, row in enumerate(grid[1:-1], 1):
        for x, val in enumerate(row[1:-1], 1):
            if val == word[1]:
                cross_count = 0
                for dy, dx in directions:
                    for i in [-1, 1]:
                        yy, xx = y + i * dy, x + i * dx
                        if grid[yy][xx] != word[i + 1]:
                            break
                    else:
                        cross_count += 1
                        print(y, x, grid[y][x], dy, dx)
                if cross_count == 2:
                    count += 1

    print(f"The word grid contains {count} X-shaped MAS sequences in any direction.")


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
