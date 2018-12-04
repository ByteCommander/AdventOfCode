# Advent Of Code 2018, day 3, part 1
# http://adventofcode.com/2018/day/3
# solution by ByteCommander, 2018-12-03

import re

fabric = {}  # maps (x, y) coordinate tuples to num of claims for that square

with open("inputs/aoc2018_3.txt") as file:
    for line in file:
        i, x, y, w, h = map(int, re.match(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line).groups())
        for xx in range(x, x + w):
            for yy in range(y, y + h):
                fabric[(xx, yy)] = fabric.get((xx, yy), 0) + 1

overlaps = sum(1 for count in fabric.values() if count > 1)

print(f"The claims contain {overlaps} overlapping square inches.")
