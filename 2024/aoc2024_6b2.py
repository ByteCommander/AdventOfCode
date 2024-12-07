# Advent Of Code 2024, day 6, part 2, attempt 2
# http://adventofcode.com/2024/day/6
# solution by ByteCommander, 2024-12-06
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import TextIO, overload

from aoc_tools.lib import run


# Attempt 2: This approach converts the 2d input grid into just a set of blocked coordinates, storing only
# information about actually visited and relevant squares in a dictionary instead, for greater efficiency.
# This approach is faster (~9s when limited to a single worker process) and needs less memory.
# Multiprocessing helps cut the runtime down a bit, but not proportionally (~2.5s on 12 CPU threads).
# There are some more small speed optimizations identified through profiling, commented in the code.

# Probably there would be an opportunity for caching traversed path fragments somehow, for further optimization.

def main(file: TextIO):
    grid: list[list[str]] = []
    start = -1, -1
    for yi, line in enumerate(file):
        if l := line.strip():
            grid.append(list(l))
            if "^" in l:
                start = yi, l.index("^")
    size = len(grid), len(grid[0])
    blocks = frozenset((y, x) for y, row in enumerate(grid) for x, square in enumerate(row) if square == "#")

    visited = walk(blocks, size, start)
    visited.remove(start)

    print(f"Processing {len(visited)} possible positions in parallel...")
    with ProcessPoolExecutor() as executor:
        result = executor.map(partial(walk, blocks, size, start), visited, chunksize=50)
    # result = [walk(blocks, size, start, obs) for obs in visited]  # single process alternative for profiling
    positions = [yx for yx, r in zip(visited, result) if r]

    # print(positions)
    print(f"There are {len(positions)} positions where placing an obstacle traps the guard in a loop.")


@overload
def walk(
    blocks: frozenset[tuple[int, int]], size: tuple[int, int], pos: tuple[int, int]
) -> list[tuple[int, int]]: ...


@overload
def walk(
    blocks: frozenset[tuple[int, int]], size: tuple[int, int], pos: tuple[int, int], obs: tuple[int, int]
) -> bool: ...


def walk(
    blocks: frozenset[tuple[int, int]], size: tuple[int, int], pos: tuple[int, int], obs: tuple[int, int] = None
) -> bool | list[tuple[int, int]]:
    """
    Simulate where the guard (starting at pos: (y, x)) walks on a map of size: (height, width)
    with the given positions of blocks: {(y, x), ...}.
    If no extra obstacle gets placed (obs: (y, x)), this will return a list of all visited coordinates.
    Otherwise, it returns whether a loop got created by placing the obstacle or not.
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # north, east, south, west
    d = 0
    visited: dict[tuple[int, int], set[int]] = {}  # map visited square coordinates to passed directions
    while 0 <= pos[0] < size[0] and 0 <= pos[1] < size[1]:
        # have we been here in this direction before? if yes, we successfully trapped the guard in a loop
        if pos in visited:
            if d in visited[pos]:  # detected a loop
                break
            # mark current pos as visited, with the current direction
            visited[pos].add(d)
        else:  # dict.setdefault seems significantly slower because of the expensive default constructor call each time
            visited[pos] = {d}

        # look forward, move if free, turn if obstacle
        next_pos = (pos[0] + directions[d][0], pos[1] + directions[d][1])
        if next_pos in blocks or next_pos == obs:  # would walk into block/obstacle, turn right instead
            d = (d + 1) % len(directions)
        else:
            pos = next_pos

    else:  # guard left the map
        if obs:
            return False  # obstacle check mode -> failed

    return True if obs else list(visited.keys())  # guard left the map, no loop created


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
