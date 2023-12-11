# Advent Of Code 2023, day 1, part 1
# http://adventofcode.com/2023/day/1
# solution by ByteCommander, 2023-12-11
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    total = 0
    for line in file:
        digits = [c for c in line if c.isdigit()]
        total += int(digits[0] + digits[-1])
    print("The sum of all calibration values is:", total)


TEST_INPUT = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

if __name__ == "__main__":
    run(main, TEST_INPUT)
