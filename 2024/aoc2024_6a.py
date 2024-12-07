# Advent Of Code 2024, day 6, part 1
# http://adventofcode.com/2024/day/6
# solution by ByteCommander, 2024-12-06
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    grid: list[list[str]] = []
    y, x = -1, -1
    for yi, line in enumerate(file):
        if l := line.strip():
            grid.append(list(l))
            if "^" in l:
                y, x = yi, l.index("^")

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # north, east, south, west
    d = 0
    while True:
        # mark current pos as visited
        grid[y][x] = "x"
        # look forward, move if free, turn if obstacle
        dy, dx = directions[d]
        if not (0 <= y + dy < len(grid) and 0 <= x + dx < len(grid[y])):
            break
        if grid[y + dy][x + dx] != "#":
            y, x = y + dy, x + dx
        else:
            d = (d + 1) % len(directions)

    # print(*["".join(row) for row in grid], sep="\n")
    count = sum(sum(square == "x" for square in row) for row in grid)
    print(f"The guard will visit {count} squares on the map before leaving.")


TEST_INPUT = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
