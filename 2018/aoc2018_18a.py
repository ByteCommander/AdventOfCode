# Advent Of Code 2018, day 18, part 1
# http://adventofcode.com/2018/day/18
# solution by ByteCommander, 2018-12-18

from collections import Counter
from itertools import chain

area = []

with open("inputs/aoc2018_18.txt") as file:
    for line in file:
        area.append(list(line.strip()))

for i in range(10):
    # print(f"\nAfter {i} minutes:")
    # print(*map("".join, area), sep="\n")

    next_area = [[field for field in row] for row in area]

    for y in range(len(area)):
        for x in range(len(area[y])):
            neighbors = Counter(
                area[yy][xx] for (yy, xx) in (
                    (y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
                    (y, x - 1), (y, x + 1),
                    (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)
                ) if 0 <= yy < len(area) and 0 <= xx < len(area[yy])
            )

            if area[y][x] == "." and neighbors["|"] >= 3:
                next_area[y][x] = "|"
            if area[y][x] == "|" and neighbors["#"] >= 3:
                next_area[y][x] = "#"
            if area[y][x] == "#" and (neighbors["#"] == 0 or neighbors["|"] == 0):
                next_area[y][x] = "."

    area = next_area

i += 1
print(f"\nAfter {i} minutes:")
print(*map("".join, area), sep="\n")

counter = Counter(chain(*area))
print(f"\nThe total resource value after {i} minutes is {counter['#'] * counter['|']}.")
