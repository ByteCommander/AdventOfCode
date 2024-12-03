# Advent Of Code 2024, day 3, part 1
# http://adventofcode.com/2024/day/3
# solution by ByteCommander, 2024-12-03
import re
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    code = file.read().strip()
    muls = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", code)
    result = sum(int(a) * int(b) for a, b in muls)
    print(f"The sum of all mul() expressions in the code is {result}.")


TEST_INPUT = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
