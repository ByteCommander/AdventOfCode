# Advent Of Code 2023, day 11, part 2
# http://adventofcode.com/2023/day/11
# solution by ByteCommander, 2023-12-13
from itertools import combinations
from operator import itemgetter
from typing import TextIO

from aoc_tools.lib import run

EXPANSION_FACTOR = 1_000_000  # 2 for part 1 like duplication


def main(file: TextIO):
    stars: list[(int, int, int)] = []  # y, x, id
    for y, line in enumerate(file):
        for x, char in enumerate(line.strip()):
            if char == "#":
                stars.append((y, x, len(stars) + 1))

    # to expand the universe, find empty rows/cols
    expanding_rows = []
    for y in range(max(map(itemgetter(0), stars))):
        if not any(True for star in stars if star[0] == y):
            expanding_rows.append(y)
    expanding_cols = []
    for x in range(max(map(itemgetter(1), stars))):
        if not any(True for star in stars if star[1] == x):
            expanding_cols.append(x)

    # increase coordinates of each star by the amount of expanding rows/cols before it
    stars.sort(key=itemgetter(0), reverse=True)
    for i in range(len(stars)):  # iterating manually to modify in place
        y, x, id_ = stars[i]
        stars[i] = (y + sum(EXPANSION_FACTOR - 1 for row in expanding_rows if row < y), x, id_)
    stars.sort(key=itemgetter(1), reverse=True)
    for i in range(len(stars)):  # iterating manually to modify in place
        y, x, id_ = stars[i]
        stars[i] = (y, x + sum(EXPANSION_FACTOR - 1 for col in expanding_cols if col < x), id_)

    # calculate pair distances
    distance_sum = 0
    stars.sort(key=itemgetter(2))
    for (y1, x1, id1), (y2, x2, id2) in combinations(stars, 2):
        d = abs(y1 - y2) + abs(x1 - x2)  # manhattan distance including target
        # print(f"{id1} ({y1}, {x1}) -- {id2} ({y2}, {x2}) : {d}")
        distance_sum += d

    # print(stars)
    print(f"The sum of all distances between pairs of galaxies is {distance_sum}.")


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
