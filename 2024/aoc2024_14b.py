# Advent Of Code 2024, day 14, part 2
# http://adventofcode.com/2024/day/14
# solution by ByteCommander, 2024-12-17
import re
from collections import Counter
from itertools import count
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    robots: list[list[tuple[int, int]]] = []  # [ [(px, py), (vx, vy)], ... ]
    for line in file:
        if l := line.strip():
            px_, py_, vx_, vy_ = re.fullmatch(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", l).groups()
            robots.append([(int(px_), int(py_)), (int(vx_), int(vy_))])

    sec = 0
    for sec in count(start=1):
        for robot in robots:
            (px, py), (vx, vy) = robot  # type: int
            px = (px + vx) % WIDTH
            py = (py + vy) % HEIGHT
            robot[0] = (px, py)

        rc = Counter(pxy for pxy, vxy in robots)
        if max(rc.values()) == 1:  # no fields containing two or more colliding robots, let's see if this is useful
            show(robots, sec)
            break  # this actually already matches the solution

    print(f"The robots seem to produce an image after {sec} seconds.")


def show(robots: list[list[tuple[int, int]]], frame: int):
    print(*[
        "".join(str(sum(1 for p, v in robots if p == (x, y)) or ".") for x in range(WIDTH))
        for y in range(HEIGHT)
    ], f"^----- Frame {frame} -----\n", sep="\n")


TEST_INPUT = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

if __name__ == "__main__":
    # no useful test case here, the example doesn't exhibit any similar behavior
    # WIDTH, HEIGHT = 11, 7
    # run(main, TEST_INPUT, test_only=True)
    WIDTH, HEIGHT = 101, 103
    run(main)
