# Advent Of Code 2024, day 15, part 2
# http://adventofcode.com/2024/day/15
# solution by ByteCommander, 2024-12-17
from typing import TextIO

from aoc_tools.lib import run

ROBOT = "@"
BOX = "O"
BOX_L, BOX_R = "[]"
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
        grid.append(list("".join(
            BOX_L + BOX_R if tile == BOX else ROBOT + FREE if tile == ROBOT else tile * 2 for tile in line
        )))
    while line := next(file_it, "").strip():  # read until next blank line / end of file
        moves.extend(line)

    ry = next(y for y, row in enumerate(grid) if ROBOT in row)
    rx = grid[ry].index(ROBOT)
    grid[ry][rx] = FREE

    move = ROBOT
    for move in moves:
        my, mx = MOVES[move]
        pushing: list[set[tuple[int, int]]] = []  # list of layers of box coordinates to push
        frontier: set[tuple[int, int]] = {(ry, rx)}
        while frontier:
            pushing.append(frontier)
            ahead: set[tuple[int, int]] = set()
            for fy, fx in frontier:
                ay, ax = fy + my, fx + mx
                at = grid[ay][ax]
                if at == WALL:  # robot or box frontier hits a wall, no movement in this direction possible
                    break
                elif at in (BOX_L, BOX_R):  # hits a box half, include it in the next layer of boxes getting pushed
                    ahead.add((ay, ax))
                    if my:  # if moving vertically, include the other half of the box ahead as well
                        ahead.add((ay, ax + 1 if at == BOX_L else ax - 1))
                else:
                    pass  # free tile ahead of frontier, continue checking the rest
            else:
                frontier = ahead
                continue
            break  # break outer loop if inner loop was broken
        else:  # enough space to move/push, so walk forward
            for layer in reversed(pushing):  # farthest layer first, to not overwrite nearer ones
                for y, x in layer:
                    grid[y + my][x + mx] = grid[y][x]
                    grid[y][x] = FREE
            ry, rx = ry + my, rx + mx

    print(*[
        "".join(move if (ry, rx) == (y, x) else tile for x, tile in enumerate(row)) for y, row in enumerate(grid)
    ], sep="\n")

    gps = sum(sum(100 * y + x for x, tile in enumerate(row) if tile == BOX_L) for y, row in enumerate(grid))
    print(f"The sum of all boxes' GPS coordinates is {gps}.")


TEST_INPUT_SMALL = """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
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
    run(main, TEST_INPUT_SMALL, test_only=True)
    run(main, TEST_INPUT, test_only=False)
