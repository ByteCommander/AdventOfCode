# Advent Of Code 2023, day 1, part 2
# http://adventofcode.com/2023/day/1
# solution by ByteCommander, 2023-12-11
import re
from typing import TextIO

from aoc_tools.lib import run

DIGITS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9"
}
# Note: using lookahead "(?=(...))" to get zero-width matches, so that they can overlap!
# This is not well documented in the question or original test case, but e.g. "oneight" should evaluate to 18.
RE_DIGITS = re.compile(rf"(?=(\d|{'|'.join(DIGITS.keys())}))")


def main(file: TextIO):
    total = 0
    for line in file:
        digits = [d if d.isdigit() else DIGITS[d] for d in RE_DIGITS.findall(line)]
        total += int(digits[0] + digits[-1])
    print("The sum of all calibration values is:", total)


TEST_INPUT = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

if __name__ == "__main__":
    run(main, TEST_INPUT)
