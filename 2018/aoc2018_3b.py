# Advent Of Code 2018, day 3, part 2
# http://adventofcode.com/2018/day/3
# solution by ByteCommander, 2018-12-03

import re

fabric = {}  # maps (x, y) coordinate tuples to list of claim ids for that square
free_ids = set()

with open("inputs/aoc2018_3.txt") as file:
    for line in file:
        i, x, y, w, h = map(int, re.match(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line).groups())
        free_ids.add(i)
        for xx in range(x, x + w):
            for yy in range(y, y + h):
                square_ids = fabric.setdefault((xx, yy), [])
                square_ids.append(i)
                if len(square_ids) > 1:
                    free_ids.difference_update(square_ids)

print(f"Only the claim {free_ids} has no overlap.")
