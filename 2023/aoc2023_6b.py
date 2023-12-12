# Advent Of Code 2023, day 6, part 2
# http://adventofcode.com/2023/day/6
# solution by ByteCommander, 2023-12-12
from math import ceil, floor, sqrt
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    rtime = int("".join(file.readline().split()[1:]))
    rdist = int("".join(file.readline().split()[1:]))

    # naive approach (works, but brute force takes ~3-4s for real input)
    # wins = sum(1 for t in range(1, rtime) if t * (rtime - t) > rdist)

    # Mathematical approach realizes that f(t)=t*(r-t) is an inverted parabola (-t**2 + r*t), so we only need
    # to solve -t**2 + t*rtime - rdist = 0 to get the boundaries of the winning range and find its width.

    # using https://en.wikipedia.org/wiki/Quadratic_formula:
    _qfroot = sqrt(rtime ** 2 - 4 * rdist)
    low = ceil((rtime - _qfroot) / 2)
    high = floor((rtime + _qfroot) / 2)

    print(f"You win between {low} and {high}ms (inclusive), for a total of {high - low + 1} configurations.")


TEST_INPUT = """
Time:      7  15   30
Distance:  9  40  200
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
