# Advent Of Code 2023, day 21, part 2
# http://adventofcode.com/2023/day/21
# solution by ByteCommander, 2023-12-21
from operator import itemgetter
from typing import TextIO

from aoc_tools.lib import run

STEPS = 1000  # 26501365
PLOT, ROCK, START = ".#S"


def main(file: TextIO):
    grid: tuple[tuple[str, ...], ...] = tuple(tuple(line.strip()) for line in file)
    height, width = len(grid), len(grid[0])
    edge: set[(int, int)] = set()
    prev_edge: set[(int, int)] = set()
    center_odd, center_even = 0, 0
    start_is_even: bool = False

    for y, row in enumerate(grid):
        if START in row:
            x = row.index(START)
            start_is_even = y % 2 == x % 2
            edge.add((y, x))

    # The reachable plots acts similar to an ever expanding area, where each field that has been reached once
    # will then continue to "blink" reachable and unreachable every other step.
    # Categorizing fields as "even field" (x and y are both even or both odd numbers) or "odd field" (x is even and
    # y is odd or the other way round), after an even amount of steps, all previously seen fields that are equally
    # "even" or "odd" as the start field will be reachable.
    # Therefore, we only have to simulate the growing edge and can then compute the number of currently reachable
    # center fields once at the end.

    for i in range(1, STEPS + 1):
        center_even += (e_even := sum(1 for y, x in edge if y % 2 == x % 2))
        center_odd += len(edge) - e_even
        next_edge: set[(int, int)] = set()
        for y, x in edge:
            next_edge |= {
                (ny, nx) for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1))
                if ((ny := y + dy), (nx := x + dx)) not in prev_edge and grid[ny % height][nx % width] != ROCK
            }
        prev_edge = edge
        edge = next_edge
        print(i, len(edge), center_odd, center_even, )
        #visualize(grid, edge, set(), i % 2 == 0)

    reachable_center_count = [center_odd, center_even][start_is_even is (i % 2 == 0)]
    print(f"After {STEPS} steps, the elf can end up on {len(edge) + reachable_center_count} different garden plots.")


def visualize(grid: tuple[tuple[str, ...], ...], edge: set[tuple[int, int]], center: set[tuple[int, int]], even: bool):
    height, width = len(grid), len(grid[0])
    ymin = (min(map(itemgetter(0), edge)) // height) * height
    ymax = (max(map(itemgetter(0), edge)) // height + 1) * height
    xmin = (min(map(itemgetter(1), edge)) // width) * width
    xmax = (max(map(itemgetter(1), edge)) // width + 1) * width

    for y in range(ymin - 1, ymax + 1):
        print("".join(
            "O" if (y, x) in edge else "X" if (y, x) in center and (y % 2 == x % 2) is even else grid[y % height][
                x % width]
            for x in range(xmin - 1, xmax + 1)
        ))




TEST_INPUT_ORIGINAL = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

# like in the real input, ensuring that the start row/column are unobstructed, so that the area expansion is ideal
TEST_INPUT = """
...........
......##.#.
.###..#..#.
..#.#...#..
....#.#....
.....S.....
.##......#.
.......##..
.##.#.####.
.##...#.##.
...........
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
