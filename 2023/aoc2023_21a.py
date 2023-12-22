# Advent Of Code 2023, day 21, part 1
# http://adventofcode.com/2023/day/21
# solution by ByteCommander, 2023-12-21
from typing import TextIO

from aoc_tools.lib import run

STEPS = 64
PLOT, ROCK, START = ".#S"


def main(file: TextIO):
    grid = tuple(tuple(line.strip()) for line in file)
    height, width = len(grid), len(grid[0])
    positions: set[(int, int)] = set()
    for y, row in enumerate(grid):
        if START in row:
            positions.add((y, row.index(START)))

    for i in range(STEPS):
        next_positions: set[(int, int)] = set()
        for y, x in positions:
            next_positions |= {
                (ny, nx) for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1))
                if 0 <= (ny := y + dy) < height and 0 <= (nx := x + dx) < width and grid[ny][nx] != ROCK
            }
        positions = next_positions
        # print(i + 1, len(positions), positions)
        # print(*["".join("O" if (y, x) in positions else grid[y][x] for x in range(len(grid[y])))
        #         for y in range(len(grid))], sep="\n")

    print(f"After {STEPS} steps, the elf can end up on {len(positions)} different garden plots.")


TEST_INPUT = """
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

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
