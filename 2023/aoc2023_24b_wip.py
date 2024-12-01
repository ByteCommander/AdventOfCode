# Advent Of Code 2023, day 24, part 2
# http://adventofcode.com/2023/day/24
# solution by ByteCommander, 2023-12-24
from collections import Counter
from itertools import combinations
from typing import TextIO

import numpy as np

from aoc_tools.lib import run

type Hailstone = (int, int, int, int, int, int)  # (position x, y, z, velocity x, y, z)

def main(file: TextIO):
    hailstones: list[Hailstone] = []
    for line in file:
        hailstones.append(tuple(
            int(n) for n in line.strip().replace("@", ",").split(",")
        ))

    print(*Counter(h[5] for h in hailstones).most_common(), sep="\n")


TEST_INPUT = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
