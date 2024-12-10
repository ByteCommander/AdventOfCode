# Advent Of Code 2024, day 10, part 1
# http://adventofcode.com/2024/day/10
# solution by ByteCommander, 2024-12-10
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    grid: list[list[int]] = []
    open_paths: list[list[tuple[int, int]]] = []
    for y, line in enumerate(file):
        grid.append(row := [])
        for x, val in enumerate(line.strip()):
            row.append(v := int(val) if val.isnumeric() else -1)  # debug
            if v == 0:
                open_paths.append([(y, x)])
    height, width = len(grid), len(grid[0])

    trailheads: dict[tuple[int, int], set[tuple[int, int]]] = {}  # map starts (0) to all reachable destinations (9)
    while open_paths:
        path = open_paths.pop()
        y, x = path[-1]
        v = grid[y][x]
        for yn, xn in [(y, x + 1), (y, x - 1), (y + 1, x), (y - 1, x)]:
            if 0 <= yn < height and 0 <= xn < width and (vn := grid[yn][xn]) == v + 1:
                next_path = path + [(yn, xn)]
                if vn == 9:
                    head, tail = next_path[0], next_path[-1]
                    trailheads.setdefault(head, set()).add(tail)
                    # print(head, "->", tail, "via", next_path)
                else:
                    open_paths.append(next_path)

    score = sum(len(destinations) for destinations in trailheads.values())
    print(f"There are {score} possible hiking paths on the map.")


TEST_INPUT = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
