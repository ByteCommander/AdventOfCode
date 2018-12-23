# Advent Of Code 2018, day 23, part 1
# http://adventofcode.com/2018/day/23
# solution by ByteCommander, 2018-12-23

import re

bots = []

with open("inputs/aoc2018_23.txt") as file:
    for line in file:
        x, y, z, r = map(int, re.match(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line).groups())
        bots.append((r, x, y, z))

strongest_r, *strongest_xyz = max(bots)

in_range = sum(1 for bot in bots if sum(abs(c1 - c2) for c1, c2 in zip(bot[1:], strongest_xyz)) <= strongest_r)

print(f"The strongest nanobot has {in_range} bots in its signal range, including itself.")
