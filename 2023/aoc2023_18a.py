# Advent Of Code 2023, day 18, part 1
# http://adventofcode.com/2023/day/18
# solution by ByteCommander, 2023-12-18
from operator import itemgetter
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    trench: list[(int, int)] = [(0, 0)]
    for line in file:
        y, x = trench[-1]
        d, l_, c_ = line.split()
        l = int(l_)
        c = c_[2:-1]
        for i in range(1, l + 1) if d in "DR" else range(-1, -l - 1, -1):
            trench.append((y + i, x) if d in "UD" else (y, x + i))
    trench.pop()  # end == start, count only once

    # normalize trench to ensure y,x >= 0 and ensure clockwise block order starting from top left
    min_y = min(map(itemgetter(0), trench))
    min_x = min(map(itemgetter(1), trench))
    trench = [(y - min_y, x - min_x) for y, x in trench]
    top_left = min(trench)
    tli = trench.index(top_left)
    trench = trench[tli:] + trench[:tli]
    if trench[0][0] != trench[1][0]:  # trench order is counter-clockwise
        trench.reverse()
        trench = trench[-1:] + trench[:-1]

    # Flood fill interior of trench loop from every possible edge field.
    # Seems like it would probably have been enough to do a single point flood fill though,
    # because all interior fields are connected to one single large area.
    lagoon: set[(int, int)] = set(trench)
    # iterate over each connected field and the one "before" and "after"
    for (yb, xb), (y, x), (ya, xa) in zip(trench[-1:] + trench[:-1], trench, trench[1:] + trench[:1]):
        # Look around current pos, starting at pos "before", going counter-clockwise, until reaching next-pos.
        # This finds adjacent free tiles on the right hand side of the trench, for flood-filling as enclosed space.
        neighbors = [(y - 1, x), (y, x - 1), (y + 1, x), (y, x + 1)]  # neighbors of (y,x) ordered counter-clockwise
        ni = neighbors.index((yb, xb))
        for yn, xn in neighbors[ni + 1:] + neighbors[:ni]:  # loop around, starting behind the pos "before"
            if (yn, xn) == (ya, xa):  # hitting next trench segment, so we finished the right hand side
                break
            if (yn, xn) not in lagoon:  # right hand side neighbor tile is free, start flooding
                edge: list[(int, int)] = [(yn, xn)]
                while edge:  # flood fill and add all connected fields which aren't part of the lagoon yet
                    ye, xe = edge.pop()
                    # print("flooding from", (yn, xn), ":", (ye, xe))
                    lagoon.add((ye, xe))
                    for yen, xen in [(ye - 1, xe), (ye, xe - 1), (ye + 1, xe), (ye, xe + 1)]:
                        if (yen, xen) not in lagoon:
                            edge.append([yen, xen])

    print(f"The lagoon can hold a total of {len(lagoon)} cubic meters of lava.")


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
