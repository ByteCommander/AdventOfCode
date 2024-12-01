# Advent Of Code 2024, day 1, part 1
# http://adventofcode.com/2024/day/1
# solution by ByteCommander, 2024-12-01
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    left, right = [], []
    for line in file:
        l, r = map(int, line.strip().split())
        left.append(l)
        right.append(r)

    d = 0
    for l, r in zip(sorted(left), sorted(right)):
        d += abs(l - r)

    print(f"The sum of all distances of sorted item pairs is {d}.")


TEST_INPUT = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
