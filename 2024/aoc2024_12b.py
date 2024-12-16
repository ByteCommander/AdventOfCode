# Advent Of Code 2024, day 12, part 2
# http://adventofcode.com/2024/day/12
# solution by ByteCommander, 2024-12-16
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    grid: list[list[str]] = []
    for line in file:
        if l := line.strip():
            grid.append([" "] + list(l) + [" "])  # plus horizontal padding
    width = len(grid[0])
    grid = [[" "] * width] + grid + [[" "] * width]  # plus vertical padding

    seen: set[tuple[int, int]] = set()
    # regions: label -> (set of plots, set of edges as included/excluded plot pair)
    regions: dict[str, tuple[set[tuple[int, int]], set[tuple[tuple[int, int], tuple[int, int]]]]] = {}
    for y, row in enumerate(grid[1:-1], 1):
        for x, label in enumerate(row[1:-1], 1):
            if (y, x) in seen:
                continue
            # new region spotted, flood fill to find all connected plots with same label
            flooded: set[tuple[int, int]] = set()
            frontier: set[tuple[int, int]] = {(y, x)}
            edges: set[tuple[tuple[int, int], tuple[int, int]]] = set()
            while frontier:
                fy, fx = frontier.pop()
                flooded.add((fy, fx))
                for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                    ny, nx = fy + dy, fx + dx
                    if (ny, nx) not in flooded:
                        if grid[ny][nx] == label:
                            frontier.add((ny, nx))
                        else:
                            edges.add(((fy, fx), (ny, nx)))  # edge = included plot, excluded plot
            regions[f"{label}({y},{x})"] = (flooded, edges)
            seen.update(flooded)

    total = 0
    for label, (plots, edges) in regions.items():
        area = len(plots)
        sides = 0

        for (iy, ix), (ey, ex) in edges:
            if iy == ey and ((iy - 1, ix), (ey - 1, ex)) not in edges:
                sides += 1  # found a horizontal edge with no direct lower neighbor, so it's the start of a new side
            if ix == ex and ((iy, ix - 1), (ey, ex - 1)) not in edges:
                sides += 1  # found a vertical edge with no direct lower neighbor, so it's the start of a new side

        price = area * sides
        # print(f"{label:12s} {area:3n} * {sides:3n} = {price:6n}")
        total += price
    print(f"The total price for all fences in {total}.")


TEST_INPUT = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
