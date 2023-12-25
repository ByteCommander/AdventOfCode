# Advent Of Code 2023, day 24, part 1
# http://adventofcode.com/2023/day/24
# solution by ByteCommander, 2023-12-24
from itertools import combinations
from typing import TextIO

import numpy as np

from aoc_tools.lib import run

XY_MIN, XY_MAX = 200000000000000, 400000000000000  # test case: 7, 27

type Hailstone = (int, int, int, int, int, int)  # (position x, y, z, velocity x, y, z)

def main(file: TextIO):
    hailstones: list[Hailstone] = []
    for line in file:
        hailstones.append(tuple(
            int(n) for n in line.strip().replace("@", ",").split(",")
        ))

    # Find intersections of the future paths of each hailstone, even if they don't actually collide.
    # Linear path equation of each stone: y = py + (x-px) * vy/vx = (m := vy/vx)*x + (c := py-px*m)
    # So the intersection x,y is the solution of m0*x-1y=-c0 and m1*x-1y=-c1.
    # This linear equation system can be solved e.g. by numpy.

    intersections: list[tuple[Hailstone, Hailstone]] = []
    for stone0, stone1 in combinations(hailstones, 2):
        (x0, y0, z0, vx0, vy0, vz0), (x1, y1, z1, vx1, vy1, vz1) = stone0, stone1
        m0, m1 = vy0 / vx0, vy1 / vx1
        c0, c1 = y0 - x0 * m0, y1 - x1 * m1
        try:
            xi, yi = np.linalg.solve(np.array([[m0, -1], [m1, -1]]), np.array([-c0, -c1]))
        except np.linalg.LinAlgError:
            # print(stone0, stone1, "no intersection")
            continue  # Singular matrix, i.e. the lines have no intersection
        if XY_MIN <= xi <= XY_MAX and XY_MIN <= yi <= XY_MAX:
            # check if we're on the "future" (t>0) part of the paths: xi=x0+t*vx0 -> t=(xi-x0)/vx0, ...
            if (xi - x0) / vx0 > 0 and (xi - x1) / vx1 > 0 and (yi - y0) / vy0 > 0 and (yi - y1) / vy1:
                intersections.append((stone0, stone1))
                # print(stone0, stone1, (xi, yi), "valid intersection!")
            # else:
            #     print(stone0, stone1, (xi, yi), "intersection in the past")
        # else:
        #     print(stone0, stone1, (xi, yi), "intersection outside boundaries")

    print(f"There are a total of {len(intersections)} potential intersections in the observed area.")


TEST_INPUT = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
