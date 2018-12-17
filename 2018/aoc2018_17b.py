# Advent Of Code 2018, day 17, part 2
# http://adventofcode.com/2018/day/17
# solution by ByteCommander, 2018-12-17

import re
from itertools import count
from math import inf

SPRING_X, SPRING_Y = 500, 0
clay = {}
xmin, xmax, ymin, ymax = inf, -inf, inf, -inf

with open("inputs/aoc2018_17.txt") as file:
    for line in file:
        xy, val1, r2low, r2high = re.match(r"([xy])=(\d+), [xy]=(\d+)\.\.(\d+)", line).groups()
        for val2 in range(int(r2low), int(r2high) + 1):
            x = int(val1 if xy == "x" else val2)
            y = int(val1 if xy == "y" else val2)
            clay.setdefault(y, []).append(x)
            xmin, xmax = min(xmin, x), max(xmax, x)
            ymin, ymax = min(ymin, y), max(ymax, y)

xmin, xmax, ymin = xmin - 1, xmax + 1, ymin - 1
# print(f"x: {xmin}..{xmax}, y: {ymin}..{ymax}")

world = [["."] * (xmax - xmin + 1) for _ in range(ymin, ymax + 1)]
for y, row in clay.items():
    for x in row:
        world[y - ymin][x - xmin] = "#"


def show():
    for x, row in enumerate(world):
        print("".join(row), f"{x:04}")
    print()
    print(*map("".join, zip(*(f"{x:03}" for x in range(len(world[0]))))), sep="\n")
    print()


# Start pouring water:
# Assume spring is always above the scanned world (SPRING_Y < ymin).

tasks = set()
tasks.add((True, SPRING_X - xmin, 0))

while tasks:
    falling, x, y = tasks.pop()
    # show()
    # print(falling, x, y, tasks)

    if falling:
        while world[y + 1][x] in ".|":
            world[y + 1][x] = "|"
            y += 1
            if y >= len(world) - 1:
                break
        else:
            tasks.add((False, x, y))

    else:
        walls_hit = 0

        for direction in (-1, 1):
            for xx in count(x, direction):
                if world[y][xx] in "|.":
                    world[y][xx] = "|"
                    if world[y + 1][xx] in ".|":
                        tasks.add((True, xx, y))
                        break
                else:
                    walls_hit += 1
                    break

        if walls_hit == 2:
            for direction in (-1, 1):
                for xx in count(x, direction):
                    if world[y][xx] in "|~":
                        world[y][xx] = "~"
                    else:
                        break
            tasks.add((False, x, y - 1))

show()

wet_fields = sum(1 for row in world for field in row if field in "~")
print(f"When the spring dries out, {wet_fields} fields will retain water.")
