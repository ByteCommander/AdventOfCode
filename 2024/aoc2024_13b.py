# Advent Of Code 2024, day 13, part 2
# http://adventofcode.com/2024/day/13
# solution by ByteCommander, 2024-12-17
import re
from typing import TextIO

import numpy as np

from aoc_tools.lib import run

OFFSET = 10000000000000


def main(file: TextIO):
    machines: list[tuple[int, int, int, int, int, int]] = []
    file_it = iter(file)
    while True:
        ax_, ay_ = re.fullmatch(r"Button A: X\+(\d+), Y\+(\d+)", next(file_it).strip()).groups()
        bx_, by_ = re.fullmatch(r"Button B: X\+(\d+), Y\+(\d+)", next(file_it).strip()).groups()
        px_, py_ = re.fullmatch(r"Prize: X=(\d+), Y=(\d+)", next(file_it).strip()).groups()
        machines.append((int(ax_), int(ay_), int(bx_), int(by_), int(px_) + OFFSET, int(py_) + OFFSET))
        if next(file_it, None) is None:  # blank line, or end of file
            break

    total = 0
    for ax, ay, bx, by, px, py in machines:
        # find exact solution, which may not be integer, either because no int solution exists or due to float errors
        af, bf = np.linalg.solve(np.array([[ax, bx], [ay, by]]), np.array([px, py]))
        # round to next int and verify it's correct
        a, b = round(af), round(bf)
        if ax * a + bx * b == px and ay * a + by * b == py:
            cost = a * 3 + b
            total += cost
            # print(a, b, cost)
        # else:
        #     print("No solution")

    print(f"You need to spend at least {total} tokens to win all possible prizes far away.")


TEST_INPUT = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
