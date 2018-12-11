# Advent Of Code 2018, day 10, part 1
# http://adventofcode.com/2018/day/10
# solution by ByteCommander, 2018-12-10

import re

lights = []

with open("inputs/aoc2018_10.txt") as file:
    for line in file:
        x, y, dx, dy = map(int, re.match(
            r"position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>", line
        ).groups())
        lights.append(([x, y], (dx, dy)))

seconds = -1
prev_area = None
while True:
    xmin = min(x for (x, y), _ in lights)
    xmax = max(x for (x, y), _ in lights)
    ymin = min(y for (x, y), _ in lights)
    ymax = max(y for (x, y), _ in lights)
    area = (xmax - xmin) * (ymax - ymin)

    if prev_area and area > prev_area:
        # undo last step
        for pos, delta in lights:
            pos[:] = [pos[0] - delta[0], pos[1] - delta[1]]

        for y in range(ymin, ymax + 1):
            print("".join(
                "#" if [x, y] in (pos for pos, delta in lights) else "."
                for x in range(xmin, xmax + 1)
            ))
        break

    prev_area = area
    seconds += 1

    for pos, delta in lights:
        pos[:] = [pos[0] + delta[0], pos[1] + delta[1]]

print(f"Waiting for this solution would have taken {seconds} seconds.")
