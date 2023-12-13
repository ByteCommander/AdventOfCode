# Advent Of Code 2023, day 11, part 1
# http://adventofcode.com/2023/day/11
# solution by ByteCommander, 2023-12-13
from itertools import combinations
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    grid: list[list[int]] = []
    star_counter = 0
    for line in file:
        grid.append([0 if char == "." else (star_counter := star_counter + 1) for char in line.strip()])

    # expand the universe
    expand_vertically(grid)
    grid_trans = transposed(grid)
    expand_vertically(grid_trans)
    grid = transposed(grid_trans)

    # find stars
    stars: dict[int, (int, int)] = {}
    for y, row in enumerate(grid):
        for x, field in enumerate(row):
            if field > 0:
                stars[field] = (y, x)

    # calculate pair distances
    distance_sum = 0
    for s1, s2 in combinations(stars, 2):
        (y1, x1), (y2, x2) = stars[s1], stars[s2]
        d = abs(y1 - y2) + abs(x1 - x2)  # manhattan distance including target
        # print(f"{s1} ({y1}, {x1}) -- {s2} ({y2}, {x2}) : {d}")
        distance_sum += d

    # print(*grid, sep="\n", end="\n\n")

    print(f"The sum of all distances between pairs of galaxies is {distance_sum}.")


def expand_vertically(grid: list[list[int]]):
    y = 0
    while y < len(grid):
        if all(a == 0 for a in grid[y]):  # find rows without stars
            grid.insert(y, list(grid[y]))  # insert a copy of the row
            y += 1
        y += 1


def transposed(grid: list[list[int]]):  # return copy with transposed rows and columns
    return [list(col) for col in zip(*grid)]


TEST_INPUT = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
