# Advent Of Code 2024, day 6, part 2, attempt 1
# http://adventofcode.com/2024/day/6
# solution by ByteCommander, 2024-12-06
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import TextIO, overload

from aoc_tools.lib import run


# Attempt 1: This approach keeps the map as a complete 2d array in memory, stores state on each element
# and lets the guard traverse between them, like in part 1.
# However, this approach is slower (~24s when limited to a single worker process) and more memory intensive.
# Multiprocessing helps cut the runtime down a bit, but not proportionally (~8s on 12 CPU threads).

def main(file: TextIO):
    grid: list[list[str]] = []
    sy, sx = -1, -1
    for yi, line in enumerate(file):
        if l := line.strip():
            grid.append(list(l))
            if "^" in l:
                sy, sx = yi, l.index("^")

    visited = walk(grid, sy, sx)
    visited.remove((sy, sx))
    print(f"Processing {len(visited)} possible positions in parallel...")
    with ProcessPoolExecutor() as executor:
        result = executor.map(partial(walk, grid, sy, sx), visited, chunksize=50)
    positions = [yx for yx, r in zip(visited, result) if r]
    # print(positions)
    print(f"There are {len(positions)} positions where placing an obstacle traps the guard in a loop.")


@overload
def walk(original_grid: list[list[str]], y: int, x: int) -> list[tuple[int, int]]: ...


@overload
def walk(original_grid: list[list[str]], y: int, x: int, obs: tuple[int, int]) -> bool: ...


def walk(original_grid: list[list[str]], y: int, x: int, obs: tuple[int, int] = None) \
    -> bool | list[tuple[int, int]]:
    """
    Simulate where the guard walks on the map.
    If no obstacle gets placed (obs_y, obs_x), this will return a list of all visited coordinates.
    Otherwise, it returns whether a loop got created by placing the obstacle or not.
    """
    grid = [[None if square == "#" else set() for square in row] for row in original_grid]
    if obs is not None:
        grid[obs[0]][obs[1]] = None  # place obstacle
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # north, east, south, west
    d = 0
    while True:
        # have we been here in this direction before? if yes, we successfully trapped the guard in a loop
        if d in grid[y][x]:
            if obs is not None:  # obstacle validation mode
                return True
            else:  # track generation mode
                break
        # mark current pos as visited, with the current direction
        grid[y][x].add(d)
        # look forward, move if free, turn if obstacle
        dy, dx = directions[d]
        if not (0 <= y + dy < len(grid) and 0 <= x + dx < len(grid[y])):
            if obs is not None:  # obstacle validation mode
                return False  # guard left the map, no loop created
            else:  # track generation mode
                break
        if grid[y + dy][x + dx] is not None:
            y, x = y + dy, x + dx
        else:
            d = (d + 1) % len(directions)
    # compute list of visited squares
    visited = [(y, x) for y, row in enumerate(grid) for x, square in enumerate(row) if square]
    return visited


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
