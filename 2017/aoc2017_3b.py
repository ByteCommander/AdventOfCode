# Advent Of Code 2017, day 3, part 2
# http://adventofcode.com/2017/day/3
# solution by ByteCommander, 2017-12-03

import math


def grow_grid(gr):
    return [[0] * (len(gr) + 2)] + \
           [[0] + ro + [0] for ro in gr] + \
           [[0] * (len(gr) + 2)]


def sum_neighbours(gr, x0, y0):
    nsum = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx != 0 or dy != 0) and x0 + dx < len(gr):
                nsum += grid[y0 + dy][x0 + dx]
    return nsum


with open("inputs/aoc2017_3.txt") as file:
    n = int(file.read().strip())
    grid = grow_grid([[1]])

    x = y = len(grid) // 2
    i, direction = 1, "s"  # south, east, north, west

    while i < n:

        if direction == "s" and grid[y][x + 1] == 0:  # can turn east
            direction = "e"
        elif direction == "e" and grid[y - 1][x] == 0:  # can turn north
            direction = "n"
        elif direction == "n" and grid[y][x - 1] == 0:  # can turn west
            direction = "w"
        elif direction == "w" and grid[y + 1][x] == 0:  # can turn south
            direction = "s"

        if direction == "s":
            y += 1
        elif direction == "e":
            x += 1
        elif direction == "n":
            y -= 1
        elif direction == "w":
            x -= 1

        i = sum_neighbours(grid, x, y)
        grid[y][x] = i

        if x == len(grid) - 1:
            grid = grow_grid(grid)
            x += 1
            y += 1

        # for row in grid:
        #     print(*["%3d" % v for v in row])
        # print()

    c = len(grid) // 2
    print("Answer: {} is the first value larger than {}"
          .format(i, n))
