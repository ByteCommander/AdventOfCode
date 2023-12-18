# Advent Of Code 2023, day 18, part 2
# http://adventofcode.com/2023/day/18
# solution by ByteCommander, 2023-12-18
from typing import Iterable, TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    # read instructions: [("R"|"D"|"L"|"U", distance),...]
    instructions = [
        ("RDLU"[int((c := line.split()[2])[-2])],
         int(c[2:7], 16))
        for line in file.readlines()
    ]

    # Follow instructions to walk around the block loop, while noting the point coordinates of the left and right
    # side corners. E.g. on a right U-turn (e.g. up, right, down), the middle segment's left edge is 1 longer and
    # its right edge is 1 shorter than the number of blocks in the segment. In an S-curve (same direction on the
    # segment before and after), both edges of the middle segment are the same length as its number of blocks.
    left_edge: list[(int, int)] = [(0, 0)]
    right_edge: list[(int, int)] = [(0, 0)]
    for (db, lb), (d, l), (da, la) in iter_with_neighbors(instructions):
        # set flag to 0 if direction before/after is equal, 1 if it would be a right U-turn, -1 if it's a left U-turn
        flag = 1 if "".join((db, d, da)) in "RDLURD" else 0 if db == da else -1
        l_left, l_right = l + flag, l - flag  # left/right edge length in walking direction
        sign = 1 if d in "DR" else -1  # walking on an axis in positive or negative direction
        yl, xl = left_edge[-1]
        yr, xr = right_edge[-1]
        left_edge.append((yl + sign * l_left, xl) if d in "UD" else (yl, xl + sign * l_left))
        right_edge.append((yr + sign * l_right, xr) if d in "UD" else (yr, xr + sign * l_right))
    left_edge.pop()  # end == start, count only once
    right_edge.pop()

    # find polygon orientation, swap inner/outer if the clockwise assumption was wrong, we need the real outer list.
    top_left = min(left_edge)
    tli = left_edge.index(top_left)
    if left_edge[tli][0] == left_edge[tli + 1][0]:  # y0==y1, polygon is clockwise, left edge is outer edge
        polygon = left_edge
    else:  # polygon is counter-clockwise, right edge is outer edge
        polygon = right_edge

    # Now we have a large polygon describing the outer edge of the lagoon, defined as list of point coordinates,
    # on which we can apply a variant of "Gauss's area formula" / "surveyor's formula"
    # (see https://en.wikipedia.org/wiki/Shoelace_formula#Other_formulas) to get the enclosed area:
    area = abs(sum(y * (xb - xa) for (yb, xb), (y, x), (ya, xa) in iter_with_neighbors(polygon)) // 2)

    print(f"The larger lagoon can hold a total of {area} cubic meters of lava.")


def iter_with_neighbors[T](l: list[T]) -> Iterable[tuple[T, T, T]]:
    """
    :param l: input list
    :return: zipped tuples of neighbors: (before, item, after)
    """
    return zip(l[-1:] + l[:-1], l, l[1:] + l[:1])


TEST_INPUT = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
