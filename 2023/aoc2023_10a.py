# Advent Of Code 2023, day 10, part 1
# http://adventofcode.com/2023/day/10
# solution by ByteCommander, 2023-12-13
from enum import Flag, auto
from typing import TextIO

from aoc_tools.lib import run


class Dir(Flag):
    N = auto()
    E = auto()
    S = auto()
    W = auto()


PIPES: dict[str, Dir] = {  # directions in which each pipe tile has outgoing connections
    "|": Dir.N | Dir.S,
    "-": Dir.E | Dir.W,
    "L": Dir.N | Dir.E,
    "J": Dir.N | Dir.W,
    "7": Dir.S | Dir.W,
    "F": Dir.E | Dir.S,
    ".": Dir(0),
    "S": Dir(0),  # start/dead end
}


def main(file: TextIO):
    grid: list[list[Dir]] = []
    start_y, start_x = -1, -1

    for y, line in enumerate(file):
        l = list(line.strip())
        grid.append([PIPES[p] for p in l])
        if "S" in l:
            start_y, start_x = (y, l.index("S"))
    max_y, max_x = len(grid) - 1, len(grid[0]) - 1

    if start_y > 0 and Dir.S in grid[start_y - 1][start_x]:  # try if north is connected
        py, px, p_from = start_y - 1, start_x, Dir.S
    elif start_y < max_y and Dir.N in grid[start_y + 1][start_x]:  # try if south is connected
        py, px, p_from = start_y + 1, start_x, Dir.N
    elif start_x > 0 and Dir.E in grid[start_y][start_x - 1]:  # try if west is connected
        py, px, p_from = start_y, start_x - 1, Dir.E
    elif start_x < max_x and Dir.W in grid[start_y][start_x + 1]:  # try if east is connected
        py, px, p_from = start_y, start_x - 1, Dir.W
    else:
        raise ValueError("disconnected start tile")

    pipe: list[(int, int)] = [(py, px)]
    while py != start_y or px != start_x:
        p_to = grid[py][px] ^ p_from
        if p_to == Dir.N:
            py, p_from = py - 1, Dir.S
        elif p_to == Dir.S:
            py, p_from = py + 1, Dir.N
        elif p_to == Dir.W:
            px, p_from = px - 1, Dir.E
        elif p_to == Dir.E:
            px, p_from = px + 1, Dir.W
        else:
            raise ValueError("dead end")
        pipe.append((py, px))

    print(f"The farthest point in the pipe is {len(pipe) // 2} tiles away from the start.")


TEST_INPUT = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
