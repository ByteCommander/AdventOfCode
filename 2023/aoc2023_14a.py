# Advent Of Code 2023, day 14, part 1
# http://adventofcode.com/2023/day/14
# solution by ByteCommander, 2023-12-16
from typing import TextIO

from aoc_tools.lib import run

BLOCK = "#"
ROCK = "O"
EMPTY = "."


def main(file: TextIO):
    grid: list[list[str]] = []
    for line in file:
        grid.append(list(line.strip()))

    # tilt north, all rocks roll straight north
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == ROCK:
                yn = y
                while yn > 0 and grid[yn - 1][x] == EMPTY:
                    yn -= 1
                grid[y][x] = EMPTY
                grid[yn][x] = ROCK
    # print(*["".join(row) for row in grid], sep="\n")

    load = sum(row.count(ROCK) * (len(grid) - i) for i, row in enumerate(grid))
    print(f"The north support beam load is {load}.")


TEST_INPUT = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
