# Advent Of Code 2024, day 14, part 1
# http://adventofcode.com/2024/day/14
# solution by ByteCommander, 2024-12-17
import re
from math import prod
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    robots: list[list[tuple[int, int]]] = []  # [ [(px, py), (vx, vy)], ... ]
    for line in file:
        if l := line.strip():
            px_, py_, vx_, vy_ = re.fullmatch(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", l).groups()
            robots.append([(int(px_), int(py_)), (int(vx_), int(vy_))])

    for _sec in range(1, 101):
        for robot in robots:
            (px, py), (vx, vy) = robot  # type: int
            px = (px + vx) % WIDTH
            py = (py + vy) % HEIGHT
            robot[0] = (px, py)

    # for y in range(HEIGHT):
    #     print("".join(str(sum(1 for p, v in robots if p == (x, y)) or ".") for x in range(WIDTH)))

    quadrants: dict[tuple[bool, bool], int] = {(False, False): 0, (False, True): 0, (True, False): 0, (True, True): 0}
    hx, hy = WIDTH // 2, HEIGHT // 2
    for (px, py), _vxy in robots:
        if px == hx or py == hy:
            continue  # skip robots on the middle axes
        quadrants[px > hx, py > hy] += 1

    # print(quadrants)
    safety = prod(quadrants.values())
    print(f"The safety factor of the bathroom floor quadrants after 100 seconds is {safety}.")


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
    WIDTH, HEIGHT = 11, 7
    run(main, TEST_INPUT, test_only=True)
    WIDTH, HEIGHT = 101, 103
    run(main)
