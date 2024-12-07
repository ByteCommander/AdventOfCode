# Advent Of Code 2024, day 7, part 1
# http://adventofcode.com/2024/day/7
# solution by ByteCommander, 2024-12-07
from operator import add, mul
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    calibration = 0
    for line in file:
        left, right = line.split(":")
        target = int(left)
        args = [int(r) for r in right.split()]

        if recurse(target, args[0], args[1:]):
            calibration += target

    print(f"The total calibration result is {calibration}.")


def recurse(target: int, result: int, args: list[int]) -> bool:
    arg, *args = args
    for op in [mul, add]:
        res = op(result, arg)
        if not args:
            if res == target:
                return True
        elif res > target:  # abort early if intermediate result is getting too big, as there is no sub or div
            continue
        elif recurse(target, res, args):
            return True
    return False


TEST_INPUT = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
