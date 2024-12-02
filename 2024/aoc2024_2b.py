# Advent Of Code 2024, day 2, part 2
# http://adventofcode.com/2024/day/2
# solution by ByteCommander, 2024-12-02
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    reports = [[int(n) for n in line.split()] for line in file]
    safe = 0
    for report in reports:
        if check(report):
            safe += 1

    print(f"The input contains {safe} safe reports.")


def check(report: list[int], try_removing=True):
    steps = [b - a for a, b in zip(report, report[1:])]
    increasing = sum(s > 0 for s in steps) > 0  # more increasing than decreasing steps
    if all(1 <= abs(s) <= 3 and (s > 0) == increasing for s in steps):
        return True
    if try_removing:
        for i in range(len(steps) + 1):
            if check(report[:i] + report[i + 1:], try_removing=False):
                return True
    return False


TEST_INPUT = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
