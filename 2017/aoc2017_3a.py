# Advent Of Code 2017, day 3, part 1
# http://adventofcode.com/2017/day/3
# solution by ByteCommander, 2017-12-03

import math

with open("inputs/aoc2017_3.txt") as file:
    n = int(file.read().strip())
    n_sqrt = int(math.ceil(math.sqrt(n)))
    width = n_sqrt + (1 - n_sqrt % 2)
    grid = [[0 for _x in range(width)] for _y in range(width)]

    x = y = c = width // 2
    grid[y][x] = 1
    i, direction = 1, "s"  # south, east, north, west

    while i < n:
        i += 1

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

        grid[y][x] = i

        # for row in grid:
        #     print(*["%3d" % v for v in row])
        # print()

    print("Answer: Distance from {} to center is {}"
          .format(n, abs(x - c) + abs(y - c)))
