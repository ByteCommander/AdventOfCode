# Advent Of Code 2023, day 3, part 1
# http://adventofcode.com/2023/day/3
# solution by ByteCommander, 2023-12-11
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    grid = [list(line.strip()) for line in file]
    height, width = len(grid), len(grid[0])
    padded_grid = [["."] * (width + 3), *[[".", *row, ".", "."] for row in grid], ["."] * (width + 3)]

    part_sum = 0

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
                    if (cn := padded_grid[yn][xn]) != "." and not cn.isdigit():
                        # print(f"found part {num}({cn}) at yp={yn} xp={xn}, label at y={y} x={num_x0}")
                        part_sum += int(num)
                num = ""

    print(f"The sum of all valid part numbers is {part_sum}.")


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
