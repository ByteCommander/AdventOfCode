# Advent Of Code 2024, day 3, part 2
# http://adventofcode.com/2024/day/3
# solution by ByteCommander, 2024-12-03
import re
from typing import TextIO

from aoc_tools.lib import run


def main(file: TextIO):
    code = file.read().strip()
    stmts = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(?:(do)|(don't))\(\)", code)  # (mul_a, mul_b, do, dont)
    result = 0
    enabled = True
    for mul_a, mul_b, do, dont in stmts:
        if do:
            enabled = True
        elif dont:
            enabled = False
        elif enabled:
            result += int(mul_a) * int(mul_b)
    print(f"The sum of all enabled mul() expressions in the code is {result}.")


TEST_INPUT = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
