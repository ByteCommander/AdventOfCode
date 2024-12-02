# Advent Of Code 2024, day 2, part 1
# http://adventofcode.com/2024/day/2
# solution by ByteCommander, 2024-12-02
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    reports = [[int(n) for n in line.split()] for line in file]
    safe = 0
    for report in reports:
        increasing = None
        for a, b in zip(report, report[1:]):
            if increasing is None:
                increasing = a < b
            elif increasing != (a < b):
                break
            if not (1 <= abs(a-b) <= 3):
                break
        else:
            safe += 1

    print(f"The input contains {safe} safe reports.")


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
