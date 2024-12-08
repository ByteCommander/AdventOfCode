# Advent Of Code 2024, day 8, part 1
# http://adventofcode.com/2024/day/8
# solution by ByteCommander, 2024-12-08
from itertools import combinations
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    antennas: dict[str, list[tuple[int, int]]] = {}
    height, width = 0, 0
    for y, line in enumerate(file):
        width = len(l := line.strip())
        height += bool(l)
        for x, v in enumerate(l):
            if v != ".":
                antennas.setdefault(v, []).append((y, x))

    antinodes: set[tuple[int, int]] = set()
    for v, position_list in antennas.items():
        for (ya, xa), (yb, xb) in combinations(position_list, 2):
            dy, dx = ya - yb, xa - xb
            for yn, xn in [(ya + dy, xa + dx), (yb - dy, xb - dx)]:
                if 0 <= yn < height and 0 <= xn < width:
                    # print(v, ":", (ya, xa), (yb, xb), "->", (yn, xn))
                    antinodes.add((yn, xn))

    ant_rev: dict[tuple[int, int], str] = {v: k for k, vl in antennas.items() for v in vl}
    for y in range(height):
        print("".join(ant_rev.get((y, x), "#" if (y, x) in antinodes else ".") for x in range(width)))

    # print(antinodes)
    print(f"There are {len(antinodes)} unique antinodes on the map.")


TEST_INPUT = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
