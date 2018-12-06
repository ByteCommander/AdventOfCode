# Advent Of Code 2018, day 6, part 1
# http://adventofcode.com/2018/day/6
# solution by ByteCommander, 2018-12-06

from collections import Counter

with open("inputs/aoc2018_6.txt") as file:
    coords = [tuple(map(int, line.split(", "))) for line in file]
    min_x, max_x = min(x for x, y in coords), max(x for x, y in coords) + 1
    min_y, max_y = min(y for x, y in coords), max(y for x, y in coords) + 1

grid = [[None] * (max_x - min_x) for y in range(max_y - min_y)]
infinite = {None}


def closest(x, y):
    dists = sorted((abs(x - cx) + abs(y - cy), i) for i, (cx, cy) in enumerate(coords))
    return dists[0][1] if dists[0][0] != dists[1][0] else None


for y in range(max_y - min_y):
    for x in range(max_x - min_x):
        c = closest(x + min_x, y + min_y)
        if x == 0 or y == 0 or x == max_x - min_x - 1 or y == max_y - min_y - 1:
            infinite.add(c)
        grid[y][x] = c

largest_area = Counter(filter(lambda i: i not in infinite, sum(grid, []))).most_common(1)[0][1]

print(f"The largest area is {largest_area} squares big.")
