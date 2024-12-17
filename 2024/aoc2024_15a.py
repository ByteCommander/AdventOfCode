# Advent Of Code 2024, day 15, part 1
# http://adventofcode.com/2024/day/15
# solution by ByteCommander, 2024-12-17
from itertools import count
from typing import TextIO

from aoc_tools.lib import run

ROBOT = "@"
BOX = "O"
WALL = "#"
FREE = "."

MOVES = {  # (y, x) steps
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


def main(file: TextIO):
    file_it = iter(file)
    grid: list[list[str]] = []
    moves: list[str] = []
    while line := next(file_it).strip():  # read until first blank line
        grid.append(list(line))
    while line := next(file_it, "").strip():  # read until next blank line / end of file
        moves.extend(line)

    ry = next(y for y, row in enumerate(grid) if ROBOT in row)
    rx = grid[ry].index(ROBOT)
    grid[ry][rx] = FREE

    move = ROBOT
    for move in moves:
        my, mx = MOVES[move]
        pushing = False
        for i in count(1):
            iy, ix = ry + i * my, rx + i * mx
            if grid[iy][ix] == WALL:
                break  # no movement in this direction possible
            elif grid[iy][ix] == BOX:
                pushing = True  # must push boxes to move in this direction
            elif pushing:  # free tile, but already pushing boxes, so move the closest box in here and move forward
                ry, rx = ry + my, rx + mx
                grid[iy][ix] = BOX
                grid[ry][rx] = FREE
                break
            else:  # free tile, not pushing anything, just move
                ry, rx = ry + my, rx + mx
                break

    print(*[
        "".join(move if (ry, rx) == (y, x) else tile for x, tile in enumerate(row)) for y, row in enumerate(grid)
    ], sep="\n")

    gps = sum(sum(100 * y + x for x, tile in enumerate(row) if tile == BOX) for y, row in enumerate(grid))
    print(f"The sum of all boxes' GPS coordinates is {gps}.")


TEST_INPUT_SMALL = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""

TEST_INPUT = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

if __name__ == "__main__":
    # run(main, TEST_INPUT_SMALL, test_only=True)
    run(main, TEST_INPUT, test_only=False)
