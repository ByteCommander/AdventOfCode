# Advent Of Code 2023, day 14, part 2
# http://adventofcode.com/2023/day/14
# solution by ByteCommander, 2023-12-16
from typing import TextIO

from aoc_tools.lib import run

BLOCK = "#"
ROCK = "O"
EMPTY = "."

CYCLES = 1_000_000_000


def main(file: TextIO):
    grid: list[list[str]] = []
    for line in file:
        grid.append(list(line.strip()))

    cache: dict[str, int] = {}
    cy_start, cy_len = 0, 0
    for i in range(CYCLES):
        serialized = "\n".join(map("".join, grid))
        if serialized in cache:
            cy_start = cache[serialized]
            cy_len = i - cy_start
            print("cycle loop found at", i, "back to cycle", cy_start)
            break
        else:
            cache[serialized] = i

        tilt(grid, -1, 0)  # north
        tilt(grid, 0, -1)  # west
        tilt(grid, 1, 0)  # south
        tilt(grid, 0, 1)  # east
        # print(f"After {i + 1} cycles:", *["".join(row) for row in grid], sep="\n", end="\n\n")

    inv_cache: dict[int, str] = {v: k for k, v in cache.items()}  # invert cache to look up grid state by index
    cy_idx = cy_start + (CYCLES - cy_start) % cy_len
    grid = [list(row) for row in inv_cache[cy_idx].splitlines()]
    # print(f"After {CYCLES} cycles (same as after {cy_idx}):", *["".join(row) for row in grid], sep="\n")

    load = sum(row.count(ROCK) * (len(grid) - i) for i, row in enumerate(grid))
    print(f"The north support beam load after {CYCLES} cycles is {load}.")


def tilt(grid: list[list[str]], dy: int, dx: int) -> None:
    # Tilt platform, so that all rocks roll straight in that direction.
    # Set exactly one of dy,dx to 1 or -1 to control the direction, e.g. dy=-1,dx=0 is north.
    for y in range(len(grid) - 1, -1, -1) if dy == 1 else range(len(grid)):
        for x in range(len(grid[y]) - 1, -1, -1) if dx == 1 else range(len(grid[y])):
            if grid[y][x] == ROCK:
                yn, xn = y, x
                while dy and 0 <= yn + dy < len(grid) and grid[yn + dy][x] == EMPTY:
                    yn += dy
                while dx and 0 <= xn + dx < len(grid[y]) and grid[y][xn + dx] == EMPTY:
                    xn += dx
                grid[y][x] = EMPTY
                grid[yn][xn] = ROCK


TEST_INPUT = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
