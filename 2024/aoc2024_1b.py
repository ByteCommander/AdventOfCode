# Advent Of Code 2024, day 1, part 2
# http://adventofcode.com/2024/day/1
# solution by ByteCommander, 2024-12-01
from collections import Counter
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    left, right = [], []
    for line in file:
        l, r = map(int, line.strip().split())
        left.append(l)
        right.append(r)

    factors = Counter(right)
    similarity = sum(l * factors[l] for l in left)

    print(f"The similarity score, sum of each left number multiplied by its count in the right list, is {similarity}.")


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
