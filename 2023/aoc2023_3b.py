# Advent Of Code 2023, day 3, part 2
# http://adventofcode.com/2023/day/3
# solution by ByteCommander, 2023-12-11
from math import prod
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    grid = [list(line.strip()) for line in file]
    height, width = len(grid), len(grid[0])
    padded_grid = [["."] * (width + 3), *[[".", *row, ".", "."] for row in grid], ["."] * (width + 3)]

    gear_parts: dict[(int, int), list[int]] = {}

    for y in range(1, height + 1):
        num = ""
        num_x0 = 0
        for x in range(1, width + 2):
            c = padded_grid[y][x]
            if c.isdigit():
                if not num:
                    num_x0 = x
                num += c
            elif num:  # finished reading a number, search for adjacent part symbol
                for yn, xn in [  # all neighbor cell y,x coordinates (left, right, top row, bottom row)
                    (y, num_x0 - 1), (y, x), *[(yi, xi) for xi in range(num_x0 - 1, x + 1) for yi in (y - 1, y + 1)]
                ]:
                    if padded_grid[yn][xn] == "*":
                        # print(f"found part {num}({cn}) at yp={yn} xp={xn}, label at y={y} x={num_x0}")
                        gear_parts.setdefault((yn, xn), []).append(int(num))
                num = ""

    gear_ratios = {coord: prod(labels) for coord, labels in gear_parts.items() if len(labels) == 2}
    sum_gear_ratios = sum(gear_ratios.values())
    print(f"The sum of all gear ratios is {sum_gear_ratios}.")


TEST_INPUT = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
