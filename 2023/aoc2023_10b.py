# Advent Of Code 2023, day 10, part 2
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
    X = auto()  # special


PIPES: dict[str, Dir] = {  # directions in which each pipe tile has outgoing connections
    "|": Dir.N | Dir.S,
    "-": Dir.E | Dir.W,
    "L": Dir.N | Dir.E,
    "J": Dir.N | Dir.W,
    "7": Dir.S | Dir.W,
    "F": Dir.E | Dir.S,
    ".": Dir(0),
    "S": Dir.X,  # start/dead end
}


def main(file: TextIO):
    grid: list[list[str]] = []
    start_y, start_x = -1, -1

    for y, line in enumerate(file):
        l = list(line.strip())
        grid.append(l)
        if "S" in l:
            start_y, start_x = (y, l.index("S"))
    max_y, max_x = len(grid) - 1, len(grid[0]) - 1

    if start_y > 0 and Dir.S in PIPES[grid[start_y - 1][start_x]]:  # try if north is connected
        py, px, p_from = start_y - 1, start_x, Dir.S
    elif start_y < max_y and Dir.N in PIPES[grid[start_y + 1][start_x]]:  # try if south is connected
        py, px, p_from = start_y + 1, start_x, Dir.N
    elif start_x > 0 and Dir.E in PIPES[grid[start_y][start_x - 1]]:  # try if west is connected
        py, px, p_from = start_y, start_x - 1, Dir.E
    elif start_x < max_x and Dir.W in PIPES[grid[start_y][start_x + 1]]:  # try if east is connected
        py, px, p_from = start_y, start_x - 1, Dir.W
    else:
        raise ValueError("disconnected start tile")

    pipe: list[(int, int)] = [(py, px)]
    while py != start_y or px != start_x:
        p_to = PIPES[grid[py][px]] ^ p_from
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

    # clear out junk pipe fragments and remember the first encountered loop pipe tile (should always be an "F" corner)
    first_y, first_x = -1, -1
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (y, x) not in pipe:
                grid[y][x] = "."
            elif first_y == -1:
                first_y, first_x = y, x

    # Walk along the pipe from the first touch point (top-leftmost "F" corner) clockwise (East next),
    # flood-filling all areas on the right hand side in walking direction, to mark all enclosed tiles.
    enclosed_count = 0

    # normalize the pipe segment list to start at our first touch point corner and go clockwise from there
    first_i = pipe.index((first_y, first_x))
    if pipe[first_i + 1][0] != pipe[first_i][0]:  # next pipe segment is below, so we flip the order
        pipe.reverse()
    pipe = pipe[first_i:] + pipe[:first_i]  # rotate our first point to the beginning of the pipe ring list

    # loop over each pipe segment while also looking at its connected segments "before" and "after"
    for (yb, xb), (y, x), (ya, xa) in zip(pipe[-1:] + pipe[:-1], pipe, pipe[1:] + pipe[:1]):
        # Look around current pos, starting at pos "before", going counter-clockwise, until reaching next-pos.
        # This finds adjacent free tiles on the right hand side of the pipe, for flood-filling as enclosed space.
        neighbors = [(y - 1, x), (y, x - 1), (y + 1, x), (y, x + 1)]  # neighbors of (y,x) ordered counter-clockwise
        ni = neighbors.index((yb, xb))
        for yn, xn in neighbors[ni + 1:] + neighbors[:ni]:  # loop around, starting behind the pos "before"
            if (yn, xn) == (ya, xa):  # hitting next pipe segment, so we finished the right hand side
                break
            elif grid[yn][xn] == ".":  # right hand side neighbor tile is free, start flooding
                enclosed_count += flood(grid, yn, xn)

    # print(*map("".join, grid), sep="\n")

    print(f"The pipe loop encloses {enclosed_count} tiles.")


def flood(grid: list[list[str]], y: int, x: int) -> int:
    grid[y][x] = "#"
    count = 1
    for yn, xn in [(y - 1, x), (y, x - 1), (y + 1, x), (y, x + 1)]:
        if grid[yn][xn] == ".":
            count += flood(grid, yn, xn)
    return count


TEST_INPUT = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
