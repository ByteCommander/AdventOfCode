# Advent Of Code 2018, day 6, part 2
# http://adventofcode.com/2018/day/6
# solution by ByteCommander, 2018-12-06

with open("inputs/aoc2018_6.txt") as file:
    coords = [tuple(map(int, line.split(", "))) for line in file]
    min_x, max_x = min(x for x, y in coords), max(x for x, y in coords) + 1
    min_y, max_y = min(y for x, y in coords), max(y for x, y in coords) + 1

area_size = sum(
    sum(abs(x - cx) + abs(y - cy) for cx, cy in coords) < 10000
    for y in range(min_y, max_y)
    for x in range(min_x, max_x)
)

print(f"The largest area is {area_size} squares big.")
